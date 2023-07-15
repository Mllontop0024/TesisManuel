from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin
class Usuario(UserMixin):
    def __init__(self,id=None,nom=None,ape=None,cor=None,tipou=None,cam=None,con=None):
        self.id=id
        self.nom=nom
        self.ape=ape
        self.cor=cor
        self.tipou=tipou
        self.cam=cam
        self.con=con
        
    
    @classmethod
    def check_password(self,hashed_password,password):
        return check_password_hash(hashed_password,password)

