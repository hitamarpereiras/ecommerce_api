from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto
from .serializers import ProdutoSerializer

class  ProdutoListView(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria')

        if categoria:
            queryset = queryset.filter(categoria__iexact=categoria.lower())
        return queryset
    
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        if not queryset.exists():
            categoria = request.query_params.get('categoria')
            if categoria:
                mensagem = f"Nenhum produto encontrado na categoria '{categoria}'."
            else:
                mensagem = "Nenhum produto encontrado."
            return Response({"mensagem": mensagem}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
# View simples
@api_view(['GET'])
def list_products(request):
    products = Produto.objects.all()
    serializer = ProdutoSerializer(products, many=True)
    return Response(serializer.data)

# Metodo Post
class ProdutoCreateView(APIView):

    def post(self, request):
        serializer = ProdutoSerializer(data=request.data)

        if serializer.is_valid():
            produto = serializer.save()
            return Response(
                {
                    "message": "Produto salvo com sucesso!",
                    "produto": ProdutoSerializer(produto).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)