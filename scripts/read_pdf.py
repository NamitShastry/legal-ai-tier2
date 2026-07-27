import os
import pdfplumber

pdf_path = "data/raw/acts/transfer_of_property_act_1882.pdf"

if os.path.exists(pdf_path):
    print("📄 Found legal file! Extracting text...")
    with pdfplumber.open(pdf_path) as pdf:
        first_few_pages = ""
        for i in range(min(3, len(pdf.pages))):
            extracted = pdf.pages[i].extract_text()
            if extracted:
                first_few_pages += extracted + "\n"
        
    print("=" * 40)
    print("PREVIEW OF EXTRACTED LEGAL TEXT:")
    print("=" * 40)
    print(first_few_pages[:500] + "...\n")
    print("✅ Success! Your free system can read official Indian legal PDFs.")
else:
    print(f"⚠️ Could not find {pdf_path}.")
    print("👉 Please download the PDF from indiacode.nic.in and drag it into data/raw/acts/")
