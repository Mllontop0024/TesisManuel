#Import necessary libraries
from flask import Flask, jsonify, render_template, request,url_for,redirect,flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager,login_user,logout_user,login_required
import numpy as np
import os
from PIL import Image
from config import config
import json
import base64


#from tensorflow.keras.preprocessing.image import load_img,img_to_array
#from tensorflow.keras.models import load_model

from tensorflow.keras.utils import load_img,img_to_array
from keras.models import load_model

#Models
from models.Modelusuario import Modelusuario
from models.Modeltomate import Modeltomate
from models.Modelcontrol import Modelcontrol
from models.Modelseguimiento import Modelseguimiento
from models.Modelplaga import Modelplaga

#Entidades
from models.entidades.Usuario import Usuario
from models.entidades.Tomate import Tomate
from models.entidades.Control import Control
from models.entidades.Seguimiento import Seguimiento
from models.entidades.Plaga import Plaga


app = Flask(__name__)

csrf=CSRFProtect()

db= MySQL(app)
login_manager_app=LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return Modelusuario.get_by_id(db,id)

#Conectando a la Red Neuronal Convolucional creada
modelo8='D:/modelos/modeloResNet4.h5'
modelo9='D:/Ciclo X/Plant-Leaf-Disease-Prediction-main/modelos'

cnn=load_model(modelo9)

print("Modelos Cargados Exitosamente")

def prediccion_tomate(hoja_tomate):
  print("@@ Imagen obtenida para predicción")

  # Cargar la imagen
  test_image = load_img(hoja_tomate, target_size = (224, 224)) # load image
  test_image = img_to_array(test_image)/225.0 # convert image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0)

  resultadoP = cnn.predict(test_image)# predict diseased palnt or not
  respuestaP = np.argmax(resultadoP)
  porcentaje=str(np.max(resultadoP)*100)+"%"
  print("Resultado= ",respuestaP)
  print("probabilidad de acierto:"+porcentaje)


  if respuestaP==0:
      return "Tomate con la plaga de la Araña Roja",porcentaje,1,'Tomato___Spider_mites .JPG'
  elif respuestaP==1:
      return "No es un tomate",porcentaje,2,'no_tomate.png'
  elif respuestaP==2:
      return "Tomate Sano",porcentaje,3,'Tomato___healthy .JPG'

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')
def error(error):
    return "<h1>La página que intentas buscar no existe...</h1>"

