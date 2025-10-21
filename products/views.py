from rest_framework import viewsets, permissions, filters
from .models import Product
from .serializers import ProductSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_admin", False))


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "material", "size"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        # Lectura pública solo de activos; admins ven todos
        qs = Product.objects.all().order_by("-created_at")
        user = self.request.user
        if not (user and user.is_authenticated and getattr(user, "is_admin", False)):
            qs = qs.filter(is_active=True)
        return qs
