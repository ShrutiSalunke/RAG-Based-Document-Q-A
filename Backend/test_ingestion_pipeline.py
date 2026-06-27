import sys
import django
import os
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
 
from documents.ingestion.pdf_parser import extract_pages, get_page_count
from documents.ingestion.chunker import chunk_pages
from documents.ingestion.embeddings import embed_texts
 
 
def main():
    if len(sys.argv) != 2:
        print("Usage: python test_ingestion_pipeline.py <path-to-pdf>")
        sys.exit(1)
 
    pdf_path = sys.argv[1]
 
    print(f"Step 1: Parsing PDF -> {pdf_path}")
    page_count = get_page_count(pdf_path)
    pages = extract_pages(pdf_path)
    print(f"  Total pages: {page_count}")
    print(f"  Pages with extractable text: {len(pages)}")
 
    print("\nStep 2: Chunking text")
    chunks = chunk_pages(pages)
    print(f"  Total chunks created: {len(chunks)}")
    if chunks:
        print(f"  Example chunk (page {chunks[0].page_number}, "
              f"{chunks[0].token_count} tokens):")
        print(f"  \"{chunks[0].content[:200]}...\"")
 
    print("\nStep 3: Generating embeddings via Hugging Face API")
    print("  (calls Hugging Face's free API -- requires internet and HF_TOKEN)")
    texts = [c.content for c in chunks[:5]]  # test on first 5 chunks only
    vectors = embed_texts(texts)
    print(f"  Generated {len(vectors)} embeddings")
    print(f"  Embedding dimension: {len(vectors[0])}")
    print(f"  First 5 values of first embedding: {vectors[0][:5]}")
 
    print("\nAll pipeline stages PASSED.")
 
 
if __name__ == "__main__":
    main()
