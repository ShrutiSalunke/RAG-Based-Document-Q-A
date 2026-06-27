from django_q.tasks import async_task
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
 
from .models import Document
from .serializers import DocumentSerializer
from .tasks import ingest_document_task
 
 
class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
 
    def perform_create(self, serializer):
        document = serializer.save()       
        async_task(ingest_document_task, str(document.id))
        return document
 
 
class DocumentDetailView(generics.RetrieveDestroyAPIView):    
 
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user) 
 
class DocumentRetryIngestionView(APIView):   
 
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request, pk):
        try:
            document = Document.objects.get(id=pk, owner=request.user)
        except Document.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
 
        document.status = Document.STATUS_PENDING
        document.error_message = ""
        document.save(update_fields=["status", "error_message", "updated_at"])
 
        async_task(ingest_document_task, str(document.id))
 
        return Response(DocumentSerializer(document).data, status=status.HTTP_202_ACCEPTED)
 
 
class LLMTestView(APIView): 
 
    permission_classes = [permissions.IsAuthenticated]
 
    def get(self, request):
        from .llm_client import generate_answer 
        try:
            answer = generate_answer( system_prompt="You are a concise assistant.", user_prompt="Reply with exactly: Hugging Face connection OK.",max_tokens=20, )
        except Exception as exc:  # noqa: BLE001
            return Response( {"detail": f"LLM call failed: {exc}"},status=status.HTTP_502_BAD_GATEWAY,)
 
        return Response({"model_response": answer}, status=status.HTTP_200_OK)
 
class HealthCheckView(APIView):   
 
    permission_classes = [permissions.AllowAny]
 
    def get(self, request):
        from django.db import connection
 
        with connection.cursor() as cursor:
            cursor.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector';")
            row = cursor.fetchone()
            pgvector_version = row[0] if row else None
 
        return Response({ "status": "ok", "database": "connected", "pgvector_extension": pgvector_version or "NOT INSTALLED", }, status=status.HTTP_200_OK, )
 
