from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import ProductViewSet, CategoryViewSet
from orders.views import OrderViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# Router principal
router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    # Frontend (páginas HTML y vistas)
    path("", include("frontend.urls")),

    # Panel de administración
    path("admin/", admin.site.urls),

    # API REST principal
    path("api/", include(router.urls)),

    # Autenticación JWT
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Usuarios (registro, perfil, etc.)
    path("api/users/", include("users.urls")),
]

# Arch

