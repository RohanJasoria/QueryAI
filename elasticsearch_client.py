# elasticsearch_client.py

from elasticsearch import Elasticsearch
from config import INDEX_NAME, MIN_SCORE, QUESTION_INDEX_NAME, QUERY_MIN_SCORE

class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(
            [
                {
                    'host': 'localhost',
                    'port': 9200,
                    'scheme': 'https'  # Specify the scheme as 'http'
                }
            ],
            http_auth=('elastic', 'ngqs3Swn7NjGY_PUcj9J'),  # Provide username and password
            ca_certs="/Users/rjasoria/Downloads/elasticsearch-8.14.3 2/config/certs/http_ca.crt"
        )

    def create_index(self):
        # Create an index with mapping for dense vectors
        mapping = {
            "mappings": {
                "properties": {
                    "text": {
                        "type": "text"
                    },
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 768,  # The number of dimensions should match the embedding size
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
        self.es.indices.create(index=INDEX_NAME, body=mapping, ignore=400)

    def index_document(self, text: str, embedding):
        # Index a document with its embedding
        document = {
            "text": text,
            "embedding": embedding
        }
        self.es.index(index=INDEX_NAME, body=document)

    def index_query(self, text: str, queryId: str, embedding):
        # Index a document with its embedding
        document = {
            "text": text,
            "embedding": embedding
        }
        self.es.index(index=QUESTION_INDEX_NAME, id=queryId, body=document)

    def index_document_given_index(self, text: str, idx: str, embedding):
        # Index a document with its embedding
        document = {
            "text": text,
            "embedding": embedding
        }
        self.es.index(index=idx, body=document)
    
    def delete_records(self):
        self.es.delete_by_query(index=INDEX_NAME, body={"query": {"match_all": {}}})

    def search_similar(self, query_embedding, k=5):
        # Search for the most similar documents
        query = {
            "field" : "embedding",
            "query_vector": query_embedding,
            "k": 5,
            "num_candidates": 500
        }
        
        response = self.es.knn_search(index=INDEX_NAME, knn=query, source=["text"])

        # Filter results based on min_score
        filtered_response = [
            hit for hit in response['hits']['hits']
            if hit['_score'] >= MIN_SCORE
        ]
        return filtered_response
    
    def search_similar_queries(self, query_embedding, k=5):
        # Search for the most similar documents
        query = {
            "field" : "embedding",
            "query_vector": query_embedding,
            "k": 5,
            "num_candidates": 500
        }
        
        response = self.es.knn_search(index=QUESTION_INDEX_NAME, knn=query, source=["id"])

        # Filter results based on min_score
        filtered_response = [
            hit for hit in response['hits']['hits']
            if hit['_score'] >= QUERY_MIN_SCORE
        ]
        return filtered_response
