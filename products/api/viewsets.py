from rest_framework import viewsets
from products.api import serializers
from products import models

class ProductViews(viewsets.ModelViewSet):
    serializer_class = serializers.ProductSerializers
    queryset = models.Product.objects.all()
