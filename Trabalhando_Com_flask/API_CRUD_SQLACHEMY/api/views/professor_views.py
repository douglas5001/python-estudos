from flask_restful import Resource
from api import api
from ..schemas import professor_schema
from flask import request, make_response, jsonify
from ..entidades import professor
from ..services import professor_service
from ..paginate import paginate
from ..models.professor_model import Professor
class ProfessorList(Resource):
    def get(self):
        #ADICIONANDO PAGINATE
        #professores = professor_service.listar_professor()
        cs = professor_schema.ProfessorSchema(many=True)
        #return make_response(cs.jsonify(professores), 200)
        return paginate(Professor, cs)
    def post(self):
        cs = professor_schema.ProfessorSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            idade = request.json["idade"]

            novo_professor = professor.Professor(nome=nome, idade=idade)
            resultado = professor_service.cadastrar_professor(novo_professor)
            x = cs.jsonify(resultado)
            return make_response(x, 201)

class ProfessorDetail(Resource):
    def get(self, id):
        professor = professor_service.listar_professor_id(id)
        if professor is None:
            return make_response(jsonify("professor nao foi encontrada"), 404)
        cs = professor_schema.ProfessorSchema()
        return make_response(cs.jsonify(professor), 200)

    def put(self, id):
        professor_bd = professor_service.listar_professor_id(id)
        if professor_bd is None:
            return make_response(jsonify("professor nao foi encontrada"), 404)
        cs = professor_schema.ProfessorSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            idade = request.json["idade"]
            novo_professor = professor.Professor(nome=nome, idade=idade)
            professor_service.atualiza_professor(professor_bd, novo_professor)
            professor_atualizado = professor_service.listar_professor_id(id)
            return make_response(cs.jsonify(professor_atualizado), 200)

    def delete(self, id):
        professor_bd = professor_service.listar_professor_id(id)
        if professor_bd is None:
            return make_response(jsonify("professor nao encontrada"), 404)
        professor_service.remove_professor(professor_bd)
        return make_response("professor excluido com sucesso", 204)


api.add_resource(ProfessorList, '/professores')
api.add_resource(ProfessorDetail, '/professores/<int:id>')