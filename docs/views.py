from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views.static import serve
import os

def serve_docs(request, path):
    if path == "oplosser":
        return redirect("oplosser")
    
    docs_path = os.path.join(settings.DOCS_DIR, path)

    if os.path.isdir(docs_path):
        path = os.path.join(path, 'index.html')

    path = os.path.join(settings.DOCS_DIR, path)
    relative_path = os.path.relpath(path, settings.DOCS_DIR)

    return serve(request, relative_path, settings.DOCS_DIR)


def serve_home(request):
    return serve_docs(request, 'index.html')
