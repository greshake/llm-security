from waitress import serve

from server import app

serve(app, listen='localhost:8080')