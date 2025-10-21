from django.db import models


class Product(models.Model):
    # Obligatorios
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField(help_text="Price in COP (pesos)")

    # Opcionales
    weight = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, help_text="Weight in grams")
    size = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"
