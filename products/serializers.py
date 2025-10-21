from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    # Lectura: lista de imágenes existentes
    images = ProductImageSerializer(many=True, read_only=True)

    # Escritura: múltiples imágenes en creación/actualización
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=10_000_000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=True,   # requerido en POST (lo controlamos en validate)
        help_text="Send one or more images using the same key."
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name", "description", "weight", "stock", "price", "size", "material",
            "is_active",
            "images",          # read-only
            "uploaded_images", # write-only
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "images", "created_at", "updated_at"]

    def validate(self, attrs):
        # En POST, uploaded_images es obligatorio; en PUT/PATCH lo hacemos opcional
        request = self.context.get("request")
        method = getattr(request, "method", "").upper() if request else ""
        if method == "POST" and (not attrs.get("uploaded_images")):
            raise serializers.ValidationError({"uploaded_images": "At least one image is required."})
        return attrs

    def create(self, validated_data):
        images_data = validated_data.pop("uploaded_images", [])
        product = Product.objects.create(**validated_data)
        for img in images_data:
            ProductImage.objects.create(product=product, image=img)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop("uploaded_images", None)

        # Actualiza campos del producto
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        # Si mandan imágenes en PUT/PATCH, reemplazamos todas las anteriores
        if images_data is not None:
            instance.images.all().delete()
            for img in images_data:
                ProductImage.objects.create(product=instance, image=img)

        return instance
