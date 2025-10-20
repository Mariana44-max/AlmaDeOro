from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from products.views import ProductViewSet
from orders.views import OrderViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    # Frontend (páginas HTML y vistas)
    path("", include("frontend.urls")),

    # Panel de administración
    path("admin/", admin.site.urls),

    # API REST principal
    path("api/", include(router.urls)),

    # JWT Authentication
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

<<<<<<< HEAD
    # Users
=======
    # Usuarios (registro, perfil, etc.)
>>>>>>> 9e932d96640bc58a748f37b7a65ec76d81fb4468
    path("api/users/", include("users.urls")),
]

# Arch

