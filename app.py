from functools import wraps
import os
from flask import Flask, jsonify, request
import data.db_conection as connection
import data.querys as query
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

USER = os.getenv("USER_API")
PASS = os.getenv("PASSWORD_API")
conexion = connection.connection()
query = query.datos()


app = Flask(__name__)

def verificar_autenticacion(username, password):
    return username == USER and password == PASS


def requerir_autenticacion(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        username = request.args.get('User')
        password = request.args.get('Password')
        if not verificar_autenticacion(username, password):
            return jsonify({'mensaje': 'Autenticación requerida'}), 401
        return f(*args, **kwargs)
    return decorador


@app.route('/', methods=['GET'])
@requerir_autenticacion
def obtener_datos():
    with connection.connection() as conexion:
        cursor = conexion.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return jsonify(data)
    

@app.route('/ejecutivos', methods=['GET'])
@requerir_autenticacion
def obtener_datos_ejecutivos():
    with connection.connection() as conexion:
        cursor = conexion.cursor()
        categorias = ['C-SS - EC Semi Senior', 'C-JU - EC Junior', 'C-SE - EC Senior', 'C-JC - EC Junior']
        query_ejecutivos = f"{query} WHERE category IN {str(tuple(categorias))}"
        cursor.execute(query_ejecutivos)
        rows = cursor.fetchall()
        data = []
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return jsonify(data)
    

@app.route('/jefatura_comercial', methods=['GET'])
@requerir_autenticacion
def obtener_jefatura_comercial():
    with connection.connection() as conexion:
        cursor = conexion.cursor()
        categoria = 'JC - Jefatura Comercial'
        query_jefatura_comercial = f"{query} WHERE category = ?"
        cursor.execute(query_jefatura_comercial, (categoria,))
        rows = cursor.fetchall()
        data = []
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return jsonify(data)
    
@app.route('/gerentes_zonales', methods=['GET'])
@requerir_autenticacion
def obtener_gerentes_zonales():
    with connection.connection() as conexion:
        cursor = conexion.cursor()
        categoria = 'GZ - Gerente Zonal'
        query_gerentes_zonales = f"{query} WHERE category = ?"
        cursor.execute(query_gerentes_zonales, categoria)
        rows = cursor.fetchall()
        data = []
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return jsonify(data)
    
@app.route('/hola')
def hello_world():
    return 'Hola Mundo'

if __name__ == '__main__':
    print('Programa corriendo con exito')
    app.run()
    
