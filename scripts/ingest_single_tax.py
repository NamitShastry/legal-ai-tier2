import os
import chromadb
from pypdf import PdfReader

print("⚡ Connecting to ChromaDB...")
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_or_create_collection(name="indian_property_laws")

pdf_path = "data/raw/acts/income_tax_property_provisions.pdf"

if not os.path.exists(pdf_path):
    print(f"❌ Error: Could not find '{pdf_path}'")
else:
    print(f"📖 Reading {pdf_path} (Memory-Optimized Stream)...")
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    print(f"📄 Total Pages: {total_pages}")

    act_title = "Income Tax Act, 1961 (Property & Rent Provisions)"
    batch_docs, batch_metas, batch_ids = [], [], []
    chunk_counter = 0

    # Stream page by page to keep RAM usage low
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        
        # Chunk text in 500-character blocks
        chunk_size = 500
        raw_chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        for chunk in raw_chunks:
            if len(chunk.strip()) > 50:
                batch_docs.append(chunk)
                batch_metas.append({"act": act_title, "file_name": "income_tax_property_provisions.pdf"})
                batch_ids.append(f"income_tax_{chunk_counter}")
                chunk_counter += 1

        # Commit to ChromaDB in batches of 200 chunks to flush RAM
        if len(batch_docs) >= 200:
            collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)
            print(f"   💾 Ingested {chunk_counter} chunks (Page {page_num+1}/{total_pages})...")
            batch_docs, batch_metas, batch_ids = [], [], []

    # Commit any remaining chunks
    if batch_docs:
        collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)

    print("=" * 60)
    print(f"✅ SUCCESS! Ingested all {chunk_counter} chunks from {act_title} into ChromaDB!")
    print("=" * 60)