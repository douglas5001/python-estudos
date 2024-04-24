from classes.usuario import Usuario
from classes.usuarios_com_chave import Usuarios_com_chave
from classes.armario import Armario

sair = False

while not sair:
    operacao = int(input(
        '====== ARMARIO DA ESCOLA ======\n\n'
        '1 - Consultar usuarios: '
        '\n2 - Consultar usuarios com a chave: '
        '\n3 - Consultar caixas do armario: '
        '\n4 - Pegar chave do armario: '
        '\n5 - Cadastrar de usuario: '
        '\n6 - Cadastro de sala: '
        '\n7 - Todos os usuarios devolvem as chaves: '
        '\n8 - SAIR: '
        '\nEscolha: '))

    match operacao:
        case 1:
            print('\n\n===== CONSULTA DE USUARIOS =====\n')
            usuarios = Usuario.listar()
            for usuario in usuarios:
                print(f'Nome: {usuario["nome"]}\nMatricula: {usuario["matricula"]}\nPossui chave: {usuario["possui_chave"]}\n\n')  
        case 2:
            print('\n\n===== CONSULTA DE USUARIOS COM CHAVES =====\n')
            usuarios_com_chave = Usuarios_com_chave.listar()
            for usuario in usuarios_com_chave:
                print(f'Nome: {usuario["nome"]}')
        case 3:
            print('\n\n===== CONSULTA DE TODOS ARMARIOS =====\n')
            armarios = Armario.listar()
            for armario in armarios:
                print(f'id: {armario["id"]}\nNumero: {armario["numero_sala"]}\nEsta com a chave: {armario["possui_chave"]}\n\n')
        case 4:
            print('\n\n===== PEGAR CHAVE DO ARMARIO =====\n')
            usuarios_com_chave = Usuarios_com_chave.pegar_chave()
        case 5:
            print('\n\n===== CADASTRO DE USUÁRIO =====\n')
            usuario = Usuario.post_usuario()
        case 6:
            print('\n\n===== CADASTRO DE ARMARIO =====\n')
            armario = Armario.post_armario()
        case 7:
            print('\n\n===== TODOS USUARIOS DEVOLVERAM AS CHAVES =====\n')
            usuarios_com_chave = Usuarios_com_chave.todos_devolvem_as_chaves()
        case 8:
            sair = True
        case _:
            print('Opção não existe')
