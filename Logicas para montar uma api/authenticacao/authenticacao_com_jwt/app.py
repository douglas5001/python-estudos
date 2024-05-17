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
    def senha(self, senha):
        self.senha = senha
    
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
        fields = ("id","nome", "email", "senha")
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=True)

def listarusuario():
    usuario_db = UsuarioModel.query.all()
    return usuario_db

def listar_usuario_id(id):
    usuario_db = UsuarioModel.query.filter_by(id=id).first() #filt(id=id).first()
    return usuario_db

def cadastrar_usuario(usuario):
    usuario_bd = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
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


class UsuariosList(Resource):
    def get(self):
        us = UsuarioSchema(many=True)
        resultado = listarusuario()
        return make_response(us.jsonify(resultado), 200)
    
    def post(self):
        us = UsuarioSchema()
        validate  = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json['nome']
            email = request.json['email']
            senha = request.json['senha']
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            resultado = cadastrar_usuario(novo_usuario)
            x = us.jsonify(resultado)
            return make_response(x, 201)
        
class UsuarioIdList(Resource):

    def get(self, id):
        usuario = listar_usuario_id(id)
        if usuario is None:
            return make_response(jsonify('usuario nao encontrado'), 404)
        else:
            us = UsuarioSchema()

            return make_response(us.jsonify(usuario), 200)

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



        





api.add_resource(UsuariosList, '/usuarios')
api.add_resource(UsuarioIdList, '/usuarios/<int:id>')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)