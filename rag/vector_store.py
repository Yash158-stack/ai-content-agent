import chromadb
from chromadb.config import Settings

# create client (local DB)
client = chromadb.Client(Settings(persist_directory="./chroma_db"))

# create collection
collection = client.get_or_create_collection(name="content")


def store_data(text: str, embedding):
    if is_duplicate(embedding):
        print("Duplicate content detected. Skipping storage.")
        return

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )
    print("Stored new content.")

def retrieve_data(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0] if results["documents"] else []

def is_duplicate(query_embedding, threshold=0.90):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )
    if results["distances"] and results["distances"][0]:
        distance = results["distances"][0][0]

        # lower distance = more similar
        similarity = 1 - distance

        return similarity > threshold
    return False