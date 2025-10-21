from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product


class ProductFlowTests(APITestCase):
    def test_list_products_public(self):
        Product.objects.create(name="A", description="d", stock=1, price=1000, material="gold", is_active=True)
        url = reverse("product-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.json()) >= 1)
