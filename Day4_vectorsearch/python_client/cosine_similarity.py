import pandas as pd
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
import os
import json

load_dotenv()

ES_CID = os.getenv('ES_CID')
ES_USER = os.getenv('ES_USER')
ES_PWD = os.getenv('ES_PWD')

# Step 1: Create elasticsearch connection
def connect_elasticsearch():
    es = Elasticsearch(
        cloud_id=ES_CID,
        basic_auth=(ES_USER, ES_PWD))
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
    return es

# Step 2: Load data from CSV
def load_data(file_path):
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records from {file_path}")
    return df

# Step 3: Generate embeddings using Sentence Transformers
def generate_embeddings(text_list):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(text_list, convert_to_numpy=True)
    print(f"Generated embeddings with shape: {embeddings.shape}")
    print("Sample Embedding:", embeddings[0])
    return embeddings, model

# Step 4: Create Elasticsearch index
def create_index(es_client, index_name, dims):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
        print(f"Deleted existing index: {index_name}")
    
    index_body = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }
    es_client.indices.create(index=index_name, body=index_body)
    print(f"Created index: {index_name}")

# Step 5: Index documents into Elasticsearch
def index_documents(es_client, index_name, df, embeddings):
    actions = []
    for i, row in df.iterrows():
        action = {
            "_index": index_name,
            "_id": row['id'],
            "_source": {
                "title": row['title'],
                "content": row['content'],
                "embedding": embeddings[i].tolist()
            }
        }
        actions.append(action)
    
    helpers.bulk(es_client, actions)
    print(f"Indexed {len(actions)} documents into {index_name}")

    # Debug: Check if documents are indexed
    count = es_client.count(index=index_name)
    print(f"Total documents indexed: {count['count']}")

# Step 6: Perform kNN search using cosine similarity
# k=5
def search_similar_docs(es_client, index_name, query_text, model, k=5):
    query_vector = model.encode([query_text], convert_to_numpy=True)[0]
    print(f"Query vector generated with shape: {query_vector.shape}")
    print("Query Vector:", query_vector)
    
    try:
        response = es_client.search(
            index=index_name,
            size=k,
            query={
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_vector.tolist()}
                    }
                }
            }
        )
        print("Raw Response:", json.dumps(response.body, indent=2))
        return response['hits']['hits']
    except Exception as e:
        print(f"Error during search: {e}")
        return []

# Main function to run the script
if __name__ == "__main__":
    # Configuration
    FILE_PATH = '../data.csv'
    INDEX_NAME = 'cosine_sim_test'
    
    # Connect to Elasticsearch
    es = connect_elasticsearch()

    # Check if connection is successful
    if not es.ping():
        print("Connection to Elasticsearch failed!")
        exit()

    # Load data from CSV
    df = load_data(FILE_PATH)
    
    # Generate embeddings
    embeddings,model = generate_embeddings(df['content'].tolist())
    
    # Create index in Elasticsearch
    create_index(es, INDEX_NAME, embeddings.shape[1])
    
    # Index documents into Elasticsearch
    index_documents(es, INDEX_NAME, df, embeddings)
    
    # Perform a cosine similarity search
    query = "Big data"
    print(f"\nPerforming search for query: '{query}'")
    results = search_similar_docs(es, INDEX_NAME, query, model)
    
    # Display the search results
    if results:
        print("\nTop Similar Documents:")
        for result in results:
            print(f"ID: {result['_id']}, Score: {result['_score']}, Title: {result['_source']['title']}")
    else:
        print("\nNo similar documents found.")
