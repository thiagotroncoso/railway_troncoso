from flask import Flask, request, jsonify
from flask.helpers import make_response
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin


# para subir archivos
import os
#from werkzeug.utils import secure_filename


app = Flask(__name__)

import os

app.config["MYSQL_HOST"] = os.environ.get("DB_HOST")
app.config["MYSQL_USER"] = os.environ.get("DB_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DB_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DB_NAME")

mysql = MySQL(app)

CORS(app)


@app.route("/registrar_usuario", methods=["POST"])
@cross_origin()
def ingresar_usuario():
    nombre = request.json["nombre"]
    contraseña = request.json["contraseña"]
    email = request.json["email"]

    cursor = mysql.connection.cursor()

    sql = "INSERT INTO Usuarios(nombre, contraseña, email) values(%s, %s, %s);"
    cursor.execute(sql, (nombre, contraseña, email))


    mysql.connection.commit()
 
    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Agregado nuevo usuario"})
    return response

@app.route("/iniciar_sesion", methods=["GET"])
@cross_origin()
def inicio_de_sesion():
    #consulta SQL
    sql = "SELECT idUsuarios, nombre, contraseña, email FROM Usuarios"

    #crear el cursor
    cursor = mysql.connection.cursor()#mysql.connect.cursor()
    cursor.execute(sql)

    resultado = cursor.fetchall()

    #cerrar la conexión
    cursor.close()
    response = make_response()

    if resultado == None:
        response = jsonify({"mensaje":None})
        return response
    else:
        usuarios = []

        for i in resultado:

            p = {"id":i[0], "nombre":i[1], "contraseña":i[2], "email":i[3]}
            usuarios.append(p)

        return jsonify(usuarios)


@app.route("/subir_receta", methods=["POST"])
@cross_origin()
def crear_receta():
    id_receta= request.json["id_receta"] 
    nombre = request.json["nombre"]  
    img = request.json["img"]
    ingredientes = request.json["ingredientes"]
    pasos_a_seguir = request.json["pasos_a_seguir"]
  

    cursor = mysql.connection.cursor()

    sql = "INSERT INTO Usuarios(id_receta, nombre, img, ingredientes, pasos_a_seguir) values(%s, %s, %s, %s, %s);"
    cursor.execute(sql, (id_receta, nombre, img, ingredientes, pasos_a_seguir))


    mysql.connection.commit()

    cursor.close()
    response = make_response()

    response = jsonify({"resultado":" Se agrego una nueva receta"})
    return response

@app.route("/traer_receta", methods=["GET"])
@cross_origin()
def mostrar_receta():
    #consulta SQL
    sql = "SELECT id_receta, nombre, img, ingredientes, pasos_a_seguir FROM Recetas"

    #crear el cursor
    cursor = mysql.connection.cursor()#mysql.connect.cursor()
    cursor.execute(sql)

    resultado = cursor.fetchall()

    #cerrar la conexión
    cursor.close()
    response = make_response()

    if resultado == None:
        response = jsonify({"mensaje":None})
        return response
    else:
        usuarios = []

        for i in resultado:

            p = {"id":i[0], "nombre":i[1], "contraseña":i[2], "email":i[3]}
            usuarios.append(p)

        return jsonify(usuarios)


@cross_origin
@app.route("/eliminar_usuario/<id>", methods=["DELETE"])
def eliminar_usuario(id):

    sql = "DELETE FROM Usuarios WHERE idUsuarios=%s"

    #crear el cursor
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (id,))

    mysql.connection.commit()

    #cerrar la conexión
    cursor.close()
    response = make_response()


    response = jsonify({"resultado":"Usuario eliminado"})
    return response


@cross_origin
@app.route("/actualizar_usuario/<id>", methods=["PUT"])
def actualizar_usuario(id):
    nombre = request.json["nom"]
    apellido = request.json["ape"]

    sql = "UPDATE Usuarios SET nombre=%s,apellido=%s WHERE idUsuarios=%s"

    #crear el cursor
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (nombre,apellido,id))
    mysql.connection.commit()


    #cerrar la conexión
    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Usuario no activo"})
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)