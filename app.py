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

@app.route("/traer_usuarios", methods=["GET"])
@cross_origin()
def traer_usuarios():
    #consulta SQL
    sql = "SELECT idUsuarios,provincia, nombre FROM Usuarios"

    #crear el cursor
    cursor = mysql.connect.cursor()#mysql.connect.cursor()
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

            p = {"id":i[0], "email":i[1], "nombre":i[2]}
            usuarios.append(p)

        return jsonify(usuarios)


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


###################################################################

#PROYECTO

@app.route("/traer_usuario", methods=["GET"])
@cross_origin()
def traer_usuario():
    #consulta SQL
    sql = "SELECT idusuario, email, nombre, fechaNacimiento FROM usuario"

    #crear el cursor
    cursor = mysql.connect.cursor()#mysql.connect.cursor()
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

            p = {"id":i[0], "email":i[1], "nombre":i[2], "fechaNacimineto":i[3]}
            usuarios.append(p)

        return jsonify(usuarios)
    

@app.route("/nuevo_usuario", methods=["POST"])
@cross_origin()
def nuevo_usuario():
    nombre = request.json["nombre"]
    email = request.json["email"]
    fecha = request.json["fecha_nac"]
    cursor = mysql.connection.cursor()

    sql = "INSERT INTO usuario(nombre, email, fechaNacimiento) values(%s, %s, %s);"
    cursor.execute(sql, (nombre, email, fecha))


    mysql.connection.commit()
 
    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Agregado nuevo usuario"})
    return response

@cross_origin
@app.route("/eliminar_usuarios/<id>", methods=["DELETE"])
def eliminar_usuarios(id):

    sql = "DELETE FROM usuario WHERE idusuario=%s"

    #crear el cursor
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (id,))

    mysql.connection.commit()

    #cerrar la conexión
    cursor.close()
    response = make_response()


    response = jsonify({"resultado":"Usuario eliminado"})
    return response

@app.route("/nueva_publicacion", methods=["POST"])
@cross_origin()
def nueva_publicacion():
    usuario_idusuario = request.json["usuario_idusuario"]
    nombre = request.json["nombre"]
    imagenes = request.json["imagenes"]
    tiempo = request.json["tiempo"]
    ingredientes = request.json["ingredientes"]
    receta = request.json["receta"]
    likes = request.json["likes"]
    dislikes = request.json["dislikes"]
    cantidadComentarios = request.json["cantidadComentarios"]
    cursor = mysql.connection.cursor()

    sql = "INSERT INTO publicacion(usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios))

    mysql.connection.commit()

    cursor.close()
    response = make_response()

    response = jsonify({"resultado":"Publicacion agregada correctamente"})
    return response

@app.route("/consulta_publicacion", methods=["GET"])
@cross_origin()
def consulta_publicacion():
    cursor = mysql.connection.cursor()

    sql = "SELECT idpublicacion, usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios FROM publicacion;"
    cursor.execute(sql)
    datos = cursor.fetchall()

    cursor.close()
    response = make_response()

    response = jsonify(datos)
    return response


@app.route("/consulta_publicacion/<id>", methods=["GET"])
@cross_origin()
def consulta_publicacion_por_id(id):
    cursor = mysql.connection.cursor()

    sql = "SELECT idpublicacion, usuario_idusuario, nombre, imagenes, tiempo, ingredientes, receta, likes, dislikes, cantidadComentarios FROM publicacion WHERE idpublicacion = %s;"
    cursor.execute(sql, (id,))
    datos = cursor.fetchall()

    cursor.close()
    response = make_response()

    response = jsonify(datos)
    return response



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)