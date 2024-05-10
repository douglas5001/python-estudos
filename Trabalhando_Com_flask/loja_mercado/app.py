from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pymysql
from marshmallow import fields
from flask_restful import Resource, Api
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

pymysql.install_as_MySQLdb()
app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://USER:SENHA@IP/loja_mercado'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = "aplicacao_flask"

db = SQLAlchemy(app)
ma = Marshmallow(app)

#entidade
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

#model
class ProdutoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    categoria = db.Column(db.String(50))  # Especificando o comprimento do campo

    def __init__(self, nome, descricao, categoria):
        self.nome = nome
        self.descricao = descricao
        self.categoria = categoria

#Schema
class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProdutoModel
        load_instance = True
        fields = ("id", "nome", "descricao", "categoria")

    nome = fields.String(required=True)
    descricao = fields.String(required=True)
    categoria = fields.String(required=True)

#service
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



#views
class ProdutoList(Resource):

    def get(self):
        produtos = listar_produto()  
        pd = ProdutoSchema(many=True)  
        produtos_serializados = pd.dump(produtos)  
        return produtos_serializados  
    
    def post(self):
        pd = ProdutoSchema()
        validate = pd.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            categoria = request.json["categoria"]
            novo_produto = Produto(nome=nome, descricao=descricao, categoria=categoria)

            resultado = cadastrar_produto(novo_produto)
            x = pd.jsonify(resultado)
            return make_response(x, 201)

class ProdutoDetail(Resource):

    def get(self, id):
        produto = listar_produto_id(id)
        if produto is None:
            return make_response(jsonify("Produtpo nao encontrado"), 404)
        pd = ProdutoSchema()
        return make_response(pd.jsonify(produto), 200)
    
    def put(self, id):
        produto_db = listar_produto_id(id)
        if produto_db is None:
            return make_response(jsonify("produto nao foi encontrado"), 404)
        pd = ProdutoSchema()
        validade = pd.validate(request.json)
        if validade:
            return make_response(jsonify(validade), 400)
        else: 
            nome = request.json["nome"]
            descricao = request.json["descricao"]
            categoria = request.json["categoria"]
        novo_produto =  Produto(nome=nome, descricao=descricao, categoria=categoria)
        atualiza_produto(produto_db, novo_produto)
        produto_atualizado = listar_produto_id(id)
        return make_response(pd.jsonify(produto_atualizado), 200)
    
    def delete(self, id):
        Produto_db = listar_produto_id(id)
        if Produto_db is None:
            return make_response(jsonify("prduto nao encontrado"), 404)
        remove_produto(Produto_db)
        return make_response("produto Excluido com sucesso", 204)
    
api.add_resource(ProdutoList, '/produtos')
api.add_resource(ProdutoDetail, '/produtos/<int:id>')


if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000, host='localhost', debug=True)
