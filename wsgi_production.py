"""
WSGI config for bloodconnect project for PythonAnywhere
"""

import os
import sys

# Add your project directory to the sys.path
project_dir = '/home/yourusername/bloodconnect'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'bloodconnect.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
