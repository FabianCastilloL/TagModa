from dataclasses import fields
from django import forms   
from .models import Contacto 


class ContactoForms(forms.ModelForm):

        class Meta:
            model = Contacto
            fields = '__all__' 