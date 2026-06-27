import logging
 
from django.db import transaction
 
from .models import Document, DocumentChunk
from .ingestion.pdf_parser import extract_pages, get_page_count
from .ingestion.chunker import chunk_pages
from .ingestion.embeddings import embed_texts
 
logger = logging.getLogger(__name__)
 
 
def ingest_document_task(document_id: str) -> None:
   
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.error("ingest_document_task: Document %s not found", document_id)
        return
 
    document.status = Document.STATUS_PROCESSING
    document.save(update_fields=["status", "updated_at"])
 
    try:
        file_path = document.file.path
 
        page_count = get_page_count(file_path)
        pages = extract_pages(file_path)
        chunks = chunk_pages(pages)
 
        if not chunks:
            raise ValueError("Document produced zero chunks after parsing.")
 
        texts = [c.content for c in chunks]
        vectors = embed_texts(texts)
 
        chunk_objects = [
            DocumentChunk(document=document, chunk_index=index, page_number=chunk.page_number, content=chunk.content, token_count=chunk.token_count,embedding=vector, )
            for index, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
 
        with transaction.atomic():
            # Clear any partial/previous chunks (e.g. on re-ingestion)
            DocumentChunk.objects.filter(document=document).delete()
            DocumentChunk.objects.bulk_create(chunk_objects, batch_size=100)
 
            document.page_count = page_count
            document.status = Document.STATUS_READY
            document.error_message = ""
            document.save(update_fields=["page_count", "status", "error_message", "updated_at"])
 
        logger.info("Ingested document %s: %s pages, %s chunks",document_id, page_count, len(chunk_objects),)
 
    except Exception as exc:  
        logger.exception("Ingestion failed for document %s", document_id)
        document.status = Document.STATUS_FAILED
        document.error_message = str(exc)[:2000]
        document.save(update_fields=["status", "error_message", "updated_at"])
