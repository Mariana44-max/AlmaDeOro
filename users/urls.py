from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPIView,
    LogoutAPIView,
    CurrentUserAPIView,
    ProfileAPIView,
    AddressViewSet,
    ChangePasswordAPIView,
    UserViewSet,  # ✅ Agregado
)

# Router general
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')  # ✅ /api/users/
router.register(r'me/addresses', AddressViewSet, basename='address')  # /api/users/me/addresses/

urlpatterns = [
    # 🔐 Autenticación
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    # 👤 Información y perfil del usuario actual
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('me/profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('me/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    # 🚀 Incluye las rutas del router
    path('', include(router.urls)),
]
