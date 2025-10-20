from django.urls import path, re_path
from django.views.static import serve as static_serve
from django.conf import settings
import os
from . import views

FRONTEND_DIR = os.path.join(settings.BASE_DIR, "frontend")

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    re_path(r"^$", views.serve_page, name="index"),
    re_path(r"^(?P<filename>[^/]+\.html)$", views.serve_page, name="serve_html"),
    re_path(r"^(?P<path>.*\.(?:css|js|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf))$",
            static_serve, {"document_root": FRONTEND_DIR}),
]

