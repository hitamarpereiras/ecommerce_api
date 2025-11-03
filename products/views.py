from django.http import JsonResponse

def produtos(request):
    if request.method == 'GET':
        #Apenas testes
        produtos = [
            {'id': 1, 'nome': 'Tablete Samsung', 'preco': 689.00},
        ]
        return JsonResponse(produtos, safe=False)