@app.route("/sesion", methods=['GET', 'POST'])
@login_required
def sesion():
    return render_template('indexSesion.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@app.route("/sabermas", methods=['GET', 'POST'])
def sabermas():
    return render_template('sabermas.html')

@app.route("/sabermas2", methods=['GET', 'POST'])
def sabermas2():
    return render_template('sabermas2.html')

@app.route("/prueba", methods=['GET', 'POST'])
@login_required
def prueba():
    return render_template('prueba.html')

@app.route("/prueba2/<string:id>", methods=['GET', 'POST'])
@login_required
def prueba2(id):
    try:
        cursor=db.connection.cursor()
        sql="SELECT s.id_tomate, s.fecha_seguimiento, s.estado FROM seguimiento AS s INNER JOIN (SELECT id_tomate, MAX(fecha_seguimiento) AS max_fecha FROM seguimiento GROUP BY id_tomate) AS m ON s.id_tomate = m.id_tomate AND s.fecha_seguimiento = m.max_fecha inner join tomate as h on h.id_tomate=s.id_tomate WHERE h.id_usuario={0} group by 1;".format(id)
        cursor.execute(sql)
        datos_hojas=cursor.fetchall()
        cursor.close()
        return render_template('prueba.html',hojas=datos_hojas)
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect('/')

@app.route("/continuarSeguimiento/<string:id_tomate>", methods=['GET', 'POST'])
@login_required
def continuarSeguimiento(id_tomate):
    try:
        
        cursor=db.connection.cursor()
        sql="SELECT s.id_seg,s.id_tomate,s.fecha_seguimiento,s.estado FROM seguimiento as s where s.id_tomate={0}".format(id_tomate)
        cursor.execute(sql)
        datos_tomates_seguimiento=cursor.fetchall()
        cursor.close()
        return render_template('continuarSeguimiento.html',hojas_seguimiento=datos_tomates_seguimiento)

    except Exception as ex:
        print(f"Error : {ex}")


@app.route("/verSeguimiento/<string:id_tomate>", methods=['GET', 'POST'])
@login_required
def verSeguimiento(id_tomate):
    try:
        cursor=db.connection.cursor()
        sql="SELECT s.id_seg,s.id_tomate,s.fecha_seguimiento,s.estado FROM seguimiento as s where s.id_tomate={0}".format(id_tomate)
        cursor.execute(sql)
        datos_tomates_seguimiento=cursor.fetchall()
        cursor.close()
        return render_template('verSeguimiento.html',hojas_seguimiento=datos_tomates_seguimiento)
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect('/')



@app.route("/gestionarAgricultores", methods=['GET','POST'])
@login_required
def gestionarAgricultores():
    try:
        cursor=db.connection.cursor()
        sql="SELECT * from usuario where tipo_usuario=1" 
        cursor.execute(sql)
        datos_seguimiento=cursor.fetchall()
        print(datos_seguimiento)
        cursor.close()
        return render_template('gestionarAgricultores.html',datos=datos_seguimiento)
        
    except Exception as ex:
        print(f"Error : {ex}")


@app.route("/gestionarAdministradores", methods=['GET','POST'])
@login_required
def gestionarAdministradores():
    try:
        cursor=db.connection.cursor()
        sql="SELECT * from usuario where tipo_usuario=2" 
        cursor.execute(sql)
        datos_seguimiento=cursor.fetchall()
        print(datos_seguimiento)
        cursor.close()
        return render_template('gestionarAdministradores.html',datos=datos_seguimiento)
        
    except Exception as ex:
        print(f"Error : {ex}")


@app.route("/editarUsuario/<string:id_usuario>", methods=['GET', 'POST'])
@login_required
def editarUsuario(id_usuario):
    try:
        cursor=db.connection.cursor()
        sql="SELECT * FROM usuario where id_usuario={0}".format(id_usuario)
        cursor.execute(sql)
        datos_usuario=cursor.fetchone()
        cursor.close()
                
        return render_template('editarAgricultor.html',datos_u=datos_usuario)
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect('/')

@app.route("/actualizarUsuario", methods=['POST'])
@login_required
def actualizarUsuario():
    if request.method == 'POST':
        id=request.form['id']
        nombre=request.form['nombre']
        apellidos=request.form['apel']
        correo=request.form['cor']
        nombre_campo=request.form['campo']
        contrasena=request.form['contrasena']
        contrasenaN=request.form['contrasenaN']
        conH=request.form['conH']
        
        co1=Usuario.check_password(conH,contrasena)
        if co1:
            usu=Usuario(id,nombre,apellidos,correo,nombre_campo,contrasenaN)
            rptaJSON=Modelusuario.actualizarUsuarioN(db,usu)
            datos_cliente=json.loads(rptaJSON)
            flash(datos_cliente)
            return redirect(url_for('gestionarAgricultores'))
        else:
            flash("Las contraseñas no coinciden")
            return render_template("index.html")
    else:
        flash("No se puede registrar al usuario...")
        return render_template("index.html")


@app.route("/verResultado/<string:id_seg>", methods=['GET','POST'])
@login_required
def verResultado(id_seg):
    try:
        cursor=db.connection.cursor()
        sql="SELECT s.id_tomate,s.id_control,s.diagnostico,s.porcen_fiabilidad,s.fecha_seguimiento,DATE_ADD(s.fecha_seguimiento, INTERVAL c.cantidad_dias DAY) as fecha_fin_seguimiento,c.nombre,c.modo_accion,c.dosis,c.cantidad_dias,s.foto_hoja,s.estado FROM seguimiento as s INNER join control as c on s.id_control=c.id_control where s.id_seg={0}".format(id_seg)
        #sql="SELECT s.id_seg,s.id_hoja,s.fecha_seguimiento,s.estado FROM seguimiento as s where s.id_seg={}".format(id_seg)
        cursor.execute(sql)
        datos_seguimiento=cursor.fetchone()
        #print(datos_seguimiento[10])
        img1 = base64.b64encode(datos_seguimiento[10]).decode('utf-8')
        cursor.close()
        return render_template('modelS.html',datos=datos_seguimiento, imagen= img1)
        
    except Exception as ex:
        print(f"Error : {ex}")

@app.route("/eliminarHoja/<string:id>", methods=['GET', 'POST'])
@login_required
def eliminarHoja(id):
    try:
        cursor=db.connection.cursor()
        sql="delete from seguimiento where id_tomate={0}".format(id)
        sql1="delete from tomate where id_tomate={0}".format(id)
        cursor.execute(sql)
        cursor.execute(sql1)
        db.connection.commit()
        return render_template("indexSesion.html")
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect("/")
    
@app.route("/eliminarUsuario/<string:id>", methods=['GET', 'POST'])
@login_required
def eliminarUsuario(id):
    try:
        cursor=db.connection.cursor()
        sql="delete from usuario where id_usuario={0}".format(id)
        cursor.execute(sql)
        db.connection.commit()
        return redirect(url_for('gestionarAgricultores'))
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect("/")

@app.route("/eliminarUsuarioA/<string:id>", methods=['GET', 'POST'])
@login_required
def eliminarUsuarioA(id):
    try:
        cursor=db.connection.cursor()
        sql="delete from usuario where id_usuario={0}".format(id)
        cursor.execute(sql)
        db.connection.commit()
        return redirect(url_for('gestionarAdministradores'))
    except Exception as ex:
        flash("Ha ocurrido un error en el sistema")
        return redirect("/")

#EJEMPLO DE LISTAR
@app.route("/tratamientos")
def listar_trat():
    data={}
    try:
        cursor=db.connection.cursor()
        sql="select * from control"
        cursor.execute(sql)
        cursos=cursor.fetchall()
        data['mensaje']='exito'
    except Exception as ex:
        data['mensaje']='error...'
    return jsonify(data)


# Registro de usuarios Agricultores Login
@app.route('/regisUsu',methods=['POST'])
def regisUsu():
    if request.method == 'POST':
        correo=request.form['correo']
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        nombre_campo=request.form['nombre_campo']
        contrasena=request.form['contrasena']
        confirmarContrasena=request.form['confirmarContrasena']
        
        if contrasena==confirmarContrasena:
            usu=Usuario(0,nombre,apellidos,correo,nombre_campo,contrasena)
            rptaJSON=Modelusuario.insertarUsuarioN(db,usu)
            datos_cliente=json.loads(rptaJSON)
            flash(datos_cliente)
            return render_template("index.html")
        else:
            flash("Las contraseñas no coinciden")
            return render_template("index.html")
    else:
        flash("No se puede registrar al usuario...")
        return render_template("index.html")


# Registro de usuarios Agricultores- Administrador
@app.route('/regisUsuAgri',methods=['POST'])
def regisUsuAgri():
    if request.method == 'POST':
        correo=request.form['correo']
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        nombre_campo=request.form['nombre_campo']
        contrasena=request.form['contrasena']
        confirmarContrasena=request.form['confirmarContrasena']
        
        if contrasena==confirmarContrasena:
            usu=Usuario(0,nombre,apellidos,correo,nombre_campo,contrasena)
            rptaJSON=Modelusuario.insertarUsuarioN(db,usu)
            datos_cliente=json.loads(rptaJSON)
            flash(datos_cliente)
            return redirect(url_for('gestionarAgricultores'))
        else:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('gestionarAgricultores'))
    else:
        flash("No se puede registrar al usuario...")
        return redirect(url_for('gestionarAgricultores'))

