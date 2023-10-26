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

        varejistas = set(row[0] for row in resultado)
        meses = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']
        data_dict = {}
        
        for varejista in varejistas:
            varejista_data = [row for row in resultado if row[0] == varejista]
            df = pd.DataFrame(varejista_data, columns=['ref_varejista', 'ano', 'mes', 'total_valor'])
            df['mes'] = pd.Categorical(df['mes'], categories=meses, ordered=True)
            df['ano'] = pd.to_numeric(df['ano'])
            df['total_valor'] = df['total_valor'].round(2)
            pivot_table = df.pivot_table(values='total_valor', index='mes', columns='ano', aggfunc='sum', fill_value=0)
            data_dict[varejista] = pivot_table

        return data_dict
