import os
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

FRONTEND_DIR = os.path.join(settings.BASE_DIR, "frontend")

def serve_page(request, filename="index.html"):
    safe_name = os.path.normpath(filename)
    if safe_name.startswith("..") or os.path.isabs(safe_name):
        raise Http404("Archivo no válido")
    return render(request, filename)



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("login")
    return render(request, "sesion.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return redirect("register")
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("index")

