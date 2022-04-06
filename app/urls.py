from django.urls import path
from .views import home, sobreNosotros, productos, carrito,contacto

urlpatterns = [
    path('', home, name="home"),
    path('sobreNosotros/', sobreNosotros, name="sobreNosotros"),
    path('productos/', productos, name="productos"),
    path('carrito/', carrito, name="carrito"),
    path('contacto/',contacto , name="contacto")
]
