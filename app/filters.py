import django_filters
from .models import Producto


class filtro_prod(django_filters.FilterSet):
    nombreProducto = django_filters.CharFilter(lookup_expr='icontains')
    precio= django_filters.AllValuesFilter
    categoria = django_filters.AllValuesFilter
    class Meta:
        model = Producto
        fields = ('nombreProducto','marca','categoria')

