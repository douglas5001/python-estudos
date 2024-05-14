from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql
from marshmallow import fields
from flask_restful import Resource, Api
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
import uuid

pymysql.install_as_MySQLdb()
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:bola2020@85.239.239.196/loja_mercado'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "aplicacao_flask"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

# entidade
class Produto():
    def __init__(self, nome, descricao, categoria):
        self.__nome = nome
        self.__descricao = descricao
        self.__categoria = categoria
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome
    
    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria

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
    def email(self,email):
        self.email = email

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.__senha = senha

# model
class ProdutoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    categoria = db.Column(db.String(50))

    def __init__(self, nome, descricao, categoria):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria




class UsuarioModel(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)


    

# Schema
class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProdutoModel
        load_instance = True
        fields = ("id", "nome", "descricao", "categoria")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    categoria = fields.String(required=True)

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsuarioModel
        fields = ("id", "nome", "email", "senha")
    nome  = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=True)


# service
def cadastrar_produto(produto):
    produto_db = ProdutoModel(nome=produto.nome, descricao=produto.descricao, categoria=produto.categoria)
    db.session.add(produto_db)
    db.session.commit()
    return produto_db

def listar_produto():
    produto = ProdutoModel.query.all()
    return produto

def listar_produto_id(id):
    produto = ProdutoModel.query.filter_by(id=id).first()
    return produto

def atualiza_produto(produto_anterior, produto_novo):
    produto_anterior.nome = produto_novo.nome
    produto_anterior.descricao = produto_novo.descricao
    produto_anterior.categoria = produto_novo.categoria
    db.session.commit()

def remove_produto(produto):
    db.session.delete(produto)
    db.session.commit()

def cadastrar_usuario(usuario):
    usuario_db = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db

# views
class ProdutoList(Resource):
    def get(self):
        produtos = listar_produto() 
        pd = ProdutoSchema(many=True)  
        produtos_serializados = pd.dump(produtos)  
        return produtos_serializados  
    
    def post(self):
        pd = ProdutoSchema()
        validate = pd.validate(request.form)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.form["nome"]
            descricao = request.form["descricao"]
            categoria = request.form["categoria"]
            novo_produto = Produto(nome=nome, descricao=descricao, categoria=categoria)
            resultado = cadastrar_produto(novo_produto)
            x = pd.jsonify(pd.dump(resultado))
            return make_response(x, 201)
            #return make_response(pd.jsonify(pd.dump(resultado)), 201)



class ProdutoDetail(Resource):

    def get(self, id):
        produto = listar_produto_id(id)
        if produto is None:
            return make_response(jsonify("Produto não encontrado"), 404)
        pd = ProdutoSchema()
        return make_response(pd.jsonify(produto), 200)
    
    def put(self, id):
        produto_db = listar_produto_id(id)
        if produto_db is None:
            return make_response(jsonify("Produto não encontrado"), 404)
        
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        categoria = request.form["categoria"]
        
        
        novo_produto =  Produto(nome=nome, descricao=descricao, categoria=categoria)
        
        atualiza_produto(produto_db, novo_produto)
        produto_atualizado = listar_produto_id(id)
        pd = ProdutoSchema()
        return make_response(pd.jsonify(produto_atualizado), 200)
    
    def delete(self, id):
        produto_db = listar_produto_id(id)
        if produto_db is None:
            return make_response(jsonify("Produto não encontrado"), 404)
        remove_produto(produto_db)
        return make_response("Produto excluído com sucesso", 204)
    
class UsuarioList(Resource):
    def post(self):
        us = UsuarioSchema()
        validate = us.validate(request.form)
        if validate:
            return make_response(jsonify(validate),400)
        else:
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            resultado = cadastrar_usuario(novo_usuario)
            x = us.jsonify(us.dump(resultado))
            return make_response(x,201)
            

        
        

api.add_resource(UsuarioList, '/usuarios')    
api.add_resource(ProdutoList, '/produtos')
api.add_resource(ProdutoDetail, '/produtos/<int:id>')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)
