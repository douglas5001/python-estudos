import json
from passlib.hash import pbkdf2_sha256

class Usuario():
  def __init__(self, nome, senha):
    self.nome = nome
    self.senha = senha
  
  def converte_em_json(self):
    return {
      "nome": self.nome,
      "senha": self.senha 
    }
  

with open('usuario.json') as json_file:
    data = json.load(json_file)


sair = False

while sair == False:
    operacao = int(input('   ====SELECIONE UMA OPCAO==== \nCadastro Usuario: \nFazer Login: \nSair: \nNumero: '))

    if operacao == 1:
        nome = input('digite o nome: ')
        senha = input('digite a senha: ')
        criptografado = pbkdf2_sha256.hash(senha)

        novo_usuario = Usuario(nome, criptografado)
        data.append(novo_usuario.converte_em_json())

        with open('usuario.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    elif operacao == 2:
        nome = input('digite o nome: ')
        senha = input('digite a senha: ')
        for usuario in data:
            if usuario['nome'] == nome:
                user_senha = usuario['nome'], usuario['senha']
            else:
               print('usuario nao encontrado')
        senha_valida = pbkdf2_sha256.verify(senha, user_senha[1])
        print(f'Senha Valida é {senha_valida}')
        print(f'Usuario: {user_senha[0]} Senha: {user_senha[1]}')
            
            
        #senhaverificada = pbkdf2_sha256.verify(senha, )
        

        
              

       


    elif operacao == 3:
       sair = True
       



