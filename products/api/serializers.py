from rest_framework import serializers
from products import models

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'