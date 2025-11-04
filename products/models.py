from django.db import models
from PIL import Image

# Create your models here.
class Categoria(models.TextChoices):
        BEBIDAS = 'Bebidas', 'Bebidas'
        DOCES = 'Doces', 'Doces'
        SALGADOS = 'Salgados', 'Salgados'
        OUTROS = 'Outros', 'Outros'

class Produto(models.Model):
    nome = models.CharField(max_length=80, blank=False)
    categoria = models.CharField(
        max_length=40,
        choices=Categoria.choices,
        default=Categoria.BEBIDAS
    )
    descricao = models.TextField(default="Sem descrição", max_length=300)
    preco = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to="imagens_produtos", blank=False)
    promocao = models.BooleanField(default=False)
    hora_criacao = models.TimeField(auto_now_add=True)
    data_criacao = models.DateField(auto_now_add=True)
        
    def __str__(self):
        return self.nome[:24] + "..."
    
    def save(self, *args, **kwargs):
         super().save(*args, **kwargs)

         if self.imagem:
            img = Image.open(self.imagem.path)
            if img.mode in ("RGB", "P"):
                img = img.convert("RGB")

            max_size = (1080, 1080)
            if img.height < 520 or img.width < 520:
                 img.thumbnail(max_size)
                 img.save(self.imagem.path, format="JPEG", quality=95)