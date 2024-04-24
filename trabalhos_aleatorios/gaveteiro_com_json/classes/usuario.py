import json
import os

class Usuario:
    def __init__(self, nome, matricula):
        self.nome = nome
        self.matricula = matricula
        self.possui_chave = False
    
    @staticmethod
    def listar():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/usuario.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    
    def converte_em_json(self):
        return {
            "nome":self.nome,
            "matricula":self.matricula,
            "possui_chave":self.possui_chave
        }
    
    def post_usuario():
        usuarios = Usuario.listar()
        nome = input('Digite o nome do Usuário: ').lower()
        matricula = max([list["matricula"] for list in usuarios], default=0) + 1
        novo_usuario = Usuario(nome, matricula)
        usuarios.append(novo_usuario.converte_em_json())

        # Salvar a estrutura de dados modificada de volta para o arquivo JSON
        Usuario.update_usuario(usuarios)

    def update_usuario(usuarios):
        script_dir = os.path.dirname(__file__)
        file_path_usuarios = os.path.join(script_dir, '../data/usuario.json')
        with open(file_path_usuarios, 'w') as json_file:
            json.dump(usuarios, json_file, indent=4)


    



