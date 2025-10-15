"""
WSGI config for monitoring project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics.settings")

application = get_wsgi_application()

# For high concurrency, prefer ASGI deployment with uvicorn/daphne.
# See asgi.py if present.
