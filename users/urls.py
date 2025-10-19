from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPIView,
    LogoutAPIView,
    CurrentUserAPIView,
    ProfileAPIView,
    AddressViewSet,
    ChangePasswordAPIView
)

# Router para AddressViewSet
router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    # Autenticación
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    # Perfil del usuario actual
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('me/profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('me/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    # Direcciones (incluye me/addresses/)
    path('me/', include(router.urls)),
]
