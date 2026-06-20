from django.contrib import admin
from .models import Document, DocumentChunk
 
 
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("original_filename", "owner", "status", "page_count", "created_at")
    list_filter = ("status",)
    search_fields = ("original_filename",)

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("document", "chunk_index", "page_number", "token_count")
    list_filter = ("document",)

