from django.db import models
from django.conf import settings  # ✅ importa esto
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ cambia aquí
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_cents = models.IntegerField(default=0)

    def subtotal(self):
        return self.quantity * self.price_cents

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

# -------------------------------
# ORDENES (actualizado)
# -------------------------------
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ cambia aquí también
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")
    total_cents = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def total(self):
        return self.total_cents / 100

    def __str__(self):
        return f"Orden #{self.id} de {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_cents = models.IntegerField(default=0)

    def subtotal(self):
        return self.quantity * self.price_cents

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

