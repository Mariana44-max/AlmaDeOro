from django.urls import re_path
from django.views.static import serve as static_serve
from django.conf import settings
import os
from . import views

FRONTEND_DIR = os.path.join(settings.BASE_DIR, "frontend")

urlpatterns = [
    # Ruta raíz -> index.html
    re_path(r"^$", views.serve_page, name="index"),

    # Rutas directas a HTML como /shop.html o /detail.html
    re_path(r"^(?P<filename>[^/]+\.html)$", views.serve_page, name="serve_html"),

    # Servir archivos estáticos (css/js/img/...). Esto es SOLO para desarrollo.
    # Patrón para cualquier archivo estático en la carpeta frontend/
    re_path(r"^(?P<path>.*\.(?:css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf))$",
            static_serve,
            {"document_root": FRONTEND_DIR}),
]
