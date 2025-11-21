from rest_framework import serializers
from .models import Produto
    
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        read_only_fields = ["id", "img_url", "hora_criacao", "data_criacao"]

    def validate_nome(self, value):
        if not value:
            raise serializers.ValidationError("O nome deve ter pelo menos 3 caracteres")
        
        return value
    
    def validate_preco(self, value):
        if value < 0:
            raise serializers.ValidationError("O preço não pode ser negativo")
        
        return value