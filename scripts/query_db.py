import chromadb
from sentence_transformers import SentenceTransformer

# Load the free local ChromaDB
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_collection(name="indian_property_laws")

# Query prompt
user_query = "What is the definition of transfer of property?"

print(f"🔎 Searching database for: '{user_query}'\n")

# Query top 2 most relevant legal chunks
results = collection.query(
    query_texts=[user_query],
    n_results=2
)

for idx, doc in enumerate(results['documents'][0]):
    print(f"--- MATCH {idx + 1} ---")
    print(doc.strip())
    print("\n")
