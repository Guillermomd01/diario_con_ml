from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#creamos el engine que se utilizara para concetarse con la base de datos
engine=create_engine("sqlite:///entradas.db", connect_args={"check_same_thread":False})
#con el connect args le decimos que no gestione la bd en el mismo hilo que la aplicacion principal
#Creamos la sesión que nos permitira hacer las transacciones necesarias
Session=sessionmaker(bind=engine)
#creamos una variable para invocar a la sesión
session=Session()
#Utilizamos base para mapear con la base de datos la información de las clases heredadas
Base= declarative_base()