from asyncio.windows_events import NULL
from distutils.command.upload import upload
from email.mime import image
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User



# Create your models here.





class Marca(models.Model):
    nombreMarca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreMarca


class Genero(models.Model):
    nombreGenero = models.CharField(max_length=50)

    def __str__(self):
        return self.nombreGenero



class Category(models.Model):
    name= models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Producto(models.Model):

    imagen = models.ImageField(upload_to="productos", null=True)
    nombreProducto = models.CharField(max_length=80, null=True)
    precio = models.IntegerField()
    descripcion = models.TextField()
    talla = models.CharField(max_length=5)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    categoria = models.ForeignKey(Category, on_delete=models.PROTECT)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombreProducto

    @property
    def imagenURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url


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

class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaccion_id = models.CharField(max_length=50, null=True)


    def __str__(self):
        return str(self.id)

    @property
    def envio(self):
        envio = False
        productospedidos = self.productospedidos_set.all()
        return envio

    @property
    def get_cart_total(self):
        productospedidos = self.productospedidos_set.all()
        total = sum([item.get_total for item in productospedidos])
        return total 
    @property
    def get_cart_items(self):
        productospedidos = self.productospedidos_set.all()
        total = sum([item.cantidad for item in productospedidos])
        return total   
        
    @property
    def get_precio_total(self):
        productospedidos = self.productospedidos_set.all()
        totalEnvio = (sum([item.get_total for item in productospedidos])+15)
        return totalEnvio 


class ProductosPedidos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total= self.producto.precio * self.cantidad
        return total

class DireccionEnvio(models.Model):
    cliente = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=200, null=True)
    codigoPostal = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.direccion