# Registro de usuarios Administradores- Administrador
@app.route('/regisUsuA',methods=['POST'])
def regisUsuA():
    if request.method == 'POST':
        correo=request.form['correo']
        nombre=request.form['nombre']
        apellidos=request.form['apellidos']
        contrasena=request.form['contrasena']
        confirmarContrasena=request.form['confirmarContrasena']
        
        if contrasena==confirmarContrasena:
            usu=Usuario(0,nombre,apellidos,correo,None,contrasena)
            rptaJSON=Modelusuario.insertarUsuarioA(db,usu)
            datos_cliente=json.loads(rptaJSON)
            flash(datos_cliente)
            return redirect(url_for('gestionarAdministradores'))
        else:
            flash("Las contraseñas no coinciden")
            return redirect(url_for('gestionarAdministradores'))
    else:
        flash("No se puede registrar al usuario...")
        return redirect(url_for('gestionarAdministradores'))



# Registro de usuarios
@app.route("/logueo", methods = ['GET','POST'])
def logueo():
    if request.method == 'POST':
       correo = request.form['correoL'] 
       contra = request.form['contrasenaL'] 
       tipoU = request.form['tipoU'] 
       usu=Usuario(0,None,None,correo,None,contra,tipoU)

       logueado=Modelusuario.login(db,usu)
       print(logueado)
       if logueado:
            if logueado.con:
                login_user(logueado)
                if tipoU=='1':
                    return render_template("indexSesion.html")
                elif tipoU=='2':
                    return render_template("indexAdmin.html")
            else:
                flash("Contraseña inválida...")
                return render_template("index.html")
       else:
            flash("Usuario no encontrado en la base de datos")
            return render_template("index.html")
        
    else:
       flash("Error al acceder")
       return render_template("index.html")
    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/protected")
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"
def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1>Página No Encontrada</h1>", 404


