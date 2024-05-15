from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_migrate import Migrate
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_restful import Resource,Api
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:bola2020@85.239.239.196/usuarios'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "aplicacao_flask"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)

class Usuario():
    def __init__(self, nome, email, senha):
        self.__nome = nome 
        self.__email = email
        self.__senha = senha

    @property
    def nome(self):
        return self.__nome 
    
    @nome.setter
    def nome(self,nome):
        self.__nome = nome

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self):
        return self.__senha
    
class UsuarioModel(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True
        fields = ('id','nome', 'email', 'senha')
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=True)

def listarusuario():
    usuario_db = UsuarioModel.Query.filter.All()
    return usuario_db

class usuariosList(Resource):
    def get():
        Usuario = listarusuario()
        us = UsuarioSchema(many=True)
        produtos_serializados = us.dump(Usuario)  
        return produtos_serializados 







if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)