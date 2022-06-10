from dataclasses import dataclass
from importlib.metadata import files
from pickletools import read_uint1
from urllib.request import Request
from wsgiref.util import request_uri
from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .models import Producto,Category
from .forms import ContactoForms,Productoform,CustomUserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.http import JsonResponse
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views import View

import json
# Create your views here.

def completo(request):
    return render(request, 'app/pagoCompleto.html')
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
    marcs = Marca.objects.all()
    gen = Genero.objects.all()

    nombre_prod = request.GET.get('nombre_producto')
    category = request.GET.get('catt')
    Nom_marcas = request.GET.get('marr')
    tipo_genero = request.GET.get('gen')



    if is_valid_queryparam(nombre_prod):
        productos = productos.filter(nombreProducto__icontains=nombre_prod)
    
    if is_valid_queryparam(category)and  category !='Selecciona...':
        productos = productos.filter(categoria__name=category)
    
    if is_valid_queryparam(Nom_marcas)and  Nom_marcas !='Selecciona...':
        productos = productos.filter(marca__nombreMarca=Nom_marcas)
    
    if is_valid_queryparam(tipo_genero):
        productos = productos.filter(genero__nombreGenero=tipo_genero)

    context = {
        'productos' : productos,
        'categorias': categorias,
        'marca': marcs,
        'genero':gen
    }
    return render(request, 'app/productos.html',context) 
    


def detalleProducto(request,id):
    productos = Producto.objects.all()
    obj = get_object_or_404(Producto,pk=id)
    data = {
        'productos' : productos,
        'obj':obj
    }
    
    
    return render (request,'app/detalle.html',data)


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






def carrito(request):  
    if request.user.is_authenticated:
        cliente = request.user
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        items = pedido.productospedidos_set.all()
        cartItems = pedido.get_cart_items
        
    else:
        items = []
        pedido = {'get_cart_total':0,'get_cart_items':0}
        cartItems = pedido['get_cart_items']

    context = {'items':items, 'pedido':pedido, 'cartItems':cartItems}
    return render(request, 'app/carrito.html', context)


def checkout(request):
    if request.user.is_authenticated:
        cliente = request.user
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, complete=False)
        items = pedido.productospedidos_set.all()
        cartItems = pedido.get_cart_items
    else:
        items = []
        pedido = {'get_cart_total':0,'get_cart_items':0}
        cartItems = pedido['get_cart_items']

    context = {'items':items, 'pedido':pedido, 'cartItems':cartItems}
    return render(request, 'app/checkout.html', context)

def actualizarProducto(request):
    data = json.loads(request.body)
    productoId = data['productoId']
    action = data['action']

    print('Action:', action)
    print('Producto', productoId)

    cliente = request.user
    producto = Producto.objects.get(id=productoId)
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, complete=False)

    productosPedidos, created = ProductosPedidos.objects.get_or_create(pedido=pedido, producto=producto)
    
    if action == 'add':
        productosPedidos.cantidad = (productosPedidos.cantidad + 1)

    if action =='remove':
        productosPedidos.cantidad = (productosPedidos.cantidad - 1)
    
    if action =='eliminarProducto':
        productosPedidos.cantidad = 0
            

    productosPedidos.save()

    if productosPedidos.cantidad <= 0:
        productosPedidos.delete()

    return JsonResponse('Item fue agregado', safe=False)




class Send(View):
    def get(self, request):
        return render(request, 'app/pagoCompleto.html')
    
    def post(self, request):
        email = request.POST.get('email')
        print(email)

        template = get_template('app/email-order-success.html')

        # Se renderiza el template y se envias parametros
        content = template.render({'email': email})

        # Se crea el correo (titulo, mensaje, emisor, destinatario)
        msg = EmailMultiAlternatives(
            'Gracias por tu compra',
            'Hola, te enviamos un correo con tu factura',
            settings.EMAIL_HOST_USER,
            [email]
        )

        msg.attach_alternative(content, 'text/html')
        msg.send()

        

        return render(request, 'app/pagoCompleto.html')