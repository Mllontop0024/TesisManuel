from werkzeug.security import check_password_hash,generate_password_hash
from .entidades.Usuario import Usuario
from util import CustomJsonEncoder
import json
class Modelusuario():
    @classmethod
    def login(self,db,usuario):
        try:
            cursor=db.connection.cursor()
            sql="""select id_usuario,nombre,apellidos,correo,tipo_usuario,nombre_campo,contrasena from usuario where correo='{}' and tipo_usuario={}""".format(usuario.cor,usuario.tipou)
            cursor.execute(sql)
            datos=cursor.fetchone()
            
            if datos:
                ver=Usuario.check_password(datos[6],usuario.con)
                if ver==True:
                    usu=Usuario(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6])
                    if usu:
                        return usu
                    else:
                        return json.dumps({'status':True,'data':'Datos no encontrados'})
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql="""select id_usuario,nombre,apellidos,correo,tipo_usuario,nombre_campo,contrasena from usuario where id_usuario={}""".format(id)
            cursor.execute(sql)
            datos=cursor.fetchone()
            
            if datos:
                usu=Usuario(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6])
                return usu
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def insertarUsuarioN(self,db,usuario):
        cursor=db.connection.cursor()
        cursor1=db.connection.cursor()
        cursor2=db.connection.cursor()

        sql1="SELECT COALESCE(MAX(u.id_usuario)+1,1) AS id from usuario AS u"
        cursor1.execute(sql1)
        datos=cursor1.fetchone()
        
        cursor1.close()

        sql2="SELECT id_usuario,nombre,apellidos,correo,nombre_campo,contrasena,tipo_usuario from usuario where correo='{}'". format(usuario.cor)
        cursor2.execute(sql2)
        datosVal=cursor2.fetchone()
        
        cursor2.close()

        if datosVal:
            return json.dumps({'status':False,'data':'Correo ya registrado con anterioridad'})
        else:
            sql="INSERT INTO usuario(id_usuario,nombre,apellidos,correo,nombre_campo,contrasena,tipo_usuario) VALUES ({},'{}','{}','{}','{}','{}',1)".format(datos[0],usuario.nom,usuario.ape,usuario.cor,usuario.cam,generate_password_hash(usuario.con))
            try:
                cursor.execute(sql)
                db.connection.commit()

                return json.dumps({'status':True,'data':'Usuario Registrado Correctamente'})
            
            except Exception as ex:
                raise Exception(ex)


        
        

    @classmethod
    def insertarUsuarioA(self,db,usuario):
        cursor=db.connection.cursor()
        cursor1=db.connection.cursor()
        cursor2=db.connection.cursor()

        sql1="SELECT COALESCE(MAX(u.id_usuario)+1,1) AS id from usuario AS u"
        cursor1.execute(sql1)
        datos=cursor1.fetchone()
        
        cursor1.close()

        sql2="SELECT id_usuario,nombre,apellidos,correo,nombre_campo,contrasena,tipo_usuario from usuario where correo='{}'". format(usuario.cor)
        cursor2.execute(sql2)
        datosVal=cursor2.fetchone()
        
        cursor2.close()

        if datosVal:
            return json.dumps({'status':False,'data':'Correo ya registrado con anterioridad'})
        else:
            sql="INSERT INTO usuario(id_usuario,nombre,apellidos,correo,nombre_campo,contrasena,tipo_usuario) VALUES ({},'{}','{}','{}','{}','{}',2)".format(datos[0],usuario.nom,usuario.ape,usuario.cor,usuario.cam,generate_password_hash(usuario.con))
            try:
                cursor.execute(sql)
                db.connection.commit()

                return json.dumps({'status':True,'data':'Usuario Administrador Registrado Correctamente'})
            
            except Exception as ex:
                raise Exception(ex)

        
    @classmethod
    def actualizarUsuarioN(self,db,usuario):
        cursor=db.connection.cursor()

        sql="update usuario set nombre='{}',apellidos='{}',correo='{}',nombre_campo='{}',contrasena='{}' where id_usuario={}".format(usuario.nom,usuario.ape,usuario.cor,usuario.cam,generate_password_hash(usuario.con),usuario.id)
        try:
            cursor.execute(sql)
            db.connection.commit()

            return json.dumps({'status':True,'data':'Usuario Actualizado Correctamente'})
        
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def insertarUsuarioG(self,db,usuario):
        
        cursor=db.connection.cursor()

        cursor1=db.connection.cursor()

        sql1="SELECT COALESCE(MAX(u.id_usuario)+1,1) AS id from usuario AS u"

        cursor1.execute(sql1)
        datos=cursor1.fetchone()
        
        cursor1.close()

        sql="INSERT INTO usuario(id_usuario,nombre,apellidos,correo,nombre_campo,contrasena,tipo_usuario) VALUES ({},'{}','{}','{}','{}','{}','{}',{})".format(datos[0],usuario.nom,usuario.ape,usuario.cor,usuario.cam,generate_password_hash(usuario.con),usuario.tipou)
        try:
            cursor.execute(sql)
            db.connection.commit()

            return json.dumps({'status':True,'data':'Usuario Registrado Correctamente'})
        
        except Exception as ex:
            raise Exception(ex)