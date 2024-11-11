import pandas as pd
from elasticsearch import Elasticsearch, helpers
import csv
from dotenv import load_dotenv
import os

load_dotenv()

ES_CID = os.getenv('ES_CID')
ES_USER = os.getenv('ES_USER')
ES_PWD = os.getenv('ES_PWD')

def read_csv_file(file_path):
    return pd.read_csv(file_path,encoding='latin1')

def connect_elasticsearch():
    es = Elasticsearch(
        cloud_id=ES_CID,
        basic_auth=(ES_USER, ES_PWD))
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
    return es

def csv_to_elasticsearch_actions(df, index_name):
    for _, row in df.iterrows():
        yield {
            "_index": index_name,
            "_source": row.to_dict()
        }

def upload_csv_to_elasticsearch(file_path, index_name):
    # Read CSV data
    df = read_csv_file(file_path)

    # Connect to Elasticsearch
    es = connect_elasticsearch()
    if not es:
        return

    # Create index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")

    # Convert DataFrame to Elasticsearch actions
    actions = csv_to_elasticsearch_actions(df, index_name)

    # Upload data using bulk API
    try:
        helpers.bulk(es, actions)
        print(f"Data successfully uploaded to index '{index_name}'.")
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    # Specify your CSV file path and Elasticsearch index name
    csv_file_path = "../dataset/superstore.csv"
    index_name = "superstore"

    # Upload the CSV file to Elasticsearch
    upload_csv_to_elasticsearch(csv_file_path, index_name)


