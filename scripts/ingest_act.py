import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

print("⚡ Loading free AI embedding model (this takes a few seconds)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize free local database
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_or_create_collection(name="indian_property_laws")

pdf_path = "data/raw/acts/transfer_of_property_act_1882.pdf"

print("📄 Reading PDF pages...")
chunks = []
with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

# Simple chunking by 500 characters
chunk_size = 500
raw_chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

print(f"📦 Created {len(raw_chunks)} text chunks from the Act.")

print("🧠 Indexing chunks into ChromaDB...")
documents = []
metadatas = []
ids = []

for idx, chunk in enumerate(raw_chunks):
    if len(chunk.strip()) > 50:  # Ignore tiny empty snippets
        documents.append(chunk)
        metadatas.append({"source": "Transfer of Property Act 1882", "chunk_id": idx})
        ids.append(f"topa_1882_{idx}")

# Embed and store in ChromaDB
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

print("=" * 40)
print(f"✅ SUCCESS! Embedded {len(documents)} legal chunks into your free ChromaDB!")
print("=" * 40)
