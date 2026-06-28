from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (DocumentListCreateView, DocumentDetailView, DocumentRetryIngestionView,LLMTestView, HealthCheckView,)
from .query_views import QueryView, QueryHistoryListView
 
urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("llm-test/", LLMTestView.as_view(), name="llm-test"),
    path("documents/", DocumentListCreateView.as_view(), name="document-list-create"),
    path("documents/<uuid:pk>/", DocumentDetailView.as_view(), name="document-detail"),
    path("documents/<uuid:pk>/retry/", DocumentRetryIngestionView.as_view(), name="document-retry",),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("query/", QueryView.as_view(), name="rag-query"),
    path("queries/", QueryHistoryListView.as_view(), name="query-history"),
]
