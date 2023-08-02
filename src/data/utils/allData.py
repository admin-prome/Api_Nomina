import data.db_conection as connection
import data.querys as query
from flask import jsonify


def allData():
    with connection.connection() as conexion:
        cursor = conexion.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            data.append(dict(zip(column_names, row)))
        return jsonify(data)


