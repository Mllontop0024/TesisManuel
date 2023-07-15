from .entidades.Plaga import Plaga
from .entidades.Tomate import Tomate
from util import CustomJsonEncoder
import json

class Modelplaga():
    @classmethod
    def listarPlaga(self,db,plaga):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id_plaga,nombre_plaga,descripcion FROM plaga WHERE id_plaga={}""".format(plaga.id)
            cursor.execute(sql)
            datos=cursor.fetchone()
            if datos:
                return datos
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    