import json
import os

class Armario():
    def __init__(self, id, numero_sala):
        self.id = id
        self.numero_sala = numero_sala
        self.possui_chave = True
        
    @staticmethod
    def listar():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/armario.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    
    def update_armario(armarios):
        script_dir = os.path.dirname(__file__)
        file_path_chaves = os.path.join(script_dir, '../data/armario.json')
        with open(file_path_chaves, 'w') as json_file:
            json.dump(armarios, json_file, indent=4)