from langchain.text_splitter import TokenTextSplitter
import chromadb
from pypdf import PdfReader
from Inference import EntityInference, FilterInference
from chromadb.utils import embedding_functions
import os
from tqdm import tqdm
import argparse

EntityExtractionPrompt = """<s> [INST] Start by reading the article on light therapy provided. Your goal is to identify all key terms (entities) relevant to the subject. These entities are crucial for constructing a decision tree within a chatbot application designed to manage and adjust light therapy device settings based on user interactions.

Procedure:
1. Extract entities from the article.
2. Label each entity with a descriptive category.

Format your findings in JSON as follows:

*start
{{
    "entities": [
        {{"entity": "<entity1>", "label": "<label1>"}},
        {{"entity": "<entity2>", "label": "<label2>"}},
        ...
    ]
}}
*end

If no entities are identified, present an empty list in the same format.

*start
{{
    "entities": []
}}
*end

Consider the context:
{Article} [/INST]"""


EntityFilterPromptTemplate = """<s> [INST] This task involves a critical review of a provided list of entities related to light therapy. These entities have already been extracted and labeled from an article. Your objective is to sift through these entities to filter out any that are not directly relevant to the functionality of a chatbot designed for managing light therapy device settings based on user input and initial configurations.

Criteria for Filtering:
- Retain entities that have a direct impact on decision-making for light therapy device settings.
- Exclude entities that are authors' names, people's names, publication dates, locations or any details not contributing to the chatbot's decision tree.
- Focus on keeping entities that aid in understanding and adjusting light therapy based on user feedback.

Reformat the refined list into the specified JSON structure:

*start
{{
    "entities": [
        <entity1>,
        <entity2>,
        ...
    ]
}}
*end

If no relevant entities are found, use an empty list:

*start
{{
    "entities": []
}}
*end

Consider the context:
{Article} [/INST]"""

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

    # Step 1: Load each pdf in the directory
    pdfs = [f for f in os.listdir(pdfs_directory) if f.endswith(".pdf")]

    for pdf in tqdm(pdfs, desc="Processing PDFs"):
        reader = PdfReader(pdfs_directory + pdf)
        pages = reader.pages
        total_pages = len(pages)

        for page_number, page in enumerate(tqdm(pages, desc=f"{pdf} Progress", leave=False), start=1):
            text = page.extract_text()
            chunks = text_splitter.split_text(text)
            for chunk in chunks:
                # Step 2: Extract entities from each chunk
                prompt = EntityExtractionPrompt.format(Article=chunk)
                # Assuming 'entities_data' is the output from 'EntityInference'
                entities_data = EntityInference(prompt)

                EntityFilterPrompt = EntityFilterPromptTemplate.format(Article=chunk)

                filtered_entities = FilterInference(EntityFilterPrompt)

                # check if entities_data is NoneType
                if filtered_entities is None:
                    print("No entities extracted.")
                    continue

                # Check if 'entities' key exists in the dictionary and it contains a list
                if 'entities' in filtered_entities and isinstance(filtered_entities['entities'], list):
                    for entity in filtered_entities['entities']:
                        entityName = entity
                        # Now you have the entityType and entityName for each entity
                        print(f"Entity: {entityName}")

                        # Example: Saving the entity to the database (pseudocode)
                        entity_id = str(vectordb.count() + 1)
                        metadata = {
                            "originalText": chunk,  # Ensure 'chunk' is defined in your context
                            "page": page.page_number,  # Make sure 'page' object has a 'number' attribute or is correctly defined
                            "originalPdf": pdf,  # Ensure 'pdf' variable is defined and holds the name of the PDF
                        }
                        vectordb.add(ids=[entity_id],
                                    documents=[entityName],
                                    metadatas=[metadata])
                        print(f"Added {entityName} to the database.")
                
                else:
                    print("No entities extracted.")
                    continue

    print("Finished processing all PDFs.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract entities from PDFs and store them in a vector database.")
    parser.add_argument("--vectordb_name", type=str, default="Entities", help="Name of the vector database to store the entities.")
    parser.add_argument("--st_model_name", type=str, default="Salesforce/SFR-Embedding-Mistral", help="Name of the sentence transformer embedding function to use.")
    args = parser.parse_args()
    main(args.vectordb_name, args.st_model_name)