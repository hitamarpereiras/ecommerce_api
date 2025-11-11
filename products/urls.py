from django.urls import path
from .views import list_products, ProdutoListView

urlpatterns = [
    #path('produtos/', list_products, name='produtos'),
    path('', ProdutoListView.as_view(), name='produtos'),
]