# Registro del primer seguimiento
@app.route("/regisSegui", methods = ['GET','POST'])
@login_required
def regisSegui():
    if request.method == 'POST':
       id_tomate = request.form['id_hoja'] 
       diagnostico = request.form['diagnostico'] 
       porc = request.form['porcen_fia'] 
       imagen_tomate = request.form['imagen_hoja'] 
       id_control = request.form['id']

      
       if diagnostico=="Tomate Sano":
        
        seg=Seguimiento(0,id_tomate,id_control,None,'T',diagnostico,porc,imagen_tomate)
        segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
        print(segInsertado)
        if segInsertado:
            flash("Seguimiento insertado correctamente...")
            return render_template("indexSesion.html")
        else:
            flash("No se ha podido insertar la hoja")
            return render_template("indexSesion.html")
       elif diagnostico=="No es un tomate":
            seg=Seguimiento(0,id_tomate,id_control,None,'T',diagnostico,porc,imagen_tomate)
            
            segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
            return render_template("indexSesion.html")
       else:
        
        seg=Seguimiento(0,id_tomate,id_control,None,'S',diagnostico,porc,imagen_tomate)
        segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
        #print(segInsertado)
        if segInsertado:
            flash("Seguimiento insertado correctamente...")
            return render_template("indexSesion.html")
        else:
            flash("No se ha podido insertar el tomate")
            return render_template("indexSesion.html")  
    else:
       return render_template("indexSesion.html")


#CONTINUAR SEGUIMIENTO DE LA HOJA
@app.route("/segH", methods = ['GET','POST'])
@login_required
def segH():
    if request.method == 'POST':
       file = request.files['image'] 
       id_ho = request.form['id_ho']
       
       filename = file.filename        
       #print("@@ Input posted = ", file)
        
       file_path = os.path.join('D:/Ciclo X/Plant-Leaf-Disease-Prediction-main/src/static/upload/fotos/', filename)
       
       file.save(file_path)
       print(file_path)
       
       print("@@ Predicting class......")
       pred, porcen,id_enfer,foto_base = prediccion_tomate(hoja_tomate=file_path)

       control=Control(0,None,None,None,None,id_enfer,None)
       lista_controles=Modelcontrol.listarcontrolsegunplaga(db,control)
       if lista_controles:
           return render_template("seguimiento2.html",foto_base=foto_base, pred_output = pred, user_image = file_path,porc=porcen,foto=filename,trat=lista_controles,id_hoja=id_ho)
       else:    
           return render_template("seguimiento2.html",foto_base=foto_base, pred_output = pred, user_image = file_path,porc=porcen,foto=filename,id_hoja=id_ho)
       
    else:
       return render_template("indexSesion.html")



