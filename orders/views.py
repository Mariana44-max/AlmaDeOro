from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        items = request.data.get("items", [])
        if not items:
            return Response({"items": "Se requieren items."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, total_cents=0, currency="COP")
        total = 0

        for it in items:
            product_id = it.get("product")
            qty = int(it.get("quantity", 0))
            if qty <= 0:
                transaction.set_rollback(True)
                return Response({"quantity": "Debe ser > 0."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.select_for_update().get(pk=product_id, is_active=True)
            except Product.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"product": "Producto inválido."}, status=status.HTTP_400_BAD_REQUEST)

            if product.stock < qty:
                transaction.set_rollback(True)
                return Response({"stock": f"Stock insuficiente para {product.title}."}, status=status.HTTP_400_BAD_REQUEST)

            # precio y descuento se toman del servidor
            line_price = product.price_cents
            OrderItem.objects.create(order=order, product=product, quantity=qty, price_cents=line_price)

            product.stock -= qty
            product.save(update_fields=["stock"])

            total += line_price * qty

        order.total_cents = total
        order.save(update_fields=["total_cents"])

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
