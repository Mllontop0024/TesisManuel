from .entidades.Tomate import Tomate
from util import CustomJsonEncoder
import json

class Modeltomate():
    @classmethod
    def insertarTomate(self,db,tomate):
        
        cursor=db.connection.cursor()

        cursor1=db.connection.cursor()

        sql1="SELECT COALESCE(MAX(t.id_tomate)+1,1) AS id from tomate AS t"

        cursor1.execute(sql1)
        datos=cursor1.fetchone()

        sql = "INSERT INTO tomate (id_tomate, fecha_registro, foto, id_usuario) VALUES (%s, CURRENT_DATE, LOAD_FILE(%s), %s)"
        values = (datos[0], tomate.foto, tomate.id_usuario)
        
        try:
            
            cursor.execute(sql,values)

            db.connection.commit()

            return json.dumps({'status':True,'data':'Tomate Registrado Correctamente','datos':datos[0]})
        
        except Exception as ex:
            raise Exception(ex)
    