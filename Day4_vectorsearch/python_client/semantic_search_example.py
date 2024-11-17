import torch
from transformers import AutoTokenizer, AutoModel
from elasticsearch import Elasticsearch
import time
from dotenv import load_dotenv
import os

load_dotenv()

ES_CID = os.getenv('ES_CID')
ES_USER = os.getenv('ES_USER')
ES_PWD = os.getenv('ES_PWD')

# Step 1: Load the pre-trained BERT model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    """Generate an embedding for a given text using BERT."""
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    # Take the mean of the token embeddings to get a sentence embedding
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
    return embedding

# Step 2: Connect to Elasticsearch
def connect_elasticsearch():
    es = Elasticsearch(
        cloud_id=ES_CID,
        basic_auth=(ES_USER, ES_PWD))
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
    return es
index_name = "semantic_search"

def create_index():
    """Create an Elasticsearch index with a dense vector field."""
    index_mapping = {
        "mappings": {
            "properties": {
                "content": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 384}
            }
        }
    }
    
    # Delete the index if it already exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Deleted existing index: {index_name}")

    # Create a new index
    es.indices.create(index=index_name, body=index_mapping)
    print(f"Created index: {index_name}")

def index_documents(documents):
    """Index a list of documents with their embeddings."""
    for doc in documents:
        embedding = get_embedding(doc['content'])
        es.index(index=index_name, body={"content": doc['content'], "embedding": embedding})
        print(f"Indexed document: {doc['content']}")

def search_semantically(query, k=3):
    """Search Elasticsearch for semantically similar documents."""
    query_embedding = get_embedding(query)
    
    # Perform KNN search
    response = es.search(
        index=index_name,
        body={
            "knn": {
                "field": "embedding",
                "query_vector": query_embedding,
                "k": k,
                "num_candidates": 10
            }
        }
    )
    
    return response['hits']['hits']

if __name__ == "__main__":
    # Connect to Elasticsearch
    es = connect_elasticsearch()
    
    # Step 3: Create the Elasticsearch index
    create_index()
    
    # Step 4: Sample documents to index
    documents = [
        {"id": 1, "content": "Climate change is affecting agriculture worldwide."},
        {"id": 2, "content": "The impact of global warming on crop yields is concerning."},
        {"id": 3, "content": "Artificial intelligence is transforming industries."},
        {"id": 4, "content": "Renewable energy sources like solar and wind are vital for the future."},
        {"id": 5, "content": "Machine learning models are being used to predict crop failures."}
    ]
    
    # Step 5: Index documents with embeddings
    index_documents(documents)
    time.sleep(2)  # Wait for indexing to complete

    # Step 6: Perform a semantic search query
    query = "Effects of climate on farming"
    print(f"\nSearch Query: '{query}'")
    
    results = search_semantically(query)
    
    # Step 7: Display search results
    print("\nSearch Results:")
    for res in results:
        content = res['_source']['content']
        score = res['_score']
        print(f"Score: {score:.4f}, Content: {content}")
