from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price_cents', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_cents', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'user__username', 'nombre', 'telefono')
    readonly_fields = ('created_at', 'total_cents')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Información del Pedido', {
            'fields': ('user', 'status', 'total_cents', 'created_at')
        }),
        ('Datos de Envío', {
            'fields': ('nombre', 'direccion', 'telefono')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_cents', 'subtotal')
    readonly_fields = ('subtotal',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price_cents', 'subtotal')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at',)
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price_cents', 'subtotal')
    readonly_fields = ('subtotal',)
