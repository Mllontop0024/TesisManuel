class Config:
    SECRET_KEY = "B!1weNA1T^%kvhUI*S^"


class DevelopmentConfig(Config):
    DEBUG = True
    # CONEXIÓN A LA BASE DE DATOS MYSQL
    # MYSQL_HOST='productotesis-server.mysql.database.azure.com"'
    # MYSQL_USER='ccucvlnlrp'
    # MYSQL_PASSWORD ='8ON4E21578CB5T8B$'
    # ALEjandro2409?
    # MYSQL_DB='tesis1'
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "bd_tesis1"


config = {"development": DevelopmentConfig}
