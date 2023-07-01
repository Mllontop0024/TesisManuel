from .entidades.Control import Control
from util import CustomJsonEncoder
import json
class Modelcontrol():
    @classmethod
    def listarcontrolsegunplaga(self,db,control):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT * FROM control WHERE id_plaga={}""".format(control.id_plaga)
            cursor.execute(sql)
            datos=cursor.fetchall()

            if datos:
                return datos
            else:
                return None
        except Exception as ex:
            raise Exception(ex)