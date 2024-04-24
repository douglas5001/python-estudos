from classes.usuario import Usuario
from classes.armario import Armario
import json
import os

class Usuarios_com_chave():
    def __init__(self, nome, matricula_usuario, numero_sala):
        self.nome = nome
        self.matricula_usuario = matricula_usuario
        self.numero_sala = numero_sala
    
    def converte_em_json(self):
        return {
            "nome": self.nome,
            "matricula": self.matricula_usuario,
            "numero_sala": self.numero_sala
        }
    
    def update_json(update_json):
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/usuarios_com_chave.json')
        with open(file_path, 'w') as json_file:
            json.dump(update_json, json_file, indent=4)
    
    @staticmethod
    def get_usuarios_com_chave():
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../data/usuarios_com_chave.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data
    
    
    def pegar_chave():
        usuarios = [usuario for usuario in Usuario.listar() if not usuario["possui_chave"]]
        armarios = [armario for armario in Armario.listar() if armario["possui_chave"]]
        get_usuarios_com_chave = Usuarios_com_chave.get_usuarios_com_chave()

        print('Qual usuário vai pegar a chave: \n')
        for i_usuario, usuario in enumerate(usuarios):
            print(f'{i_usuario} - {usuario["nome"]}')
        escolha_usuario = int(input('Escolha: '))

        
        print('Qual chave vai pegar: \n')
        for i_armario, armario in enumerate(armarios):
            print(f'{i_armario} - {armario["numero_sala"]}')
        escolha_armario = int(input('Escolha: '))

        if 0 <= escolha_usuario < len(usuarios) and 0 <= escolha_armario < len(armarios):
            print(f'Você escolheu {usuarios[escolha_usuario]["nome"]} e a chave da sala {armarios[escolha_armario]["numero_sala"]}')
            usuarios[escolha_usuario]["possui_chave"] = True
            armarios[escolha_armario]["possui_chave"] = False

            nome = usuarios[escolha_usuario]["nome"]
            matricula_usuario = usuarios[escolha_usuario]["matricula"]
            numero_sala = armarios[escolha_armario]["numero_sala"]

            usuario_com_chave = Usuarios_com_chave(nome, matricula_usuario, numero_sala)
            get_usuarios_com_chave.append(usuario_com_chave.converte_em_json())
            
            # Salvar a estrutura de dados modificada de volta para o arquivo JSON
            Usuario.update_usuario(usuarios)
            Armario.update_armario(armarios)
            Usuarios_com_chave.update_json(get_usuarios_com_chave)
      
        else:
            print('Você escolheu uma opção inválida!!!')
    
    def todos_devolvem_as_chaves():
        usuarios = Usuario.listar()
        armarios = Armario.listar()
        usuarios_com_chave = Usuarios_com_chave.get_usuarios_com_chave()

        
        for usuario in usuarios:
            usuario["possui_chave"] = False
            
        for armario in armarios:
            armario["possui_chave"] = True
        
        usuarios_com_chave = []


        Usuario.update_usuario(usuarios)
        Armario.update_armario(armarios)
        Usuarios_com_chave.update_json(usuarios_com_chave)
        # Salvar a estrutura de dados modificada de volta para o arquivo JSON
        




