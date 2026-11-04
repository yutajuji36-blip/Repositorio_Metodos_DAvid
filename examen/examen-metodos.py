# Importar las librerias
from sqlalchemy import Column,Date, Numeric, Integer, String, create_engine, Text, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
import pandas as pd

# Informacion de la conexión a la base de datos de postgreSQL
USER = "david12"
PASSWORD = "qazPÑM1"
HOST = "localhost"
PORT = "5432"
DB_NAME = "examen"

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# Creating a Database Connection

# SQLAlchemy creates database connections using create_engine() function. This function takes a
# connection URL and returns an engine object, which manages the connection between Python and the database.


engine = create_engine(DATABASE_URL)

# Declarar la base para los modelos
Base = declarative_base()


#  Definir la clase (tabla 'nombre-de-la-tabla')
class tabla_fechas(Base):
  __tablename__ = "tabla_fechas"

  id = Column(Integer, primary_key=True, autoincrement=True)
  fecha = Column(Date, nullable=False)
  precio = Column(Numeric(precision=10,scale=4))


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

#  Crear una sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

fecha_inicio = "20-10-2026"
fecha_fin = "22-10-2026"

mi_query= session.query(tabla_fechas).filter(tabla_fechas.fecha.between(fecha_inicio, fecha_fin))
df = pd.read_sql(mi_query.statement, session.bind)

# Cerrar sesión
session.close()

media = df['precio'].astype(float).mean()
varianza = df['precio'].astype(float).var()
desviacion_estandar = df['precio'].astype(float).std()




