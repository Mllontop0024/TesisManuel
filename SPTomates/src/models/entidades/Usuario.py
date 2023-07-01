from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
class Usuario(UserMixin):
    def __init__(self,id=None,nom=None,ape=None,cor=None,cam=None,con=None,tipou=None):
        self.id=id
        self.nom=nom
        self.ape=ape
        self.cor=cor
        self.cam=cam
        self.con=con
        self.tipou=tipou
    
    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password,password)

