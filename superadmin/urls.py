from django.urls import path
from .views import cryptolinkx_admin
from django.urls import include

urlpatterns = [
    path('', cryptolinkx_admin, name = 'cryptolinkx_admin'),
    
]