from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import ProductViewSet
from orders.views import OrderViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# Rutas principales de la API
router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    # Frontend (páginas HTML)
    path("", include("frontend.urls")),

    # Panel de administración
    path("admin/", admin.site.urls),

    # API principal
    path("api/", include(router.urls)),

    # Autenticación JWT
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Usuarios (registro, perfil, etc.)
    path("api/users/", include("users.urls")),
]

# Archivos multimedia (imágenes subidas, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


