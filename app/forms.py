from dataclasses import fields
from django import forms   
from .models import Contacto ,Producto


class ContactoForms(forms.ModelForm):

        class Meta:
            model = Contacto
            fields = '__all__' 

class Productoform(forms.ModelForm):
        class Meta:
            model = Producto
            fields = '__all__'