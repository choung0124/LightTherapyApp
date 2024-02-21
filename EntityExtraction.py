from langchain.text_splitter import TokenTextSplitter
import chromadb
from pypdf import PdfReader
from Inference import EntityInference
from chromadb.utils import embedding_functions
import os

text_splitter = TokenTextSplitter( # Create an instance of the CharacterTextSplitter class (https://python.langchain.com/docs/modules/data_connection/document_transformers/split_by_token#tiktoken)
    chunk_size=1000, chunk_overlap=200
) # Th

pdfs_directory = "pdfs/"
persist_directory = "vectordbs/"
chromadb_client = chromadb.PersistentClient(path=persist_directory)

VectorDBName = "Entities"

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="intfloat/multilingual-e5-large-instruct",
    device="cuda",
    normalize_embeddings=True
)

try:
    chromadb_client.delete_collection(VectorDBName)
except:
    pass

vectordb = chromadb_client.create_collection(name=VectorDBName,
                                             embedding_function=sentence_transformer_ef,
                                             get_or_create=True)

EntityExtractionPrompt = """<s> [INST] Below is an article related to light therapy
Your job is to extract the entities from the article.
The extracted entities will be used to construct a decision tree.
The decision tree is part of the logic for a chatbot app that will be used to set, and adjust light device settings for a patient undergoing light therapy.
This decision tree will be used to 1. Determine the starting settings for the light devices and, 2. Adjust the settings based on the user's feedback.
Extract the entities that are relevant to the decision tree.
Do not extract more than 20 entities.
When presenting the extracted entities, please use the following format:
*start
{{
    "entities": [
        <entity1>,
        <entity2>,
        ...
    ]
}}
*end
Please make sure your response is a valid JSON object.
Please enclose all the entities in double quotes.
if there are no entities or relations, please present the following:
{{
    "entities": [],
}}
Article:
{Article} [/INST]"""


# Step 1: Load each pdf in the directory
pdfs = [f for f in os.listdir(pdfs_directory) if f.endswith(".pdf")]

for pdf in pdfs:
    reader = PdfReader(pdfs_directory + pdf)
    pages = reader.pages

    for page in pages:
        text = page.extract_text()
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            print(chunk)
            # Step 2: Extract entities from each chunk
            prompt = EntityExtractionPrompt.format(Article=chunk)
            print(prompt)
            # Assuming 'entities_data' is the output from 'EntityInference'
            entities_data = EntityInference(prompt)

            # Check if 'entities' key exists in the dictionary and it contains a list
            if 'entities' in entities_data and isinstance(entities_data['entities'], list):
                for entity in entities_data['entities']:
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
            
