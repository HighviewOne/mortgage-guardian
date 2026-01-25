# WSGI entry point for PythonAnywhere
import sys
import os

# Add the backend directory to the path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from app.main import app

# PythonAnywhere uses 'application' as the WSGI callable
application = app
