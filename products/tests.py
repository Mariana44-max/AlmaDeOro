from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from products.models import Product, Category

User = get_user_model()


class ProductFlowTests(APITestCase):
    def test_list_products_public(self):
        Product.objects.create(name="A", description="d", stock=1, price=1000, material="gold", is_active=True)
        url = reverse("product-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.json()) >= 1)


# ===== TESTS COMPLETOS AGREGADOS =====

class CategoryModelTest(TestCase):
    """Tests para el modelo Category"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Anillos Test",
            slug="anillos-test",
            description="Categoría de prueba",
            is_active=True
        )

    def test_category_creation(self):
        """Test creación de categoría"""
        self.assertEqual(self.category.name, "Anillos Test")
        self.assertEqual(str(self.category), "Anillos Test")

    def test_category_is_active(self):
        """Test que la categoría está activa por defecto"""
        self.assertTrue(self.category.is_active)


class ProductModelTest(TestCase):
    """Tests para el modelo Product"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Collares",
            slug="collares"
        )
        self.product = Product.objects.create(
            name="Collar de Oro",
            description="Hermoso collar",
            category=self.category,
            price="200000",
            stock=10,
            material="Oro 18k",
            weight="5.5",
            size="50cm",
            is_active=True
        )

    def test_product_creation(self):
        """Test creación de producto"""
        self.assertEqual(self.product.name, "Collar de Oro")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(str(self.product), "Collar de Oro")

    def test_product_price(self):
        """Test que el precio se guarda correctamente"""
        self.assertEqual(float(self.product.price), 200000.0)

    def test_product_stock(self):
        """Test que el stock se guarda correctamente"""
        self.assertEqual(self.product.stock, 10)


class ProductFilterAPITest(APITestCase):
    """Tests para filtros de la API de productos"""

    def setUp(self):
        self.category = Category.objects.create(
            name="Pulseras",
            slug="pulseras"
        )
        self.product1 = Product.objects.create(
            name="Pulsera Oro",
            category=self.category,
            price="150000",
            stock=5
        )
        self.product2 = Product.objects.create(
            name="Pulsera Plata",
            category=self.category,
            price="80000",
            stock=10
        )

    def test_filter_by_category_slug(self):
        """Test filtrar por slug de categoría"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?category_slug=pulseras')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_price_max(self):
        """Test filtrar por precio máximo"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?price_max=100000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Solo debe retornar productos con precio <= 100000
        for product in response.data:
            self.assertLessEqual(float(product['price']), 100000)

    def test_filter_by_price_min(self):
        """Test filtrar por precio mínimo"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?price_min=100000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Solo debe retornar productos con precio >= 100000
        for product in response.data:
            self.assertGreaterEqual(float(product['price']), 100000)

    def test_ordering_by_price_asc(self):
        """Test ordenar por precio ascendente"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?ordering=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(p['price']) for p in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_ordering_by_price_desc(self):
        """Test ordenar por precio descendente"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?ordering=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(p['price']) for p in response.data]
        self.assertEqual(prices, sorted(prices, reverse=True))

    def test_search_products(self):
        """Test búsqueda de productos"""
        url = reverse("product-list")
        response = self.client.get(f'{url}?search=Oro')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que todos los resultados contienen "Oro"
        for product in response.data:
            self.assertIn('Oro', product['name'])

    def test_filter_in_stock(self):
        """Test filtrar productos con stock"""
        # Crear producto sin stock
        Product.objects.create(
            name="Pulsera Sin Stock",
            category=self.category,
            price="100000",
            stock=0
        )
        url = reverse("product-list")
        response = self.client.get(f'{url}?in_stock=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que todos tienen stock > 0
        for product in response.data:
            self.assertGreater(product['stock'], 0)


class CategoryAPITest(APITestCase):
    """Tests para la API de categorías"""

    def setUp(self):
        Category.objects.create(name="Anillos", slug="anillos", is_active=True)
        Category.objects.create(name="Collares", slug="collares", is_active=True)

    def test_list_categories(self):
        """Test listar categorías"""
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_category_detail(self):
        """Test obtener detalle de categoría"""
        category = Category.objects.first()
        url = reverse("category-detail", kwargs={'pk': category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], category.name)
