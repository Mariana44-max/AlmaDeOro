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
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # Autenticación JWT
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Endpoints de usuarios (registro, perfil, direcciones, cambio de contraseña, etc.)
    path("api/users/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
