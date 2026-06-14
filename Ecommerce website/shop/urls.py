from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_list, name='shop_list'),
    path('collections/', views.collections, name='collections'),
    path('about/', views.about, name='about'),
    path('api/newsletter/', views.newsletter_api, name='newsletter_api'),
    path('api/products/', views.products_api, name='products_api'),
    path('api/cart/', views.cart_api, name='cart_api'),
    path('api/wishlist/', views.wishlist_api, name='wishlist_api'),
]
