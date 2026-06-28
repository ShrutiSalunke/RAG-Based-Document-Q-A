from rest_framework import serializers
from .models import Document,QueryLog
 
 
class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ["id",  "original_filename", "file", "page_count", "status", "error_message",   "created_at", "updated_at", ]
        read_only_fields = ["id", "page_count", "status", "error_message", "created_at",  "updated_at","original_filename", ]
 
    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        validated_data["original_filename"] = uploaded_file.name
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class QueryRequestSerializer(serializers.Serializer):  
 
    question = serializers.CharField(min_length=3, max_length=2000, trim_whitespace=True)
    document_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        allow_empty=True,
        help_text=("Optional list of document IDs to restrict the search to. " "If omitted, all of the user's ready documents are searched " "(multi-document cross-query)." ),
    )
    top_k = serializers.IntegerField(required=False, min_value=1, max_value=20, default=5)
 
 
class QuerySourceSerializer(serializers.Serializer):
    document_id = serializers.CharField()
    document_name = serializers.CharField()
    page_number = serializers.IntegerField()
 
 
class QueryResponseSerializer(serializers.Serializer):    
 
    answer = serializers.CharField()
    answerable = serializers.BooleanField()
    sources = QuerySourceSerializer(many=True)
    retrieval_latency_ms = serializers.IntegerField()
    generation_latency_ms = serializers.IntegerField()
    query_log_id = serializers.CharField(allow_null=True)
 
 
class QueryLogSerializer(serializers.ModelSerializer):    
 
    class Meta:
        model = QueryLog
        fields = ["id", "question","answer", "retrieved_chunk_ids", "retrieval_latency_ms",  "generation_latency_ms", "created_at", ]
        read_only_fields = fields
