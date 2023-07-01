class Config:
    SECRET_KEY='B!1weNA1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    DEBUG = True
    #CONEXIÓN A LA BASE DE DATOS MYSQL
    MYSQL_HOST='127.0.0.1'
    MYSQL_USER='root'
    MYSQL_PASSWORD =''
    MYSQL_DB='bd_tesis1'

config = {
    'development': DevelopmentConfig
}

