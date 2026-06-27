import uuid
import pgvector.django
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
 
 
class Migration(migrations.Migration):
 
    dependencies = [
        ("documents", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
 
    operations = [
        # Drop the old 1536-dim HNSW index before changing column width.
        migrations.RemoveIndex(
            model_name="documentchunk",
            name="chunk_embedding_hnsw_idx",
        ),
        migrations.AlterField(
            model_name="documentchunk",
            name="embedding",
            field=pgvector.django.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AddIndex(
            model_name="documentchunk",
            index=pgvector.django.HnswIndex(
                ef_construction=64,
                fields=["embedding"],
                m=16,
                name="chunk_embedding_hnsw_idx",
                opclasses=["vector_cosine_ops"],
            ),
        ),
        migrations.CreateModel(
            name="QueryLog",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("question", models.TextField()),
                ("answer", models.TextField(blank=True, default="")),
                ("retrieved_chunk_ids", models.JSONField(blank=True, default=list)),
                ("retrieval_latency_ms", models.PositiveIntegerField(default=0)),
                ("generation_latency_ms", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="queries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
