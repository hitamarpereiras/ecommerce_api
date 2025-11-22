from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   # pega access + refresh (login)
    TokenRefreshView,     # troca refresh por novo access (e opcionalmente novo refresh se ROTATE)
    TokenVerifyView,      # verifica um token (útil em debug)
)

def home(request):
    return JsonResponse({'message': 'API Django no ar 🚀'})

urlpatterns = [
    path('', home),  # rota principal opcional
    path('admin/', admin.site.urls),
    path('produtos/', include('products.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]