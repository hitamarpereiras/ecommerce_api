from django.db import models
from PIL import Image
from django.utils import timezone
import os
import uuid

# Create your models here.
class Category(models.TextChoices):
        DRINKS = 'Bebidas', 'Bebidas'
        CANDY = 'Doces', 'Doces'
        SALTY = 'Salgados', 'Salgados'
        OTHERS = 'Outros', 'Outros'

class Product(models.Model):
    # Atributos
    nome = models.CharField(max_length=100, blank=False)
    categoria = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.CANDY
    )
    descricao = models.TextField(default="Sem descrição", max_length=400)
    preco = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to="Images_products", blank=False)
    promocao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome[:24] + "..."
    
    def save(self, *args, **kwargs):
         super().save(*args, **kwargs)

         if self.imagem:
            ext = os.path.splitext(self.imagem.name)[1] # pegar a extensao
            self_name = "".join(
                c for c in self.nome if c.isalnum() or c in (" ", "_", "-")
            ).rstrip() # Aqui remove os caracters especiais
            self_name = self_name.replace(" ", "_").lower()

            new_name = f"{self_name}_{uuid.uuid4().hex[:8]}{ext}"
            new_path = os.path.join("Images_products", new_name)
            full_old_path = self.imagem.path
            full_new_path = os.path.join(os.path.dirname(full_old_path), new_name)

            # Aqui renomeia o arquivo no disco
            os.rename(full_old_path, full_new_path)

            self.imagem.name = new_path
            super().save(update_fields=["imagem"])

            img = Image.open(self.imagem.path)
            if img.mode in ("RGB", "P"):
                img = img.convert("RGB")

            max_size = (1080, 1080)
            if img.height != 1080 or img.width != 1080:
                 img.thumbnail(max_size)

            img.save(self.imagem.path, format="JPEG", quality=95)