from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('shop.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=False)),
]
