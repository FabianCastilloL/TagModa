from asyncio.windows_events import NULL
from distutils.command.upload import upload
from email.mime import image
from pyexpat import model
from django.db import models

# Create your models here.
class Marca(models.Model):
    nombreMarca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreMarca

class Producto( models.Model):
    imagen = models.ImageField(upload_to="productos", null=True)
    nombreProducto = models.CharField(max_length=80)
    precio = models.IntegerField()
    descripcion = models.TextField()
    talla = models.CharField(max_length=5)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombreProducto




opciones_consultas = [
    [0,"Consulta"],
    [1,"Reclamo"],
    [2,"Sugerencias"]
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre