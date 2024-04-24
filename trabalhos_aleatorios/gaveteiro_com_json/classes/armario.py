import json
import os

class Armario():
    def __init__(self, numero_sala):
        self.numero_sala = numero_sala
        self.possui_chave = True
        
    @staticmethod
    def listar():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/armario.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    
    def converte_em_json(self):
        return {
            "numero_sala":self.numero_sala,
            "possui_chave":self.possui_chave
        }
    
    def update_armario(armarios):
        script_dir = os.path.dirname(__file__)
        file_path_chaves = os.path.join(script_dir, '../data/armario.json')
        with open(file_path_chaves, 'w') as json_file:
            json.dump(armarios, json_file, indent=4)

    def post_armario():
        get_armario = Armario.listar()
        numero = max([lista["numero_sala"] for lista in get_armario], default=0) + 1

        armario = Armario(numero)

        get_armario.append(armario.converte_em_json())

        Armario.update_armario(get_armario)



