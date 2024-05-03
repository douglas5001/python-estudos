from ..models import formacao_model
from api import db

def cadastrar_formacao(formacao):
    formacao_bd = formacao_model.Formacao(nome=formacao.nome, descricao=formacao.descricao)
    db.session.add(formacao_bd)
    db.session.commit()
    return formacao_bd

def listar_formacoes():
    formacoes = formacao_model.Formacao.query.all()
    return formacoes

def listar_formacao_id(id):
    formacao = formacao_model.Formacao.query.filter_by(id=id).first()
    return formacao

def atualiza_formacao(formacao_anterior, formacao_novo):
    formacao_anterior.nome = formacao_novo.nome
    formacao_anterior.descricao = formacao_novo.descricao
    db.session.commit()

def remove_formacao(formacao):
    db.session.delete(formacao)
    db.session.commit()