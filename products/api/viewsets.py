from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from products.api import serializers
from products import models

class ProductViews(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProductSerializers
    queryset = models.Product.objects.all()
