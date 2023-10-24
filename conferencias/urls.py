from django.urls import path
from conferencias.views import login_c, list_databases, varejistas

app_name = 'conferencias'

urlpatterns = [
    path('login_c/',login_c, name='login_c'),
    path('list_databases/',list_databases, name='list_databases'),
    path('varejistas/<str:database_name>',varejistas, name='varejistas'),
]
