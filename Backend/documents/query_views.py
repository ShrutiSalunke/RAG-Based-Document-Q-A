from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView 
from .models import QueryLog
from .rag.query_engine import run_query
from .serializers import (QueryLogSerializer, QueryRequestSerializer,QueryResponseSerializer,)
from drf_spectacular.utils import extend_schema
 
@extend_schema(request=QueryRequestSerializer, responses=QueryResponseSerializer)
class QueryView(APIView):    
 
    permission_classes = [permissions.IsAuthenticated]
 
    def post(self, request):
        request_serializer = QueryRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated = request_serializer.validated_data
 
        document_ids = (
            [str(doc_id) for doc_id in validated["document_ids"]]
            if "document_ids" in validated
            else None
        )
 
        result = run_query(question=validated["question"], user=request.user, document_ids=document_ids, top_k=validated.get("top_k", 5), )
 
        response_serializer = QueryResponseSerializer(
            {
                "answer": result.answer,
                "answerable": result.answerable,
                "sources": [
                    {
                        "document_id": s.document_id,
                        "document_name": s.document_name,
                        "page_number": s.page_number,
                    }
                    for s in result.sources
                ],
                "retrieval_latency_ms": result.retrieval_latency_ms,
                "generation_latency_ms": result.generation_latency_ms,
                "query_log_id": result.query_log_id,
            }
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
 
 
class QueryHistoryListView(generics.ListAPIView):   
 
    serializer_class = QueryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        return QueryLog.objects.filter(user=self.request.user)
 
