import json
from classes.usuario import Usuario
from classes.usuarios_com_chave import Usuarios_com_chave
from classes.armario import Armario
sair = False

while not sair:
    dato_leido = int(input(
        '====== ARMARIO DA ESCOLA ======\n\n'
        '1 - Consultar usuarios: '
        '\n2 - Consultar usuarios com a chave: '
        '\n3 - Consultar caixas do armario: '
        '\n4 - Pegar chave do armario: '
        '\n5 - Cadastrar usuario: '
        '\n6 - Todos os usuarios devolvem as chaves: '
        '\n7 - SAIR: '
        '\nEscolha: '))

    match dato_leido:
        case 1:
            print('===== CONSULTA DE USUARIOS =====\n')
            usuarios = Usuario.listar()
            for usuario in usuarios:
                print(f'Nome: {usuario["nome"]}\nMatricula: {usuario["matricula"]}\nPossui chave: {usuario["possui_chave"]}\n\n')
            break  
        case 2:
            print('===== CONSULTA DE USUARIOS COM CHAVES =====\n')
            usuarios_com_chave = Usuarios_com_chave.listar()
            for usuario in usuarios_com_chave:
                print(f'Nome: {usuario["nome"]}')
            break
        case 3:
            print('===== CONSULTA DE TODOS ARMARIOS =====\n')
            armarios = Armario.listar()
            for armario in armarios:
                print(f'id: {armario["id"]}\nNumero: {armario["numero_sala"]}\nEsta com a chave: {armario["possui_chave"]}\n\n')
            break
        case 4:
            print('Pegar chave do armario: ')
            break
        case 5:
            print('Cadastrar usuario: ')
            break
        case 6:
            print('Todos os usuarios devolvem as chaves: ')
            break
        case 7:
            sair = True
            break
        case _:
            print('Opção não existe')
