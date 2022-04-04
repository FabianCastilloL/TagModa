from django.urls import path
from .views import home,sobrenosotros
urlpatterns = [
    path('', home,name="home"),
    path('sobrenosotros/', sobrenosotros,name="sobrenosotros"),
]
