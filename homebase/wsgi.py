"""
WSGI config for homebase project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import sys

#add the hellodjango project path into the sys.path
sys.path.append('/home/ubuntu/homebase')

#add the virtualenv site-packages path to the sys.path 
sys.path.append('/home/ubuntu/homebase/venv/lib/python3.12/site-packages/') 

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homebase.settings')

application = get_wsgi_application()
