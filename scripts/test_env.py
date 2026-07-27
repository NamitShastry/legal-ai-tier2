import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 40)
print(f"✅ Python Version running in cloud: {sys.version.split()[0]}")

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
pinecone_key = os.getenv("PINECONE_API_KEY")

if anthropic_key and anthropic_key != "your_anthropic_key_here":
    print("✅ Anthropic API key loaded successfully!")
else:
    print("⚠️  Anthropic API key is missing or set to default in .env")

if pinecone_key and pinecone_key != "your_pinecone_key_here":
    print("✅ Pinecone API key loaded successfully!")
else:
    print("⚠️  Pinecone API key is missing or set to default in .env")
print("=" * 40)