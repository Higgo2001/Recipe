"""
WSGI config for djangoproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import sys
import os
from django.core.wsgi import get_wsgi_application

project_home = '/Users/higgo/PycharmProjects/djangoProject'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoProject.settings'

# These lines are important!
application = get_wsgi_application()

# Import Flask app
from flask_app import app as flask_app

# Define the combined WSGI application
class CombinedApplication:
    def __init__(self, django_app, flask_app):
        self.django_app = django_app
        self.flask_app = flask_app

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/flask'):
            return self.flask_app(environ, start_response)
        return self.django_app(environ, start_response)

application = CombinedApplication(application, flask_app)
