from elasticsearch import Elasticsearch


es = Elasticsearch(
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