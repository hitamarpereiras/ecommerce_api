from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produto
from .serializers import ProdutoSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class  ProdutoListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('categoria')

        if category:
            queryset = queryset.filter(categoria__iexact=category.lower())
        return queryset
    
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        if not queryset.exists():
            this_category = request.query_params.get('categoria')
            if this_category:
                msg = f"Nenhum produto encontrado na categoria '{this_category}'."
            else:
                msg = "Nenhum produto encontrado."
            return Response({"mensagem": msg}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class ProdutoCreateView(APIView):
    permission_classes = [IsAuthenticated]

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