import pandas as pd
import time
from django.db import connection

def get_auto_increment_columns(table_name, database_name):
    auto_increment = []
    with connection.cursor() as cursor:
                cursor.execute(f"USE {database_name}")
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns = cursor.fetchall()
                for column in columns:
                    field, type, null, key, default, extra = column
                    if "auto_increment" in extra:
                        auto_increment.append(field)
    return auto_increment

def append_data(table_name, database_name, uploaded_file, auto_increment):
    start_time = time.time()
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        temp_csv_file = 'temp.csv'
        df.to_csv(temp_csv_file, sep=';', index=False, encoding='utf-8')
    elif uploaded_file.name.endswith('.csv'):
        temp_csv_file = uploaded_file.name
    else:
        error_message = "Formato de arquivo não suportado"
        return error_message

    df = pd.read_csv(temp_csv_file, sep=';', encoding='utf-8')
    for column_name in df.columns:
        if column_name in auto_increment:
            df[column_name] = None
        else:
            df[column_name] = df[column_name].apply(lambda x: None if pd.isna(x) else x)

    with connection.cursor() as cursor:
        cursor.execute(f"USE {database_name}")
        cursor.execute(f"DESCRIBE {table_name}")
        table_columns = [column[0] for column in cursor.fetchall()]

    if list(df.columns) == table_columns:
        with connection.cursor() as cursor:
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            values = [tuple(row) for row in df.values]
            cursor.executemany(sql, values)
            connection.commit()
            end_time = time.time()
        
        with connection.cursor() as cursor:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    total_records = cursor.fetchone()[0]

        row_count = len(df)
        elapsed_time = end_time - start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        elapsed_milliseconds = int((elapsed_time - int(elapsed_time)) * 1000)
        elapsed_time_formatted = f"{elapsed_minutes:02d}:{elapsed_seconds:02d}.{elapsed_milliseconds:03d}"

    return row_count, total_records, elapsed_time_formatted

