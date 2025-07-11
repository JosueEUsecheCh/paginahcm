from django.urls import path
from . import views

urlpatterns = [
    path('', views.consultar_cedula, name='consultar_cedula'),  
]
