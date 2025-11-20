from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O nome deve ter pelo menos 3 caracteres")
        return value
    
    def validate_nome(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço não pode ser negativo")
        
        elif not value.isdigit():
            raise serializers.ValidationError("Preço invalido")
        
        return value