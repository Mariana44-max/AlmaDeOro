from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    uploaded_images = ProductImageSerializer(many=True, read_only=True)
    images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'weight', 'stock',
            'price', 'size', 'material', 'is_active',
            'uploaded_images', 'images'
        ]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)
        for img in images:
            ProductImage.objects.create(product=product, image=img)
        return product
