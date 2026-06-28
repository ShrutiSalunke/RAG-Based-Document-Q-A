
import logging
from dataclasses import dataclass
 
from django.contrib.auth.models import AbstractBaseUser
from pgvector.django import CosineDistance
 
from documents.ingestion.embeddings import embed_query
from documents.models import Document, DocumentChunk
 
logger = logging.getLogger(__name__)
 
DEFAULT_TOP_K = 5
NO_MATCH_DISTANCE_THRESHOLD = 0.6
 
 
@dataclass
class RetrievedChunk:
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    content: str
    distance: float
 
 
def retrieve_relevant_chunks(question: str, owner: AbstractBaseUser, document_ids: list[str] | None = None, top_k: int = DEFAULT_TOP_K,) -> list[RetrievedChunk]:
    
    query_vector = embed_query(question) 
    queryset = DocumentChunk.objects.filter(document__owner=owner, document__status=Document.STATUS_READY, )
 
    if document_ids:
        queryset = queryset.filter(document_id__in=document_ids)
 
    queryset = (queryset.annotate(distance=CosineDistance("embedding", query_vector)).order_by("distance").select_related("document")[:top_k] )
 
    results = [
        RetrievedChunk(chunk_id=str(chunk.id), document_id=str(chunk.document_id), document_name=chunk.document.original_filename, page_number=chunk.page_number,content=chunk.content,distance=float(chunk.distance), )
        for chunk in queryset
    ]
 
    if results:
        logger.info("Retrieved %s chunks for query, best distance=%.4f, worst distance=%.4f", len(results),  results[0].distance, results[-1].distance,  )
    else:
        logger.info("Retrieved 0 chunks for query (no ready documents matched filters).")
 
    return results
 
 
def has_relevant_match(chunks: list[RetrievedChunk]) -> bool:
    
    if not chunks:
        return False
    return chunks[0].distance <= NO_MATCH_DISTANCE_THRESHOLD
