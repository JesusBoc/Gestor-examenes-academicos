from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app= Flask(__name__)
conexion= MySQL(app)

@app.route('/preguntas', methods=['GET'])
def listar_preguntas():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id_pregunta, docente, categoria, subcategoria, cuerpo_pregunta, respuesta_correcta, respuesta_incorrecta_1, respuesta_incorrecta_2, respuesta_incorrecta_3, imagen, observaciones FROM preguntas"
        cursor.execute(sql)
        datos=cursor.fetchall()
        preguntas=[]
        for fila in datos:
            pregunta={'id_pregunta': fila[0],
                      'docente': fila[1],
                      'categoria':fila[2],
                      'subcategoria':fila[3],
                      'cuerpo_pregunta':fila[4],
                      'respuesta_correcta':fila[5],
                      'respuesta_incorrecta_1':fila[6],
                      'respuesta_incorrecta_2':fila[7],
                      'respuesta_incorrecta_3':fila[8],
                      'imagen':fila[9],
                      'observaciones':fila[10]
                      }
            preguntas.append(pregunta)
            
        return jsonify({'preguntas':preguntas,'mensaje':"Preguntas listadas"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"}) 


@app.route('/preguntas/<id_pregunta>', methods=['GET'])
def leer_pregunta(id_pregunta):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT docente, categoria, subcategoria, cuerpo_pregunta, respuesta_correcta, respuesta_incorrecta_1, respuesta_incorrecta_2, respuesta_incorrecta_3, imagen, observaciones FROM preguntas WHERE id_pregunta= '{0}'".format(id_pregunta)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos!= None:
            pregunta={'id_pregunta': id_pregunta,
                      'docente': datos[0],
                      'categoria': datos[1],
                      'subcategoria': datos[2],
                      'cuerpo_pregunta': datos[3],
                      'respuesta_correcta': datos[4],
                      'respuesta_incorrecta_1': datos[5],
                      'respuesta_incorrecta_2': datos[6],
                      'respuesta_incorrecta_3': datos[7],
                      'imagen': datos[8],
                      'observaciones': datos[9]
                      }
            return jsonify({'preguntas':pregunta,'mensaje':"pregunta encontrada"})
        else:
            return jsonify({'mensaje':"pregunta no encontrada"})           
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})


@app.route('/preguntas', methods=['POST'])
def registrar_pregunta():
    try:
        cursor=conexion.connection.cursor()
        sql="INSERT INTO preguntas (docente, categoria, subcategoria, cuerpo_pregunta, respuesta_correcta, respuesta_incorrecta_1, respuesta_incorrecta_2, respuesta_incorrecta_3, imagen, observaciones) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(request.json['docente'], request.json['categoria'], request.json['subcategoria'], request.json['cuerpo_pregunta'], request.json['respuesta_correcta'], request.json['respuesta_incorrecta_1'], request.json['respuesta_incorrecta_2'], request.json['respuesta_incorrecta_3'], request.json['imagen'], request.json['observaciones'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Pregunta Registrada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})


@app.route('/preguntas/<id_pregunta>', methods=['DELETE'])
def eliminar_pregunta(id_pregunta):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM preguntas WHERE id_pregunta= '{0}'".format(id_pregunta)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Pregunta Eliminada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})

@app.route('/preguntas/<id_pregunta>', methods=['PUT'])
def actualizar_pregunta(id_pregunta):
    try:
        cursor=conexion.connection.cursor()
        sql="UPDATE preguntas SET docente='{0}', categoria='{1}', subcategoria='{2}', cuerpo_pregunta='{3}', respuesta_correcta='{4}', respuesta_incorrecta_1='{5}', respuesta_incorrecta_2='{6}', respuesta_incorrecta_3='{7}', imagen='{8}', observaciones='{9}' WHERE id_pregunta='{10}'".format(request.json['docente'], request.json['categoria'], request.json['subcategoria'], request.json['cuerpo_pregunta'], request.json['respuesta_correcta'], request.json['respuesta_incorrecta_1'], request.json['respuesta_incorrecta_2'], request.json['respuesta_incorrecta_3'], request.json['imagen'], request.json['observaciones'], id_pregunta)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Pregunta Actualizada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})
     

def pagina_no_encontrada(error):
    return "<h1>la pagina que intentas buscar no existe</h1>", 404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()