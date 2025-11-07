from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from django.db import models
from io import BytesIO
from PIL import Image
import os
import uuid

path_env = os.path.join('database', '.env')
load_dotenv(dotenv_path=path_env)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def upload_image(file_bytes, filename):
    SUPABASE_BUCKET = "imagens_produtos"

    date = datetime.now().strftime("%d%m%Y_%H%M%S")
    ext = filename.split('.')[-1]
    name_image = f"{uuid.uuid4().hex[:10]}_{date}.{ext}"
    path_storage = f"public/{name_image}"

    # bytes diretos (sem BytesIO)
    response = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path_storage,
        file_bytes,  # <-- aqui vão os bytes crus
        file_options={"content-type": f"image/{ext}"}
    )

    # O SDK retorna None quando sucesso precisamos conferir erros
    if hasattr(response, "error") and response.error is not None:
        raise Exception(response.error.message)

    # Gera URL pública
    url_publica = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(path_storage)
    return url_publica

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
    img_file = models.ImageField(upload_to="temp_uploads", blank=True, null=True) #upload_to="imagens_produtos",
    img_url = models.URLField(max_length=500, blank=True, null=True)
    promocao = models.BooleanField(default=False)
    hora_criacao = models.TimeField(auto_now_add=True)
    data_criacao = models.DateField(auto_now_add=True)
        
    def __str__(self):
        return self.nome[:24] + "..."

    def save(self, *args, **kwargs):
        if self.img_file:
            img = Image.open(self.img_file)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            max_size = (1080, 1080)
            img.thumbnail(max_size)

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=95)
            buffer.seek(0)

            # Enviando os bytes diretos
            url_publica = upload_image(buffer.getvalue(), f"{self.nome}.jpg")
            self.img_url = url_publica

            # Apaga a imagem local
            self.img_file.delete(save=False)

        super().save(*args, **kwargs)
