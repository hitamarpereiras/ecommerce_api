from django.urls import path
from .views import list_products

urlpatterns = [
    path('produtos/', list_products, name='produtos')
]