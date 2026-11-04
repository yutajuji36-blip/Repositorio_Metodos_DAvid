import pandas as pd
from sqlalchemy import create_engine


df = pd.read_csv('fechas.csv')


usuario = "david12"       
contrasena = "qazPÑM1" 
host = "localhost"
puerto = "5432"
nombre_db = "examen"   


engine = create_engine(f'postgresql+psycopg2://{usuario}:{contrasena}@{host}:{puerto}/{nombre_db}')


df.to_sql('tabla_fechas', con=engine, if_exists='replace', index=False)

print("¡Datos guardados exitosamente en la base de datos!")
