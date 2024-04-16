import json
from objetos.usuario import Usuario

try:
    # Tenta abrir o arquivo JSON
    with open('data/usuarios.json') as usuarios_file:
        # Tenta carregar os dados do arquivo
        data = json.load(usuarios_file)
except json.decoder.JSONDecodeError:
    # Se o arquivo estiver vazio ou inválido, define data como uma lista vazia
    data = []

def adiciona_usuario():
    nome = input('Nome:')
    data_nascimento = input('data de nascimento: ')
    novo_id = max([lista['id'] for lista in data], default=0) + 1

    usuarios = Usuario(novo_id, nome, data_nascimento)
    data.append(usuarios.converte_em_json())

    with open('data/usuarios.json', 'w') as usuarios_file:
        json.dump(data, usuarios_file, indent=4)

    
def remove_usuario(id):
    index = None

    for i, usuario in enumerate(data):
        if usuario['id'] == id:
            index = i
            break
    if index is not None:
        del data[index]
    
        with open('data/usuarios.json', 'w') as usuarios_file:
            json.dump(data, usuarios_file, indent=4)

        return f'Usuário do id f{id} excluido'
    else: 
        f'usuário do id {id} não encontrado'

def retorta_todos_nomes():
    nome_parametro = [nome['nome'] for nome in data]
    return nome_parametro

def retorna_um_nome(nome_paramentro):
    for nome in data:
        if nome['nome'] == nome_paramentro:
            return nome_paramentro
    return 'Nome nao encontrado'

#uso do case no Python
operacao = 2
match operacao:
    case 1:
        print('Escolhido o numero 1')
    case 2: 
        print('Escolhido o numero 2')
    case 3:
        print('Escolhido o numero 3')
    case 4:
        print('Escolhido o numero 4')
    case _: #caso contrario
        print('Opcao invalida!!')




