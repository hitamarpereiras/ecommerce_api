from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produto
from .serializers import ProdutoSerializer

@api_view(['GET'])
def list_products(request):
    products = Produto.objects.all()
    serializer = ProdutoSerializer(products, many=True)
    return Response(serializer.data)
