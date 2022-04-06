from urllib.request import Request
from django.shortcuts import render
from .models import Producto
from .forms import ContactoForms
# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def sobreNosotros(request):
    return render(request, 'app/sobreNosotros.html')    

def contacto(request):
    data = {
        'form': ContactoForms()
    }

    if request.method == 'POST':
        formulario = ContactoForms(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]= "contacto guardado"
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html',data)

def productos(request):

    productos = Producto.objects.all()
    data = {
        'productos' : productos
    }
    return render(request, 'app/productos.html',data) 

def carrito(request):
    return render(request, 'app/carrito.html')
