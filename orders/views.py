from decimal import Decimal
from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = get_or_create_cart(self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = get_or_create_cart(self.request.user)
        product = serializer.validated_data["product"]
        price_cents = int(Decimal(product.price) * 100)
        serializer.save(cart=cart, price_cents=price_cents)


# ===============================
# ✅ ORDENES (ACTUALIZADO COMPLETO)
# ===============================
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        """
        Crea una orden desde el carrito y guarda los datos del cliente (nombre, dirección, teléfono)
        """
        user = request.user
        cart = get_or_create_cart(user)

        if not cart.items.exists():
            return Response({"detail": "Carrito vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # 📦 Obtener datos de envío del cuerpo del request
        nombre = request.data.get("nombre", "")
        direccion = request.data.get("direccion", "")
        telefono = request.data.get("telefono", "")

        # Crear la orden
        order = Order.objects.create(
            user=user,
            status="pending",
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
        )

        total = 0
        for ci in cart.items.select_related("product"):
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price_cents=ci.price_cents,
            )
            total += ci.quantity * ci.price_cents

        order.total_cents = total
        order.save()

        # Vaciar carrito
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="pay")
    def pay(self, request, pk=None):
        """
        Marcar una orden como pagada y actualizar stock.
        """
        order = self.get_object()
        if order.status != "pending":
            return Response({"detail": "La orden no está pendiente"}, status=status.HTTP_400_BAD_REQUEST)

        for item in order.items.select_related("product"):
            if item.quantity > item.product.stock:
                return Response({"detail": f"Sin stock para {item.product.name}"}, status=status.HTTP_400_BAD_REQUEST)

        for item in order.items.select_related("product"):
            item.product.stock -= item.quantity
            item.product.save()

        order.status = "paid"
        order.save()
        return Response(OrderSerializer(order).data)
