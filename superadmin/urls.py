from django.urls import path
from .views import cryptolinkx_admin
urlpatterns = [
    path('', cryptolinkx_admin, name = 'cryptolinkx_admin'),
]