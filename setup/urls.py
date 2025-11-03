from products.views import produtos
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produtos/', produtos, name="produtos"),
]
