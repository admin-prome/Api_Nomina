import os
import traceback
import pyodbc
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'..', '..', '.env')
load_dotenv(dotenv_path)

SERVER = os.getenv("SERVER")
USER = os.getenv("USER")
PASS = os.getenv("PASSWORD")
DB = os.getenv("DB")


def connection():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DB+';UID='+USER+';PWD='+PASS)
        print(f'conexion exitosa a {SERVER}')
        return conexion
    except Exception as e:
        print('Error al intentar conectarse a la base de "provmicrosql02.database.windows.net"')
        traceback.print_exc()
        
# connection()