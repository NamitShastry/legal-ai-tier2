import os
import chromadb
import pytesseract
from pdf2image import convert_from_path

print("⚡ Connecting to ChromaDB...")
db_client = chromadb.PersistentClient(path="data/processed/chroma_db")
collection = db_client.get_or_create_collection(name="indian_property_laws")

pdf_path = "data/raw/up_noida/up_stamp_registration_rules.pdf"

if not os.path.exists(pdf_path):
    print(f"❌ Error: Could not find '{pdf_path}'")
else:
    print(f"📖 Running OCR on scanned PDF: {pdf_path}...")
    act_title = "UP Stamp Registration Rules & Noida Circle Rates"
    batch_docs, batch_metas, batch_ids = [], [], []
    chunk_counter = 0

    # Convert PDF to images page by page to save RAM
    pages = convert_from_path(pdf_path, dpi=150)
    total_pages = len(pages)
    print(f"📄 Total Scanned Pages to OCR: {total_pages}")

    for page_num, image in enumerate(pages):
        text = pytesseract.image_to_string(image)
        if not text or len(text.strip()) < 10:
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
                    "file_name": "up_stamp_registration_rules.pdf"
                })
                batch_ids.append(f"up_stamp_{chunk_counter}")
                chunk_counter += 1

        if len(batch_docs) >= 100:
            collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)
            print(f"   💾 Ingested {chunk_counter} OCR chunks (Page {page_num+1}/{total_pages})...")
            batch_docs, batch_metas, batch_ids = [], [], []

    if batch_docs:
        collection.add(documents=batch_docs, ids=batch_ids, metadatas=batch_metas)

    print("=" * 60)
    print(f"✅ SUCCESS! Ingested {chunk_counter} OCR chunks from {act_title} into ChromaDB!")
    print("=" * 60)
