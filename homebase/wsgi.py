"""
WSGI config for homebase project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import sys
from django.utils.regex_helper import _lazy_re_compile
import django.http.request

django.http.request.host_validation_re = _lazy_re_compile(r"[a-zA-z0-9.:]*")

# add the hellodjango project path into the sys.path
sys.path.append("/home/ubuntu/homebase")

# add the virtualenv site-packages path to the sys.path
sys.path.append("/home/ubuntu/homebase/venv/lib/python3.12/site-packages/")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "homebase.settings")

application = get_wsgi_application()