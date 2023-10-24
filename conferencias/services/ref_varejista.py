import pandas as pd
from django.db import connection

def soma_valores(database_name):
    with connection.cursor() as cursor:
        cursor.execute(f'USE {database_name}')
        cursor.execute("""
            SELECT ref_varejista,ano, mes, SUM(valor) 
            FROM prod_lj 
            WHERE ano IN (2021, 2022, 2023) 
            GROUP BY ano, mes, ref_varejista
        """)
        resultado = cursor.fetchall()

        return resultado

def gerar_tabelas_html(resultado):
    varejistas = set(row[0] for row in resultado)
    meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
    
    html = ''
    for varejista in varejistas:
        varejista_data = [row for row in resultado if row[0] == varejista]
        df = pd.DataFrame(varejista_data, columns=['ref_varejista', 'ano', 'mes', 'total_valor'])
        df['mes'] = pd.Categorical(df['mes'], categories=meses, ordered=True)
        df['ano'] = pd.to_numeric(df['ano'])
        pivot_table = df.pivot_table(values='total_valor', index='mes', columns='ano', aggfunc='sum', fill_value=0)
        
        html += f'<h2>{varejista}</h2>'
        html += '<table border="1">'
        html += '<tr><th></th>'
        for col in pivot_table.columns:
            html += f'<th>{col}</th>'
        html += '</tr>'
        for index, row in pivot_table.iterrows():
            html += f'<tr><td>{index}</td>'
            for col in pivot_table.columns:
                html += f'<td>{row[col]:.2f}</td>'
            html += '</tr>'
        html += '</table>'
    
    return html
