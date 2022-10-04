from sqlite3 import Cursor
from flask import Flask
from flask import render_template, request, jsonify, redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

#inicializando flask ¿para que __name__ ?
app= Flask(__name__)

#conectando flask con la base de datos
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB']= 'institucion'
mysql.init_app(app)

#conectando app con os para editar fotos
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#acceso a la carpeta por parte de flask

@app.route('/preguntas', methods=['GET'])
def listar_preguntas():
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
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
        conn=mysql.connect()
        cursor=conn.cursor()
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
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="INSERT INTO preguntas (docente, categoria, subcategoria, cuerpo_pregunta, respuesta_correcta, respuesta_incorrecta_1, respuesta_incorrecta_2, respuesta_incorrecta_3, imagen, observaciones) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')".format(request.json['docente'], request.json['categoria'], request.json['subcategoria'], request.json['cuerpo_pregunta'], request.json['respuesta_correcta'], request.json['respuesta_incorrecta_1'], request.json['respuesta_incorrecta_2'], request.json['respuesta_incorrecta_3'], request.json['imagen'], request.json['observaciones'])
        cursor.execute(sql)
        conn.commit()
        return jsonify({'mensaje':"Pregunta Registrada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})

@app.route('/preguntas/<id_pregunta>', methods=['DELETE'])
def eliminar_pregunta(id_pregunta):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="DELETE FROM preguntas WHERE id_pregunta= '{0}'".format(id_pregunta)
        cursor.execute(sql)
        conn.commit()
        return jsonify({'mensaje':"Pregunta Eliminada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})

@app.route('/preguntas/<id_pregunta>', methods=['PUT'])
def actualizar_pregunta(id_pregunta):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        sql="UPDATE preguntas SET docente='{0}', categoria='{1}', subcategoria='{2}', cuerpo_pregunta='{3}', respuesta_correcta='{4}', respuesta_incorrecta_1='{5}', respuesta_incorrecta_2='{6}', respuesta_incorrecta_3='{7}', imagen='{8}', observaciones='{9}' WHERE id_pregunta='{10}'".format(request.json['docente'], request.json['categoria'], request.json['subcategoria'], request.json['cuerpo_pregunta'], request.json['respuesta_correcta'], request.json['respuesta_incorrecta_1'], request.json['respuesta_incorrecta_2'], request.json['respuesta_incorrecta_3'], request.json['imagen'], request.json['observaciones'], id_pregunta)
        cursor.execute(sql)
        conn.commit()
        return jsonify({'mensaje':"Pregunta Actualizada"})
    except Exception as ex:
        return jsonify({'mensaje':"ERROR"})

def pagina_no_encontrada(error):
    return "<h1>la pagina que intentas buscar no existe</h1>", 404

#metodos JSON
@app.route('/uploads/<nombreImagen>')
def uploads(nombreImagen):
    return send_from_directory(app.config['CARPETA'],nombreImagen)

@app.route('/')
def index():
    #muetra todos los resultados en raiz    
    sql="SELECT * FROM preguntas;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)    
    preguntas=cursor.fetchall()   
    conn.commit()
    return render_template('index.html', preguntas=preguntas)

@app.route('/destroy/<int:id_pregunta>')
def destroy(id_pregunta):
    #elimina el id de base de datos llamando el metodo "destroy" y retorna a raiz
    conn=mysql.connect()
    cursor=conn.cursor()
    
    #elimina la foto
    cursor.execute("SELECT imagen FROM preguntas WHERE id_pregunta=%s", id_pregunta)
    fila=cursor.fetchall()
    if fila[0][0]!='':
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    
    #guara cambios en BD
    cursor.execute("DELETE FROM preguntas WHERE id_pregunta=%s",(id_pregunta))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id_pregunta>')
def edit(id_pregunta):
    #modifica id llamando el metodo "update" y regresa a raiz    
    conn=mysql.connect()
    cursor=conn.cursor()    
    cursor.execute("SELECT * FROM preguntas WHERE id_pregunta=%s",(id_pregunta))
    preguntas=cursor.fetchall()   
    conn.commit()    
    return render_template('/edit.html', preguntas=preguntas)    

@app.route('/update', methods=['POST'])
def update():
    #modifica los valores de la base de datos
    _docente=request.form['txtDocente']
    _categoria=request.form['txtCategoria']
    _subcategoria=request.form['txtSubCategoria']
    _cuerpo_pregunta=request.form['txtCuerpoPregunta']
    _respuesta_correcta=request.form['txtRespuestaCorrecta']
    _respuesta_incorrecta1=request.form['txtRespuestaIncorrecta1']
    _respuesta_incorrecta2=request.form['txtRespuestaIncorrecta2']
    _respuesta_incorrecta3=request.form['txtRespuestaIncorrecta3']
    _imagen=request.files['txtImagen']
    _observaciones=request.form['txtObservaciones']
    id_pregunta=request.form['txtIDPregunta']    
    sql="UPDATE preguntas SET docente=%s, categoria=%s, subcategoria=%s, cuerpo_pregunta=%s, respuesta_correcta=%s, respuesta_incorrecta_1=%s, respuesta_incorrecta_2=%s, respuesta_incorrecta_3=%s, observaciones=%s WHERE id_pregunta=%s;"
    datos=(_docente, _categoria, _subcategoria, _cuerpo_pregunta, _respuesta_correcta, _respuesta_incorrecta1, _respuesta_incorrecta2, _respuesta_incorrecta3, _observaciones, id_pregunta)    
    conn=mysql.connect()
    cursor=conn.cursor()
    
    #modifica el archivo foto de la base de datos
    now=datetime.now()
    tiempo=now.strftime(r"%Y%m%d")    
    if _imagen.filename!='':
        nuevoNombreImagen=tiempo+_imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
        cursor.execute("SELECT imagen FROM preguntas WHERE id_pregunta=%s", id_pregunta)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE preguntas SET imagen=%s WHERE id_pregunta=%s", (nuevoNombreImagen, id_pregunta))
        conn.commit()
    else:
        nuevoNombreImagen=''
    
    #manda todos los cambien y devuelve a raiz
    cursor.execute(sql,datos)
    conn.commit()    
    return redirect('/') 

@app.route('/create')
def create():
    #manda a pagina creat donde se usa el metodo "store"
    return render_template('create.html')

@app.route('/store', methods=['POST'])
def storage():
    #toma los valores del formulario y la fecha actual para guardarlos en base de datos
    _docente=request.form['txtDocente']
    _categoria=request.form['txtCategoria']
    _subcategoria=request.form['txtSubCategoria']
    _cuerpo_pregunta=request.form['txtCuerpoPregunta']
    _respuesta_correcta=request.form['txtRespuestaCorrecta']
    _respuesta_incorrecta1=request.form['txtRespuestaIncorrecta1']
    _respuesta_incorrecta2=request.form['txtRespuestaIncorrecta2']
    _respuesta_incorrecta3=request.form['txtRespuestaIncorrecta3']
    _imagen=request.files['txtImagen']
    _observaciones=request.form['txtObservaciones']

    #comprobacion de campos vacios    
    if _cuerpo_pregunta=='' or _respuesta_correcta=='' or _observaciones=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))
    
    now=datetime.now()
    tiempo=now.strftime(r"%Y%m%d")    
    
    #guarda la foto
    if _imagen.filename!='':
        nuevoNombreImagen=tiempo+_imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
    else:
        nuevoNombreImagen=''

    #guarda todo en BD y manda a raiz
    sql="INSERT INTO preguntas (id_pregunta, docente, categoria, subcategoria, cuerpo_pregunta, respuesta_correcta, respuesta_incorrecta_1, respuesta_incorrecta_2, respuesta_incorrecta_3, imagen, observaciones) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    datos=(_docente, _categoria, _subcategoria, _cuerpo_pregunta, _respuesta_correcta, _respuesta_incorrecta1, _respuesta_incorrecta2, _respuesta_incorrecta3, nuevoNombreImagen, _observaciones)      
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()    
    return redirect('/')

#metodo principal ¿para que son esos datos?
if __name__=='__main__':
    app.register_error_handler(404,pagina_no_encontrada)
    app.run(debug=True)