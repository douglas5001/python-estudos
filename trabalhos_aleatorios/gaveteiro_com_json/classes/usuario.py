import json
import os

class Usuario:
    def __init__(self, nome, matricula, possui_chave):
        self.nome = nome
        self.matricula = matricula
        self.possui_chave = possui_chave
    
    @staticmethod
    def listar():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/usuario.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
