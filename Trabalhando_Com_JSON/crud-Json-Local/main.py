import json
from usuario import Usuario
with open('data/usuarios.json') as usuarios_json:
  data = json.load(usuarios_json)


sair = False

while sair == False:
  operacao = int(input('1 - Cadastro usuário: \n2 - Login aluno: \n3 - Consultar usuários: '))

  if operacao == 1:
    print("=== Cadastrar Usuário ===")
    nome = input("Digite nome: ")
    cpf = int(input("Digite o CPF: "))
    data_nascimento = input("Digite data de nascimento: ")
    id = max([usuarios['id'] for usuarios in data], default=0) +1
    
    novo_usuario = Usuario(id, nome, cpf, data_nascimento)
    data.append(novo_usuario.converte_em_json())
  
    with open('data/usuarios.json', 'w') as file:
      json.dump(data, file, indent=4)

  elif operacao == 2:
    print("=== LOGIN ===")
    nome = input('Nome: ')
    cpf = int(input('cpf'))
    usuario = Usuario(nome, cpf)

    if usuario == (usuario, data):
      print('usuario existe')
    else:
      print('Usuário nao existe')


  elif operacao == 3:
    print("=== Consultar usuários ===")
    for usuarios in data:
      print(usuarios["nome"])

