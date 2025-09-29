import os
from django.conf import settings
from django.http import HttpResponse, Http404

FRONTEND_DIR = os.path.join(settings.BASE_DIR, "frontend")

def serve_page(request, filename="index.html"):
    """
    Sirve un archivo HTML desde la carpeta frontend/
    Usage:
      /          -> index.html
      /shop.html -> shop.html
    """
    # Normalizar para seguridad: evitar rutas fuera de la carpeta frontend
    safe_name = os.path.normpath(filename)
    # No permitir subidas de ruta como ../../etc
    if safe_name.startswith("..") or os.path.isabs(safe_name):
        raise Http404("Archivo no válido")

    file_path = os.path.join(FRONTEND_DIR, safe_name)
    if not os.path.exists(file_path):
        raise Http404("Página no encontrada")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HttpResponse(content)
