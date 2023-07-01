from .entidades.Seguimiento import Seguimiento
from util import CustomJsonEncoder
import json

class Modelseguimiento():
    @classmethod
    def insertarSeguimiento(self,db,seguimiento):
        
        cursor=db.connection.cursor()

        cursor1=db.connection.cursor()

        sql1="SELECT COALESCE(MAX(s.id_seg)+1,1) AS id from seguimiento AS s"

        cursor1.execute(sql1)
        datos=cursor1.fetchone()
        cursor1.close()
        
        sql = "INSERT INTO seguimiento (id_seg, id_tomate, id_control, fecha_seguimiento, estado, diagnostico, porcen_fiabilidad, foto_hoja) VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s, LOAD_FILE(%s))"
        values = (datos[0], seguimiento.id_tomate, seguimiento.id_control, seguimiento.estado, seguimiento.diagnostico, seguimiento.porcen_fiab, seguimiento.foto_hoja)
        try:

            cursor.execute(sql, values)
            db.connection.commit()

            return json.dumps({'status':True,'data':'Seguimiento Registrado Correctamente','datos':datos})
        
        except Exception as ex:
            raise Exception(ex)

    