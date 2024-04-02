from classPessoa import Pessoa
import json

sair = False

while sair == False:
    operacao = int(input("Escolha uma opção: \n1 - Consulta: \n2 - Cadastro: \n3 - Alteração: \n4 - Exclusão: \n5 - Sair: \n"))
    if operacao == 1:
        print('      === CONSULTA === \n')
        #Consulta de um arquivo JSON local (No mesmo diretorio)
        with open('pessoas.json') as pessoas: #pessoas é a variavel que escolho para usar a função
            data = json.load(pessoas)
            for i in data:
                print(f'id: {i["id"]} - Nome: {i["nome"]} - CPF: {i["cpf"]} - Data_Nascimento: {i["data_nascimento"]}')
    elif operacao == 2:
        with open('pessoas.json') as pessoas: #pessoas é a variavel que escolho para usar a função
            data = json.load(pessoas)
        print('    === Cadastro de Pessoa === \n')
        nome = input("Nome: ")
        cpf = int(input("CPF: "))
        data_nascimento = input("Data de nascimento: ")
        novo_id = max([pessoa["id"] for pessoa in data], default=0) + 1 # aqui ele vai consultar o arquivo Json e vai verificar qual é o ultimo ID e vai acrecentar mais um para o novo usuário
        
        nova_pessoa = Pessoa(novo_id, nome, cpf, data_nascimento)

        data.append(nova_pessoa.transforma_em_json())

        with open('pessoas.json', 'w') as file:
            json.dump(data, file, indent=4)

    elif operacao == 3:
        print('Alteracao: \n')
    elif operacao == 4:
        print('Exclusao: \n')
    elif operacao == 5:
        sair = True
        print('Você finalizou o programa!')
    else:
        operacao = 'Valor invalido'