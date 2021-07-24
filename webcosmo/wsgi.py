"""
WSGI config for webcosmo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/my.cosmolite.co.id/public_html/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcosmo.settings')

application = get_wsgi_application()
