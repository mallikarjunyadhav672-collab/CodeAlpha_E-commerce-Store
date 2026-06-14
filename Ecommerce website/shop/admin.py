from django.contrib import admin
from .models import Product, Cart, CartItem, NewsletterEmail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'name', 'price', 'old_price', 'category', 'badge', 'rating', 'reviews')
    search_fields = ('name', 'brand', 'category')
    list_filter = ('category', 'badge')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'qty')
    search_fields = ('product__name',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'updated_at')
    search_fields = ('session_key',)


@admin.register(NewsletterEmail)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
