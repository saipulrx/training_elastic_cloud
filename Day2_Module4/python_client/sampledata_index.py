import os
import time
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ES_CID = os.getenv('ES_CID')
ES_USER = os.getenv('ES_USER')
ES_PWD = os.getenv('ES_PWD')

es = Elasticsearch(
    cloud_id=ES_CID,
    basic_auth=(ES_USER, ES_PWD)
)

print(es.info())

mymovie = {
  'release_year': '1908',
  'title': 'It is not this day.',
  'origin': 'American',
  'director': 'D.W. Griffith',
  'cast': 'Harry Solter, Linda Arvidson',
  'genre': 'comedy',
  'wiki_page':'https://en.wikipedia.org/wiki/A_Calamitous_Elopement',
  'plot': 'A young couple decides to elope after being caught in the midst of a romantic moment by the woman .'
}

response = es.index(index='movies_test', document=mymovie)
print(response)

# Write the '_id' to a file named tmp.txt
with open('tmp.txt', 'w') as file:
    file.write(response['_id'])

# Print the contents of the file to confirm it's written correctly
with open('tmp.txt', 'r') as file:
    print(f"document id saved to tmp.txt: {file.read()}")

time.sleep(2)

response = es.search(index='movies_test', query={"match_all": {}})
print("Sample movie data in Elasticsearch:")
for hit in response['hits']['hits']:
    print(hit['_source'])