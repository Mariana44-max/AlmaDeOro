"""
Filtros personalizados para productos
"""
from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    """
    Filtros avanzados para productos:
    - Categoría
    - Rango de precio (min/max)
    - Stock disponible
    - Búsqueda por nombre, descripción, material
    """
    # Filtro por categoría
    category = filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_active=True),
        field_name='category'
    )
    category_slug = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact'
    )

    # Filtro por rango de precio
    price_min = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    price_max = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )

    # Filtro por stock
    in_stock = filters.BooleanFilter(
        field_name='stock',
        method='filter_in_stock'
    )
    stock_min = filters.NumberFilter(
        field_name='stock',
        lookup_expr='gte'
    )

    # Búsqueda por nombre
    name = filters.CharFilter(
        lookup_expr='icontains'
    )

    # Búsqueda por material
    material = filters.CharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = Product
        fields = {
            'is_active': ['exact'],
        }

    def filter_in_stock(self, queryset, name, value):
        """
        Filtra productos con stock disponible (> 0)
        """
        if value:
            return queryset.filter(stock__gt=0)
        return queryset
