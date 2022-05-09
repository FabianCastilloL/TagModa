from asyncio.windows_events import NULL
from distutils.command.upload import upload
from email.mime import image
from pyexpat import model
from django.db import models



# Create your models here.


class Cliente(models.Model):
    primer_nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    numero = models.CharField(max_length=9)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Cliente.objects.get(email= email)
        except:
            return False


    def isExists(self):
        if Cliente.objects.filter(email = self.email):
            return True

        return False    


class Marca(models.Model):
    nombreMarca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreMarca

class Category(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Producto( models.Model):

    imagen = models.ImageField(upload_to="productos", null=True)
    nombreProducto = models.CharField(max_length=80, null=True)
    precio = models.IntegerField()
    descripcion = models.TextField()
    talla = models.CharField(max_length=5)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombreProducto




opciones_consultas = [
    [0,"Consulta"],
    [1,"Reclamo"],
    [2,"Sugerencias"],
    [3,"Cambio Producto"],
]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre