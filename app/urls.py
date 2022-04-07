from ast import Div
from unicodedata import name
from django.urls import path
from .views import agregar_producto, home, sobreNosotros, productos, carrito,contacto,listar_productos,modificar_productos,eliminar_producto

urlpatterns = [
    path('', home, name="home"),
    path('sobreNosotros/', sobreNosotros, name="sobreNosotros"),
    path('productos/', productos, name="productos"),
    path('carrito/', carrito, name="carrito"),
    path('contacto/',contacto , name="contacto"),
    path('agragar-producto/', agregar_producto, name="agregar_producto"),
    path('listar-productos/', listar_productos, name="listar_productos"),
    path('modificar-productos/<id>/',modificar_productos,name="modificar_productos"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    
]

