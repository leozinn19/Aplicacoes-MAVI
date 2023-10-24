from django.shortcuts import render
from django.conf import settings
from django.db import connection

from conferencias.services.ref_varejista import soma_valores, gerar_tabelas_html

def login_c(request):
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

        return render(request, 'conferencias/login_c.html', {'error_message': error_message})
    else:
        return render(request, 'conferencias/login_c.html')
    
def list_databases(request):
    with connection.cursor() as cursor:
        cursor.execute("SHOW DATABASES")
        databases= cursor.fetchall()
    
    return render(request, 'conferencias/databases.html', {'databases': databases})

def varejistas(request, database_name):
    resultado = soma_valores(database_name)
    tabelas_html = gerar_tabelas_html(resultado)
    return render(request, 'conferencias/varejistas.html', {'tabelas_html': tabelas_html})
