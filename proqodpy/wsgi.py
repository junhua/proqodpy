"""
WSGI config for proqodpy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proqodpy.settings")

application = get_wsgi_application()

'''
gunicorn --name=proqodpy \
    --pythonpath=proqodpy \
    --bind=127.0.0.1:9000 \
    --config /etc/gunicorn.d/gunicorn.py \
    proqodpy.wsgi:application
'''