"""
Development settings for the project.

These settings extend the base settings and add development-specific settings.
"""

import socket

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ["*"]

# CORS settings - allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Debug toolbar settings
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # noqa: F405

# Add debug toolbar middleware
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

# Configure internal IPs for debug toolbar
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Disable password validation in development
AUTH_PASSWORD_VALIDATORS = []

# Django Extensions settings
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_IMPORTS = [
    "from django.core.cache import cache",
    "from django.conf import settings",
    "from django.contrib.auth import get_user_model",
    "from django.db import transaction",
    "from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When",
    "from django.utils import timezone",
]

# Logging
LOGGING["loggers"]["django"]["level"] = "INFO"  # noqa: F405
LOGGING["loggers"]["apps"]["level"] = "DEBUG"  # noqa: F405
