from importlib.metadata import files
from urllib.request import Request
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import Producto
from .forms import ContactoForms,Productoform
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
# Create your views here.


# paginas principales
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
            data["mensaje"]= " ✓ Mensaje enviado"
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





# Crud
def agregar_producto (request):

    data = {
        'form':Productoform()
    }

    if request.method == 'POST':
        formulario = Productoform(data=request.POST, files=request.FILES )
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Producto Registrado")
            data["mensaje"] = "Guardado Correctamente"
        else:
            data["form"] = formulario

    return render(request,'app/producto/agregar.html',data)

def listar_productos(request):
        productos = Producto.objects.all()

        page = request.GET.get('page',1)
        try:
            # cantidad de items que muestra el listado 
            paginator = Paginator(productos,5)
            productos= paginator.page(page)
        except:
            raise Http404

        data = {
            'entity' : productos,
            'paginator':paginator
        }

        return render(request,'app/producto/listar.html',data)

def modificar_productos(request, id):
    
    producto = get_object_or_404(Producto, id=id)

    data = {
        'form':Productoform(instance=producto)
    }

    if request.method == 'POST':
        formulario = Productoform(data=request.POST, instance=producto, files=request.FILES )
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listar_productos")
        data["form"]= formulario
    return render(request,'app/producto/modificar.html',data)

def eliminar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_productos")