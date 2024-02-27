from langchain.text_splitter import TokenTextSplitter
import chromadb
from pypdf import PdfReader
from Inference import EntityInference, FilterInference
from chromadb.utils import embedding_functions
import os
from tqdm import tqdm
import argparse
import json

EntityClusterLabelPrompt = """<s> [INST] Below is a list of key terms (entities) and the articles they were extracted from. The entities below have been clustered together based on their semantic similarity. Your task is to review the entities in this cluster and perform the following actions:
1. Review the entities in the cluster.
2. Identify if any smaller groups of entities basically mean the same thing. Think of it as finding synonyms within the group.
3. For each of these smaller groups, choose or create a single label that best represents all the entities in it.
4. If a group has just one entity, decide if its label is clear as is or if it should be changed to be more understandable.
5. Format your findings in JSON as follows:

*start
{{
    "Labels": [
        {{
            "label": "<label>", 
            "entities": ["<entity1>", "<entity2>", ...]
            "entityIDs": ["<entityID1>", "<entityID2>", ...]
        }},
        ...
    ]
}}
*end

Entities and their IDs:
{entities} [/INST]"""


text_splitter = TokenTextSplitter( # Create an instance of the CharacterTextSplitter class (https://python.langchain.com/docs/modules/data_connection/document_transformers/split_by_token#tiktoken)
    chunk_size=1000, chunk_overlap=200
) # Th

pdfs_directory = "pdfs/"
persist_directory = "vectordbs/"
chromadb_client = chromadb.PersistentClient(path=persist_directory)

def main(vectordb_name, st_model_name):
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=st_model_name,
        device="cuda",
        normalize_embeddings=True
    )

    try:
        chromadb_client.delete_collection(vectordb_name)
    except:
        pass

    vectordb = chromadb_client.create_collection(name=vectordb_name,
                                                embedding_function=sentence_transformer_ef,
                                                get_or_create=True)

    # Load json file directory with clustered entities
    cluster_dir = "ClusteredEntities"

    skipped_files = []

    for filename in os.listdir(cluster_dir):
        if filename.endswith(".json"):
            with open(os.path.join(cluster_dir, filename), "r") as f:
                data = json.load(f)

                entity_strings = []
                for entity in data:
                    #entity_str = f"Entity: {entity['document']}\nEntityID: {entity['id']}\nSource Article: {entity['metadata']['originalText']}\n"
                    entity_str = f"Entity: {entity['document']}\nEntityID: {entity['id']}\n"
                    entity_strings.append(entity_str)

                entity_context = "\n".join(entity_strings)

                prompt = EntityClusterLabelPrompt.format(entities=entity_context)

                count = 0
                while count < 5:
                    try:
                        labels = FilterInference(prompt)
                        if labels != "Failed to parse JSON.":
                            break
                    except:
                        count += 1
                        continue

                if count == 5:
                    skipped_files.append(filename)
                    print(f"Failed to extract labels for {filename}.")
                    continue

                # Check if 'Labels' key exists in the dictionary and it contains a list
                if 'Labels' in labels and isinstance(labels['Labels'], list):
                    for label in labels['Labels']:
                        label_id = str(vectordb.count() + 1)
                        labelName = label['label']
                        # Now you have the label and the entities for each label
                        print(f"Label: {labelName}")
                        for entity in label['entities']:
                            print(f"Entity: {entity}")

                        # Ensure metadata is a dictionary
                        metadata = {
                            "entities": str(label['entities']),
                            "entityIDs": str(label['entityIDs'])
                        }

                        vectordb.add(ids=[label_id], 
                                    documents=[labelName],
                                    metadatas=[metadata])  # Pass the dictionary as metadata

                        print(f"Label {labelName} added to the database.")
                else:
                    print("No labels extracted.")
                    continue

    if len(skipped_files) > 0:
        print(f"Skipped files: {skipped_files}")
        with open("skipped_files.txt", "w") as f:
            f.write("\n".join(skipped_files))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract entities from PDFs and store them in a vector database.")
    parser.add_argument("--vectordb_name", type=str, default="FinalEntities", help="Name of the vector database to store the entities.")
    parser.add_argument("--st_model_name", type=str, default="BAAI/bge-large-en-v1.5", help="Sentence Transformer model name.")
    args = parser.parse_args()
    main(args.vectordb_name, args.st_model_name)