from atexit import register
from re import search
from django.contrib import admin
from .models import Marca, Producto,Contacto
# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombreProducto","precio","talla","marca"]
    search_fields = ["nombreProducto"]
    list_filter = ["marca"]


class ContactoAdmin(admin.ModelAdmin):
    list_display = ["nombre","correo","tipo_consulta"]
    search_fields = ["nombre"]
    list_filter = ["tipo_consulta"]

admin.site.register(Marca)
admin.site.register(Producto,ProductoAdmin)
admin.site.register(Contacto,ContactoAdmin)