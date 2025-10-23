from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

route = routers.DefaultRouter()

from products.api import viewsets as productsviewset

route.register(r"products", productsviewset.ProductViews, basename='Products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(route.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
