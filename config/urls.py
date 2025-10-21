from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from users.views import AddressViewSet  # ✅ puedes agregar otros ViewSets si existen
from products.views import ProductViewSet  # opcional si ya tienes
# ⚠️ No olvides importar tus ViewSets

router = routers.DefaultRouter()

# ✅ Aquí registras el ViewSet que faltaba (si luego haces un UserViewSet, también va aquí)
router.register(r"addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),

    # Incluye el router principal (para ViewSets)
    path("api/", include(router.urls)),

    # Users
    path("api/users/", include("users.urls")),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Products
    path("api/", include("products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
