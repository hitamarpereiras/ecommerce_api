from django.urls import path
from .views import list_products, ProdutoListView
from .views import ProdutoCreateView

urlpatterns = [
    #path('produtos/', list_products, name='produtos'),
    path('', ProdutoListView.as_view(), name='produtos'),
    path("criar/", ProdutoCreateView.as_view(), name="criar_produto"),
]