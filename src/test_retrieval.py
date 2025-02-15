import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
from sentence_transformers import SentenceTransformer


#Load APi KEY
api_key = os.environ.get("PINECONE_API_KEY")

#configure Pinecone client
pc = Pinecone(api_key=api_key)


cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)
index_name = 'regulatoryai' 
model_name="all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)
index = pc.Index(index_name)

def test_retrieval(query):
    """
    Input -> Recieve a query
    Return -> The Search result from pinecone

    Search for results simillar to query from retrieval

    """

   
    query_vector = model.encode(query).tolist()

    query_result = index.query(vector=query_vector, top_k=3, include_metadata=True)
    return query_result

query = input("Input Query")
print(test_retrieval(query))