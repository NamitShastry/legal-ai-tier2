import os
import chromadb
from pypdf import PdfReader

print("⚡ Connecting to ChromaDB...")
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_or_create_collection(name="indian_property_laws")

pdf_path = "data/raw/up_noida/up_apartment_act_2010.pdf"

if not os.path.exists(pdf_path):
    print(f"❌ Error: Could not find '{pdf_path}'")
else:
    print(f"📖 Reading {pdf_path}...")
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    act_title = "Uttar Pradesh Apartment Act, 2010"
    batch_docs, batch_metas, batch_ids = [], [], []
    chunk_counter = 0

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        
        chunk_size = 500
        raw_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        for chunk in raw_chunks:
            if len(chunk.strip()) > 50:
                batch_docs.append(chunk)
                batch_metas.append({
                    "act": act_title, 
                    "state": "Uttar Pradesh",
                    "region": "Noida / Greater Noida",
                    "file_name": "up_apartment_act_2010.pdf"
                })
                batch_ids.append(f"up_apt_{chunk_counter}")
                chunk_counter += 1

        if len(batch_docs) >= 200:
            collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)
            batch_docs, batch_metas, batch_ids = [], [], []

    if batch_docs:
        collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)

    print("=" * 60)
    print(f"✅ SUCCESS! Ingested {chunk_counter} chunks from {act_title} into ChromaDB!")
    print("=" * 60)
