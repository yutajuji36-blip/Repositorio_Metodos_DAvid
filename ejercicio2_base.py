import pandas as pd
import sqlite3

# Conectar a la base de datos local
conn = sqlite3.connect('banco_datos.db')

archivos = [
    ('sexenio-1.csv', 'sexenio_1'),
    ('sexenio-2.csv', 'sexenio_2')
]

for archivo, nombre_tabla in archivos:
    # Leer el CSV omitiendo las primeras 6 filas de encabezado institucional
    df = pd.read_csv(archivo, skiprows=6)

    # Seleccionar y renombrar columnas clave
    df_limpio = df[['Fecha', 'Para solventar\nobligaciones']].copy()
    df_limpio.columns = ['fecha', 'tipo_cambio']

    # Asegurar que el tipo de cambio sea numérico y limpiar valores no válidos (como "N/E")
    df_limpio['tipo_cambio'] = pd.to_numeric(df_limpio['tipo_cambio'], errors='coerce')
    df_limpio = df_limpio.dropna()

    # Guardar en la base de datos
    df_limpio.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
    print(f"Base de datos: Tabla '{nombre_tabla}' creada correctamente con {len(df_limpio)} registros.")

conn.close()
