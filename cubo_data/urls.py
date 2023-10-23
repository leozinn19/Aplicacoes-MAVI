from django.urls import path

from cubo_data.views import (index ,login, list_databases, list_tables, table_services, save_table, append_table)

urlpatterns = [
    path("", index, name='index'),
    path("login/", login, name='login'),
    path('databases/', list_databases, name='databases'),
    path('tables/<str:database_name>', list_tables, name='tables'),
    path('table_service/<str:database_name>/<str:table_name>', table_services, name='table_service'),
    path('save_table/<str:database_name>/<str:table_name>', save_table, name='save_table'),
    path('append_table/<str:database_name>/<str:table_name>', append_table, name='append_table'),
]