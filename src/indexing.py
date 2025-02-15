import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
import time
from tqdm.auto import tqdm
import json



#Load APi KEY
api_key = os.environ.get("PINECONE_API_KEY")

#Load Documents
input_path = os.path.join("documents", "content_section_embeddings.json")

#configure Pinecone client
pc = Pinecone(api_key=api_key)


cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)


index_name = 'regulatoryai' #Name Index


#Check for name availability
existing_indexes = [
    index_info["name"] for index_info in pc.list_indexes()
]

if index_name not in existing_indexes:
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=384, 
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# connect to index
index = pc.Index(index_name)
time.sleep(1)

# view index stats
print(index.describe_index_stats())

def upsert_data():
    """
    Upsert data to pinecone cloud

    """
    with open(input_path, 'r', encoding='utf-8') as file:
        documents = json.load(file)  

    vectors = []
    for doc in tqdm(documents, total=len(documents)):
        vector_id = str(doc["Id"]) 
        embedding = doc["Embedding"]  
        metadata = {
            "Section": doc["Section"],
            "Content": doc["Content"]
        }

        vectors.append((vector_id, embedding, metadata))

    
    for i in range(0, len(vectors)):
        index.upsert(vectors[i:i])

    print("Upsert complete.")

#upsert_data()
print(index.describe_index_stats())
