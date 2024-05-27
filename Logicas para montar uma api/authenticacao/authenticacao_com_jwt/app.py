from datetime import timedelta
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_migrate import Migrate
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_restful import Resource,Api
import pymysql
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:bola2020@85.239.239.196/usuarios'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "aplicacao_flask"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)

from functools import wraps
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request

class Usuario():
    def __init__(self, nome, email, senha, is_admin):
        self.__nome = nome 
        self.__email = email
        self.__senha = senha
        self.__is_admin = is_admin

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
    def senha(self, senha):
        self.senha = senha

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, is_admin):
        self.is_admin = is_admin

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean)

    def encriptar_senha(self):
        self.senha = pbkdf2_sha256.hash(self.senha)

    def ver_senha(self, senha):
        return pbkdf2_sha256.verify(senha, self.senha)

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True
        fields = ("id", "nome", "email", "senha")

    nome = fields.String(required=False)
    email = fields.String(required=True)
    senha = fields.String(required=True)

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        load_instance = True
        fields = ("id","nome", "email", "senha", "is_admin")
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=True)
    is_admin = fields.Boolean(required=True)



def listarusuario():
    usuario_db = UsuarioModel.query.all()
    return usuario_db

def listar_usuario_id(id):
    usuario_db = UsuarioModel.query.filter_by(id=id).first() #filt(id=id).first()
    return usuario_db

def listar_usuario_email(email):
    return UsuarioModel.query.filter_by(email=email).first()


def cadastrar_usuario(usuario):
    usuario_bd = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=usuario.senha, is_admin=usuario.is_admin)
    usuario_bd.encriptar_senha()
    db.session.add(usuario_bd)
    db.session.commit()
    return usuario_bd

def atualizar_tabela(usuario_anterior, usuario_novo):
    usuario_anterior.nome = usuario_novo.nome
    usuario_anterior.email = usuario_novo.email
    usuario_anterior.senha = usuario_novo.senha
    db.session.commit()

def deletar_usuario(usuario):
    db.session.delete(usuario)
    db.session.commit()
    return usuario

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['roles'] != 'admin':
            return make_response(jsonify(message='Náo é prermitido esse recurco, só para administradores'), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper


class LoginList(Resource):
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        usuario_token = listar_usuario_id(identity)  #(identity)
        if usuario_token.is_admin:
            roles = 'admin'
        else:
            roles = 'user'

        return {'roles':roles}

    def post(self):
        ls = LoginSchema()
        validate = ls.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            email = request.json["email"]
            senha = request.json["senha"]

            usuario_db = listar_usuario_email((email))

            if usuario_db and usuario_db.ver_senha(senha):
                access_token = create_access_token(
                    identity=usuario_db.id,
                    expires_delta=timedelta(seconds=500)
                )

                refresh_token = create_refresh_token(
                    identity=usuario_db.id
                )

                return make_response(jsonify({
                    'access_token':access_token,
                    'refresh_token':refresh_token,
                    'message':'login realizado com sucesso'
                }), 200)

            return make_response(jsonify({
                'message':'Credenciais estao invalidadas'
            }), 401)

class RefreshTokenList(Resource):
    @jwt_required(refresh=True)
    def post(self):
        usuario_token = get_jwt_identity()
        access_token = create_access_token(
            identity=usuario_token,
            expires_delta=timedelta(seconds=100)
        )
        refresh_token = create_refresh_token(
            identity=usuario_token
        )

        return make_response({
            'access_token':access_token,
            'refresh_token':refresh_token
        }, 200)



class UsuariosList(Resource):
    def get(self):
        us = UsuarioSchema(many=True)
        resultado = listarusuario()
        return make_response(us.jsonify(resultado), 200)
        #us = UsuarioSchema(many=True)
        #resultado = listarusuario()
        #return make_response(us.jsonify(resultado), 200)
    
    def post(self):
        us = UsuarioSchema()
        validate  = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            email = request.json['email']
            senha = request.json['senha']
            is_admin = request.json['is_admin']
            novo_usuario = Usuario(nome=nome, email=email, senha=senha, is_admin=is_admin)
            resultado = cadastrar_usuario(novo_usuario)
            x = us.jsonify(resultado)
            return make_response(x, 201)
        
class UsuarioIdList(Resource):

    def get(self, id):
        us = listar_usuario_id(id)
        if us is None:
            return make_response(jsonify('Usuario nao encontrado'),404)
        else:
            resultado = UsuarioSchema()
            x = resultado.jsonify(us)
            return make_response(x, 200)

    def put(self, id):
        us = listar_usuario_id(id)
        if us is None:
            return make_response(jsonify('usuario Nao encontrado'), 404)
        else:
            us = UsuarioSchema()
            validate = us.validate(request.json)
            if validate:
                return make_response(jsonify(validate), 400)
            else:
                nome = request.json['nome']
                email = request.json['email']
                senha = request.json['senha']
                novo_usuario = Usuario(nome=nome, email=email, senha=senha)
                atualizar_tabela(us, novo_usuario)
                usuario_atualizado = listar_usuario_id(id)
                return make_response(us.jsonify(usuario_atualizado), 201)
    
    def delete(self, id):
        us = listar_usuario_id(id)
        if us is None:
            return make_response(jsonify('usuario nao encontrado'),404)
        else:
            deletar_usuario(us)
            return make_response('usuario deletado')


api.add_resource(RefreshTokenList, '/token/refresh')
api.add_resource(LoginList, '/login')


api.add_resource(UsuariosList, '/usuarios')
api.add_resource(UsuarioIdList, '/usuarios/<int:id>')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)