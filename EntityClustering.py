import argparse
import chromadb
from chromadb.utils import embedding_functions
import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import json
import shutil
from tqdm import tqdm

def create_docs_from_results(results):
    documents = results["documents"]
    metadatas = results["metadatas"]
    embeddings = results["embeddings"]
    ids = results["ids"]

    docs = []
    for document, metadata, embedding, id in zip(documents, metadatas, embeddings, ids):
        doc = {
            "document": document,
            "metadata": metadata,
            "embedding": np.array(embedding),
            "id": id
        }
        docs.append(doc)
    return docs

def main(sentence_transformer_ef, vector_db, min_clusters=2, max_clusters=200):
    # Correct the function definition to accept parameters or remove them if not needed
    pdfs_directory = "pdfs/"
    persist_directory = "vectordbs/"
    chromadb_client = chromadb.PersistentClient(path=persist_directory)

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=sentence_transformer_ef,
        device="cuda",
        normalize_embeddings=True
    )

    vectordb = chromadb_client.get_collection(name=vector_db, 
                                        embedding_function=sentence_transformer_ef)

    limit = vectordb.count()
    print(f"Number of documents in the collection: {limit}")

    result = vectordb.get(limit=limit, include=["documents", "embeddings", "metadatas"])
    docs = create_docs_from_results(result)

    OutputDir = "ClusteredEntities"
    if os.path.exists(OutputDir):
        # Remove the directory and its contents
        shutil.rmtree(OutputDir)
    os.makedirs(OutputDir)

    # Extract embeddings
    embeddings = np.array([doc['embedding'] for doc in docs])

    # Standardize the features
    scaler = StandardScaler()
    scaled_embeddings = scaler.fit_transform(embeddings)

    # Determine the optimal number of clusters using silhouette analysis with tqdm progress bar
    max_clusters = min(max_clusters, len(docs))
    best_score = -1
    best_n_clusters = min_clusters  # Use min_clusters argument
    for n_clusters in tqdm(range(min_clusters, max_clusters + 1), desc="Finding optimal clusters"):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_embeddings)
        silhouette_avg = silhouette_score(scaled_embeddings, cluster_labels)
        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_n_clusters = n_clusters

    # Clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
    kmeans.fit(scaled_embeddings)
    labels = kmeans.labels_

    # Save each cluster to a separate JSON file with tqdm progress bar
    for cluster_id in tqdm(range(best_n_clusters), desc="Saving clusters"):
        cluster_docs = [doc for doc, label in zip(docs, labels) if label == cluster_id]
        # remove the embedding field
        for doc in cluster_docs:
            doc.pop('embedding', None)
        with open(f'{OutputDir}/cluster_{cluster_id}.json', 'w') as f:
            json.dump(cluster_docs, f, ensure_ascii=False, indent=4)

    print(f"Clustering completed with {best_n_clusters} clusters. Data saved in '{OutputDir}' directory.")

if __name__ == "__main__":
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description='Cluster documents into JSON files.')
    parser.add_argument('--min_clusters', type=int, default=2, help='Minimum number of clusters.')
    parser.add_argument('--max_clusters', type=int, default=200, help='Maximum number of clusters.')
    parser.add_argument('--st_model', type=str, default="Salesforce/SFR-Embedding-Mistral", help='Sentence Transformer model name.')
    parser.add_argument('--vector_db', type=str, default="Entities", help='VectorDB name.')
    args = parser.parse_args()

    # Call the main function with the command line argument
    main(args.st_model, args.vector_db, args.min_clusters, args.max_clusters)
