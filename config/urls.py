from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),

    # Users
    path("api/users/", include("users.urls")),

    # Auth (JWT)
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Products
    path("api/", include("products.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
