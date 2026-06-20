from rest_framework import serializers
from .models import Document
 
 
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id",  "original_filename", "file", "page_count", "status", "error_message",   "created_at", "updated_at", ]
        read_only_fields = ["id", "page_count", "status", "error_message", "created_at",  "updated_at", ]
 
    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        validated_data["original_filename"] = uploaded_file.name
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
