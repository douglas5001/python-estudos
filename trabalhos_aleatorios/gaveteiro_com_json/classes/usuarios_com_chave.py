import json
import os
class Usuarios_com_chave():
    def __init__(self, usuario, matricula_usuario, numero_sala):
        self.usuario = usuario
        self.matricula_usuario = matricula_usuario
        self.numero_sala = numero_sala
    
    def converte_em_json(self):
        return {
            "usuario":self.usuario,
            "matricula":self.matricula_usuario,
            "numero_sala":self.numero_sala
        }
    
    @staticmethod
    def listar():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/usuarios_com_chave.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

