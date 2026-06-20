from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentSerializer


class DocumentListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/documents/   -> list the current user's documents
    POST /api/v1/documents/   -> upload a new PDF document
    """ 
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
 
    def perform_create(self, serializer):
        document = serializer.save()
        # TODO (Phase 2): enqueue Celery task here, e.g.
        # ingest_document_task.delay(str(document.id))
        return document
    

class DocumentDetailView(generics.RetrieveDestroyAPIView):    
 
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

class HealthCheckView(APIView):
    """
    GET /api/v1/health/  -> simple liveness probe used to confirm the
    backend, database connection, and pgvector extension are reachable.
    """
 
    permission_classes = [permissions.AllowAny]
 
    def get(self, request):
        from django.db import connection
 
        with connection.cursor() as cursor:
            cursor.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
            row = cursor.fetchone()
            pgvector_version = row[0] if row else None
 
        return Response( { "status": "ok",  "database": "connected",  "pgvector_extension": pgvector_version or "NOT INSTALLED",   }, status=status.HTTP_200_OK, )
 
