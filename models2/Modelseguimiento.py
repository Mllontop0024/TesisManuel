from .entidades.Seguimiento import Seguimiento
from util import CustomJsonEncoder
import json


class Modelseguimiento:
    @classmethod
    def insertarSeguimiento(self, db, seguimiento):
        cursor = db.connection.cursor()

        cursor1 = db.connection.cursor()
        cursor2 = db.connection.cursor()

        sql1 = "SELECT COALESCE(MAX(s.id_seg)+1,1) AS id from seguimiento AS s"

        cursor1.execute(sql1)
        datos = cursor1.fetchone()
        cursor1.close()

        sql2 = "SELECT cantidad_dias FROM control WHERE id_control={}".format(
            seguimiento.id_control
        )
        cursor2.execute(sql2)
        datos2 = cursor2.fetchone()
        cursor2.close()

        if datos2[0] == 0:
            sql = "INSERT INTO seguimiento (id_seg, id_tomate, id_control, fecha_registro, estado, diagnostico, porcen_fiabilidad, foto_hoja) VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s, %s)"
            values = (
                datos[0],
                seguimiento.id_tomate,
                seguimiento.id_control,
                seguimiento.estado,
                seguimiento.diagnostico,
                seguimiento.porcen_fiab,
                seguimiento.foto_hoja,
            )
            try:
                cursor.execute(sql, values)
                db.connection.commit()
                return json.dumps(
                    {
                        "status": True,
                        "data": "Seguimiento Registrado Correctamente",
                        "datos": datos,
                    }
                )
            except Exception as ex:
                raise Exception(ex)
        else:
            sql = "INSERT INTO seguimiento (id_seg, id_tomate, id_control, fecha_registro, estado, diagnostico, porcen_fiabilidad, foto_hoja,fecha_inicio,fecha_fin) VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s, %s,%s,DATE_ADD(%s, INTERVAL %s DAY))"
            values = (
                datos[0],
                seguimiento.id_tomate,
                seguimiento.id_control,
                seguimiento.estado,
                seguimiento.diagnostico,
                seguimiento.porcen_fiab,
                seguimiento.foto_hoja,
                seguimiento.fecha_ini,
                seguimiento.fecha_ini,
                datos2[0],
            )
            try:
                cursor.execute(sql, values)
                db.connection.commit()
                return json.dumps(
                    {
                        "status": True,
                        "data": "Seguimiento Registrado Correctamente",
                        "datos": datos,
                    }
                )
            except Exception as ex:
                raise Exception(ex)
