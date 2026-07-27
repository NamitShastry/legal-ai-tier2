import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

print("⚡ Connecting to ChromaDB...")
model = SentenceTransformer("all-MiniLM-L6-v2")
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_or_create_collection(name="indian_property_laws")

pdf_path = "data/raw/acts/indian_contract_act_1872.pdf"

if not os.path.exists(pdf_path):
    print(f"❌ Error: Could not find '{pdf_path}'. Please check the filename and folder!")
else:
    print(f"📖 Reading {pdf_path}...")
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    chunk_size = 500
    raw_chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    
    documents, metadatas, ids = [], [], []
    act_title = "Indian Contract Act, 1872"

    for idx, chunk in enumerate(raw_chunks):
        if len(chunk.strip()) > 50:
            documents.append(chunk)
            metadatas.append({"act": act_title, "file_name": "indian_contract_act_1872.pdf"})
            ids.append(f"contract_act_{idx}")

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print("=" * 40)
    print(f"✅ SUCCESS! Added {len(documents)} chunks from {act_title} into ChromaDB!")
    print("=" * 40)
