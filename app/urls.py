from ast import Div
from unicodedata import name
from django.urls import path
from .views import actualizarProducto,agregar_producto, home, sobreNosotros, productos, carrito,contacto,listar_productos,modificar_productos,eliminar_producto,detalleProducto,registro,checkout
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', home, name="home"),
    path('sobreNosotros/', sobreNosotros, name="sobreNosotros"),
    path('productos/', productos, name="productos"),
    path('productos/<id>',detalleProducto , name="detail"),
    path('carrito/',login_required(carrito), name="carrito"),
    path('checkout/',login_required(checkout), name="checkout" ),
    path('contacto/',contacto , name="contacto"),
    path('agragar-producto/', agregar_producto, name="agregar_producto"),
    path('listar-productos/', listar_productos, name="listar_productos"),
    path('modificar-productos/<id>/',modificar_productos,name="modificar_productos"),
    path('eliminar-producto/<id>/', eliminar_producto, name="eliminar_producto"),
    path('registro/', registro, name="registro"),
    path('actualizarProducto/', actualizarProducto, name="actualizarProducto"),  

]

