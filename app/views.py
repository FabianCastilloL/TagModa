from dataclasses import dataclass
from importlib.metadata import files
from urllib.request import Request
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import Producto,Category
from .forms import ContactoForms,Productoform,CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required

from .filters import filtro_prod
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


#validacion para filtro
def is_valid_queryparam(param):
    return param !='' and param is not None

def productos(request):
    productos = Producto.objects.all()
    categorias = Category.objects.all()
    
    nombre_prod = request.GET.get('nombre_producto')
    category = request.GET.get('catt')

    if is_valid_queryparam(nombre_prod):
        productos = productos.filter(nombreProducto__icontains=nombre_prod)
    
    if is_valid_queryparam(category)and  category !='Selecciona...':
        productos = productos.filter(categoria__name=category)
    
    context = {
        'productos' : productos,
        'categorias': categorias
    }
    return render(request, 'app/productos.html',context) 
    
def detalleProducto(request,id):
    obj = get_object_or_404(Producto,pk=id)
    return render (request,'app/detalle.html',{'obj':obj})


@login_required
def carrito(request):
    return render(request, 'app/carrito.html')





# Crud
@permission_required('app.add_producto')
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

@permission_required('app.view_producto')
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

@permission_required('app.change_producto')
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

@permission_required('app.delete_producto')
def eliminar_producto(request,id):
    producto = get_object_or_404(Producto,id=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listar_productos")


#registro de usuario
def registro(request):
    data = {
    'form': CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario=CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request,"Se a registrado correctamente")
            #redirigir al home

            return redirect(to="home")
        data["form"]=formulario

    return render(request, 'registration/registro.html',data)