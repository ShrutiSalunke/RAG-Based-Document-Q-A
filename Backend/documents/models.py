import uuid
from django.conf import settings
from django.db import models
from pgvector.django import VectorField, HnswIndex
 
EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output size
 
 
class Document(models.Model):
    """A single uploaded PDF document belonging to a user."""
 
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_READY = "ready"
    STATUS_FAILED = "failed"
 
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_READY, "Ready"),
        (STATUS_FAILED, "Failed"),
    ]
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    original_filename = models.CharField(max_length=512)
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    page_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"{self.original_filename} ({self.status})"
 
 
class DocumentChunk(models.Model):
    """
    A token-bounded, overlapping text chunk extracted from a Document,
    along with its 384-dimensional embedding generated via the free
    Hugging Face Inference API (sentence-transformers/all-MiniLM-L6-v2).
    Populated by the
    ingestion pipeline (Phase 2: PDF parsing -> chunking -> embedding).
    """
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks"
    )
    chunk_index = models.PositiveIntegerField()
    page_number = models.PositiveIntegerField()
    content = models.TextField()
    token_count = models.PositiveIntegerField(default=0)
    embedding = VectorField(dimensions=EMBEDDING_DIM, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["document_id", "chunk_index"]
        indexes = [
            HnswIndex(
                name="chunk_embedding_hnsw_idx",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]
 
    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.original_filename}"
 
 
class QueryLog(models.Model):
    """
    Records every RAG query for auditability and the performance
    benchmarking deliverable described in the proposal. Populated by
    the query endpoint built in Phase 3.
    """
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="queries"
    )
    question = models.TextField()
    answer = models.TextField(blank=True, default="")
    retrieved_chunk_ids = models.JSONField(default=list, blank=True)
    retrieval_latency_ms = models.PositiveIntegerField(default=0)
    generation_latency_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"Query by {self.user} at {self.created_at:%Y-%m-%d %H:%M}"
 
