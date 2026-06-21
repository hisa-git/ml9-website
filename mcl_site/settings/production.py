from .base import *
import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# --------------------------------------------------
# BASIC
# --------------------------------------------------

DEBUG = False

# secret = os.environ.get("SECRET_KEY")
# if not secret:
#     raise ImproperlyConfigured("SECRET_KEY environment variable is required")
# SECRET_KEY = secret

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "temporary-build-secret"
)

# --------------------------------------------------
# CSRF / HTTPS
# --------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

if not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = [
        "https://ml9-website-production.up.railway.app",
        "https://mcl.mk.ua"
    ]

ALLOWED_HOSTS = [
    h.strip() 
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",") 
    if h.strip()
]

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = [
        "ml9-website-production.up.railway.app",
        "mcl.mk.ua",
        "www.mcl.mk.ua"
    ]

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # ← Important for Wagtail
CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True

# --------------------------------------------------
# WAGTAIL
# --------------------------------------------------

WAGTAILADMIN_BASE_URL = os.environ.get(
    "WAGTAILADMIN_BASE_URL",
    "https://ml9-website-production.up.railway.app"
)

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

LOG_DIR = os.environ.get("DJANGO_LOG_DIR", "/home/LogFiles")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 2,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "wagtail": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# --------------------------------------------------
# CACHING
# --------------------------------------------------

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache_table",
    }
}
