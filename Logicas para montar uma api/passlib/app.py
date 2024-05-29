from flask import Flask, make_response, jsonify, request
from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request, create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow import fields
from flask_restful import Resource, Api
from passlib.hash import pbkdf2_sha256



app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:postgres@localhost/usuarios"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
migrate = Migrate(app, db)

class Usuario():
    def __init__(self, nome, senha, is_admin):
        self.__nome = nome 
        self.__senha = senha
        self.__is_admin = is_admin

    @property
    def nome(self):
        return self.__nome 
    
    @nome.setter
    def nome(self,nome):
        self.__nome = nome

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.senha = senha

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, is_admin):
        self.is_admin = is_admin

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    nome = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean)

    def criptografar(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True
        fields = ('id','nome', 'senha', 'is_admin')
    nome = fields.String(required=True)
    senha = fields.String(required=True)
    is_admin = fields.Boolean(required=True)


def cadastro_usuario(usuario):
    usuario_db = UsuarioModel(nome=usuario.nome, senha=usuario.senha, is_admin=usuario.is_admin)
    usuario_db.criptografar()
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


class UsuarioList(Resource):
    def post(self):
        us = LoginSchema()
        validate = us.validate(request.json)
        if validate:
            return make_response(jsonify('Erro no formulario'), 403)
        else:
            nome = request.json['nome']
            senha = request.json['senha']
            is_admin = request.json['is_admin']

        novo_usuario = Usuario(nome=nome, senha=senha, is_admin=is_admin)
        resultado = cadastro_usuario(novo_usuario)
        x = us.jsonify(resultado)
        return make_response(x, 201)



def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'admin':
            return make_response(jsonify(message='nao é permitido, apenas para administrador'), 403)
        else:
            return fn(*args, **kargs)
    return wrapper


api.add_resource(UsuarioList, '/usuarios')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)              