@app.route("/regisSegui2", methods = ['GET','POST'])
@login_required
def regisSegui2():
    if request.method == 'POST':
       id_tomate = request.form['id_hoja'] 
       diagnostico = request.form['diagnostico'] 
       
       porc = request.form['porcen_fia'] 
       imagen_tomate = request.form['imagen_hoja'] 
       
       id_control = request.form['id']
       #En seguimiento: S; Terminado: T
       if diagnostico=="Tomate Sano":
        
        seg=Seguimiento(0,id_tomate,id_control,None,'T',diagnostico,porc,imagen_tomate)
        segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
        #print(segInsertado)
        if segInsertado:
            flash("Seguimiento insertado correctamente...")
            return render_template("indexSesion.html")
        else:
            flash("No se ha podido insertar el tomate")
            return render_template("indexSesion.html")
       elif diagnostico=="No es un tomate":
            seg=Seguimiento(0,id_tomate,id_control,None,'T',diagnostico,porc,imagen_tomate)
            segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
            return render_template("indexSesion.html")
            #return render_template("indexSesion.html")
       else:
        
        seg=Seguimiento(0,id_tomate,id_control,None,'S',diagnostico,porc,imagen_tomate)
        segInsertado=Modelseguimiento.insertarSeguimiento(db,seg)
        #print(segInsertado)
        if segInsertado:
            flash("Seguimiento insertado correctamente...")
            return render_template("indexSesion.html")
        else:
            flash("No se ha podido insertar el tomate")
            return render_template("indexSesion.html")  
    else:
       return render_template("indexSesion.html")


# Predicción con foto de la hoja
@app.route("/predict", methods = ['GET','POST'])
@login_required
def predict():
    if request.method == 'POST':
       file = request.files['image'] 
       correo = request.form['correoP'] 
       imagen_original = Image.open(file)

       # Redimensionar la foto
       imagen_redimensionada = imagen_original.resize((512, 512))
       
       
       filename = file.filename        
       print("@@ Input posted = ", file)
        

       file_path = os.path.join('D:/Ciclo X/Plant-Leaf-Disease-Prediction-main/src/static/upload/fotos/', filename)
       #file.save(file_path)
       imagen_redimensionada.save(file_path)
       print(file_path)

       print("@@ Predicting class......")
       pred, porcen,id_plaga,foto_base = prediccion_tomate(hoja_tomate=file_path)

       tomate=Tomate(0,None,file_path,correo)
       insertado=Modeltomate.insertarTomate(db,tomate)
       datos=json.loads(insertado)
       if insertado:
            flash("Tomate insertada correctamente...")
            control=Control(0,None,None,None,None,id_plaga,None)
            lista_controles=Modelcontrol.listarcontrolsegunplaga(db,control)
            
            if lista_controles:
                return render_template("seguimiento.html",foto_base=foto_base, pred_output = pred, user_image = file_path,porc=porcen,foto=filename,trat=lista_controles,id_hoja=datos['datos'])
            else:    
                return render_template("seguimiento.html",foto_base=foto_base, pred_output = pred, user_image = file_path,porc=porcen,foto=filename,id_hoja=datos['datos'])
       else:
            flash("No se ha podido insertar el tomate")
            return render_template("indexSesion.html")
    else:
       return render_template("indexSesion.html")
       

#Reporte 1: Diagnostico por tiempo
import datetime


