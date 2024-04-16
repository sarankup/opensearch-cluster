from opensearchpy import OpenSearch
from opensearch_dsl import Search, Document, Text, Keyword


auth = ('admin', 'XXXXXXXXX')  # For testing only. Don't store credentials in code.
ca_certs_path = 'root-ca.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts=[{'host': "localhost", 'port': 9200}],
    http_compress=True,  # enables gzip compression for request bodies
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    # ca_certs=ca_certs_path
)
index_name = 'my-dsl-index'

index_body = {
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        }
    }
}

response = client.indices.create(index_name, index_body)
print('\nCreating index:')
print(response)

# Create the structure of the document
class Movie(Document):
    title = Text(fields={'raw': Keyword()})
    director = Text()
    year = Text()

    class Index:
        name = index_name

    def save(self, ** kwargs):
        return super(Movie, self).save(** kwargs)

# Set up the opensearch-py version of the document
Movie.init(using=client)
doc = Movie(meta={'id': 1}, title='Moneyball', director='Bennett Miller', year='2011')
response = doc.save(using=client)

print('\nAdding document:')
print(response)

# Perform bulk operations

movies = '{ "index" : { "_index" : "my-dsl-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n { "create" : { "_index" : "my-dsl-index", "_id" : "3" } } \n { "title" : "Star Trek Beyond", "director" : "Justin Lin", "year" : "2015"} \n { "update" : {"_id" : "3", "_index" : "my-dsl-index" } } \n { "doc" : {"year" : "2016"} }'

client.bulk(movies)

# Search for the document.
for x in range(100000):
    print(f"========{x}======")
    s = Search(using=client, index=index_name) \
        .filter('term', year='2011') \
        .query('match', title='Moneyball')

    response = s.execute()

    print('\nSearch results:')
    for hit in response:
        print(hit.meta.score, hit.title)
    
# Delete the document.
print('\nDeleting document:')
print(response)

# Delete the index.
#response = client.indices.delete(index = index_name)
#print('\nDeleting index:')
#print(response)