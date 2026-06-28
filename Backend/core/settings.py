"""
Django settings for the RAG Document Query Engine — core project.
Phase 1: Environment configuration + Project scaffolding.
File location: backend/core/settings.py
"""
 
import os
from pathlib import Path
from datetime import timedelta
import environ
 
# ---------------------------------------------------------------------------
# Base paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
 
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
 
# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
 
# ---------------------------------------------------------------------------
# Installed apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
    "pgvector.django",
    "django_q",
    # Local apps
    "documents",
]
 
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
 
ROOT_URLCONF = "core.urls"
 
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
 
WSGI_APPLICATION = "core.wsgi.application"
 
# ---------------------------------------------------------------------------
# Database — Supabase PostgreSQL (pgvector pre-installed, free tier)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT", default="5432"),       
       
    }
}
 
# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
 
# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
 
# ---------------------------------------------------------------------------
# Static / media
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
 
# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
 
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}
 
SPECTACULAR_SETTINGS = {
    "TITLE": "RAG Document Query Engine API",
    "DESCRIPTION": "Major Project 21CSA699A — Shruti Salunke",
    "VERSION": "1.0.0",
}
 
# ---------------------------------------------------------------------------
# CORS (frontend runs on a different port during local dev)
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS", default=["http://localhost:5173"]
)
 
# ---------------------------------------------------------------------------
# OpenAI configuration (used from Phase 2 onward)
# ---------------------------------------------------------------------------
OPENAI_API_KEY = env("OPEN_AI_KEY", default="")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# ---------------------------------------------------------------------------
# Hugging Face Inference Providers (free tier) — replaces OpenAI
# ---------------------------------------------------------------------------
HF_TOKEN = env("HF_TOKEN", default="")
 
# ---------------------------------------------------------------------------
# django-q2 — async task queue, replaces Celery + Redis.
# Uses the existing PostgreSQL database (the "orm" broker) so no
# additional service needs to be installed or run.
# ---------------------------------------------------------------------------
Q_CLUSTER = {
    "name": "rag_document_engine",
    "workers": 2,
    "recycle": 500,
    "timeout": 300,       # max seconds a task may run before being killed
    "retry": 360,         # must be > timeout
    "queue_limit": 50,
    "bulk": 10,
    "orm": "default",     # use the default Django DB connection as broker
    "catch_up": False,
}
 

 