@app.route("/diagnosticosTiempo", methods=['GET','POST'])
@login_required
def diagnosticosTiempo():
    try:
        cursor=db.connection.cursor()
        sql="SELECT DATE_FORMAT(t.fecha_registro, '%Y-%m') as mes, COUNT(t.fecha_registro) as cantidad FROM tomate as t GROUP BY mes;"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursor.close()


        cursor1=db.connection.cursor()
        sql1="SELECT DATE_FORMAT(t.fecha_registro, '%Y') as año,DATE_FORMAT(t.fecha_registro, '%M') as mes FROM tomate as t GROUP BY mes;"
        cursor1.execute(sql1)
        datosCombo=cursor1.fetchall()
        cursor1.close()


        cursor2=db.connection.cursor()
        sql2="SELECT DATE_FORMAT(t.fecha_registro, '%Y') as año, COUNT(t.fecha_registro) as cantidad FROM tomate as t GROUP BY año;"
        cursor2.execute(sql2)
        datosCombo2=cursor2.fetchall()
        cursor2.close()

        meses = [datetime.datetime.strptime(row[0], '%Y-%m').strftime('%B, %Y') for row in datos]
        cantidades = [row[1] for row in datos]
        return render_template('reporte1.html',labels=meses,values=cantidades,datosCombo=datosCombo,datosCombo2=datosCombo2)
        
    except Exception as ex:
        print(f"Error : {ex}")



@app.route("/diagnosticosTiempoDetallado", methods=['GET','POST'])
@login_required
def diagnosticosTiempoDetallado():
    try:
        if request.method == 'POST':
            mes=request.form['mes']
            anio=request.form['anio']
            
            cursor=db.connection.cursor()
            sql="SELECT h.fecha_registro, COUNT(h.fecha_registro) as cantidad from tomate as h WHERE DATE_FORMAT(h.fecha_registro,'%Y')='{}'and  DATE_FORMAT(h.fecha_registro,'%M')='{}' group by 1;".format(anio,mes)
            cursor.execute(sql)
            datos=cursor.fetchall()
            cursor.close()

            labels = [datetime.datetime.strftime(row[0], '%d-%m-%Y') for row in datos]
            cantidades = [row[1] for row in datos]
            return render_template('reporte1Detallado.html',labels=labels,values=cantidades)
        
        else:
            flash("No se puede filtrar...")
            return render_template("index.html")
            

    except Exception as ex:
        print(f"Error : {ex}")


#REPORTE 2: Diagnostico por usuario

@app.route("/diagnosticosUsuario", methods=['GET','POST'])
@login_required
def diagnosticosUsuario():
    try:
        cursor=db.connection.cursor()
        sql = "SELECT h.id_usuario, CONCAT(u.nombre, ' ', u.apellidos) AS nombre_completo, COUNT(h.id_usuario) AS cantidad FROM tomate AS h INNER JOIN usuario AS u ON u.id_usuario = h.id_usuario GROUP BY h.id_usuario;"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursor.close()

        etiquetas = [row[1] for row in datos]
        cantidades = [row[2] for row in datos]
        return render_template('reporte2.html',labels=etiquetas,values=cantidades,datos=datos)
        
    except Exception as ex:
        print(f"Error : {ex}")


@app.route("/diagnosticosUsuarioDetallado", methods=['GET','POST'])
@login_required
def diagnosticosUsuarioDetallado():
    try:
        if request.method == 'POST':
            usuario=request.form['usuario']
            cursor=db.connection.cursor()
            sql="SELECT DATE_FORMAT(h.fecha_registro, '%Y-%m') as mes, COUNT(h.fecha_registro) as cantidad from tomate as h WHERE h.id_usuario={} group by 1;".format(usuario)
            cursor.execute(sql)
            datos=cursor.fetchall()
            cursor.close()
        
            labels = [datetime.datetime.strptime(row[0], '%Y-%m').strftime('%B, %Y') for row in datos]
            cantidades = [row[1] for row in datos]
            return render_template('reporte2Detallado.html',labels=labels,values=cantidades)
        
        else:
            flash("No se puede filtrar...")
            return render_template("index.html")
            

    except Exception as ex:
        print(f"Error : {ex}")


# Create flask instance
if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()