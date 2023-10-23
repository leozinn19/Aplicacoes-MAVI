from django.shortcuts import render
from django.conf import settings
from django.db import connection
from django.http import HttpResponse

from cubo_data.form import UploadFileForm
from .services.append_data import append_data, get_auto_increment_columns

import io
import pandas as pd

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se as credenciais são válidas (implemente sua própria lógica de autenticação)
        try:
                # Atualiza as configurações do banco de dados
                settings.DATABASES['default']['USER'] = user
                settings.DATABASES['default']['PASSWORD'] = password
                return list_databases(request)
        except Exception as e:
                error_message = f"Erro ao conectar ao banco de dados: {e}"

        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def list_databases(request):
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        databases= cursor.fetchall()
    
    return render(request, 'databases.html', {'databases': databases})

def list_tables(request, database_name):
    with connection.cursor() as cursor:
        cursor.execute(f"USE {database_name}")
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
    
    return render(request, 'tables.html', {'database_name': database_name, 'tables': tables})

def table_services(request, database_name, table_name):
    return render(request, 'table_services.html', {'database_name': database_name, 'table_name' : table_name}) 

def save_table(request, database_name, table_name):
    with connection.cursor() as cursor:
        cursor.execute(f'USE {database_name}')
        cursor.execute(f'SHOW COLUMNS FROM {table_name}')
        columns = [row[0] for row in cursor.fetchall()]

        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False, sheet_name=f'{table_name}')
        response = HttpResponse(excel_file.getvalue(), content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file_name = f"{table_name.upper()}_{database_name}.xlsx"
        response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response

def append_table(request, database_name, table_name):
    form = UploadFileForm(request.POST, request.FILES)
    row_count, total_records, elapsed_time_formatted = None, None, None
    if request.POST:
        file = request.FILES['file']
        auto_increment = get_auto_increment_columns(table_name, database_name)
        row_count, total_records, elapsed_time_formatted = append_data(table_name, database_name, file, auto_increment)

    return render(request, 'append_table.html', {'form': form, 'table_name': table_name, 'db_name': database_name, 'row_count' : row_count,
                                                  "total_records": total_records, 'elapsed_time_formatted': elapsed_time_formatted})