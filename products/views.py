from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso: Lectura pública, escritura solo para admins"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_admin", False))


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint para categorías de productos

    GET /api/categories/ - Listar categorías activas
    GET /api/categories/{id}/ - Detalle de categoría
    POST /api/categories/ - Crear categoría (solo admin)
    PUT/PATCH /api/categories/{id}/ - Actualizar (solo admin)
    DELETE /api/categories/{id}/ - Eliminar (solo admin)
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        qs = Category.objects.all()
        user = self.request.user
        # Usuarios no-admin solo ven categorías activas
        if not (user and user.is_authenticated and getattr(user, "is_admin", False)):
            qs = qs.filter(is_active=True)
        return qs


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint para productos con filtros avanzados

    Filtros disponibles:
    - ?category=<id> - Filtrar por categoría
    - ?category_slug=<slug> - Filtrar por slug de categoría
    - ?price_min=<valor> - Precio mínimo
    - ?price_max=<valor> - Precio máximo
    - ?in_stock=true - Solo productos con stock
    - ?stock_min=<valor> - Stock mínimo
    - ?name=<texto> - Buscar por nombre
    - ?material=<texto> - Buscar por material
    - ?search=<texto> - Búsqueda general
    - ?ordering=price,-price,created_at,-created_at,stock,-stock,name,-name

    Ejemplos:
    - /api/products/?category_slug=anillos&price_max=5000000
    - /api/products/?in_stock=true&ordering=-price
    - /api/products/?search=oro&price_min=1000000
    """
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description", "material", "size"]
    ordering_fields = ["price", "created_at", "stock", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        # Lectura pública solo de activos; admins ven todos
        qs = Product.objects.select_related('category').prefetch_related('uploaded_images')
        user = self.request.user
        if not (user and user.is_authenticated and getattr(user, "is_admin", False)):
            qs = qs.filter(is_active=True)
        return qs
