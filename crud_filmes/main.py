from filmes import Filmes
import json


with open('filmes.json') as filmes_json:
    data = json.load(filmes_json)


def adicionar_json():
    nome = input('Nome: ')
    descricao = input('Descricao: ')
    ano = input('Data: ')
    id = max([list['id'] for list in data], default=0) + 1
    novo_filme = Filmes(id, nome, descricao, ano,)
    data.append(novo_filme.converte_em_json())

    with open('filmes.json', 'w') as filmes_json:
        json.dump(data, filmes_json, indent=4)

sair = False

while sair == False:
    operacao = input('1- Adicionar: \n2- Consultar')
    
    if operacao == 1:
        print('adicionar')
        #adicionar_json()
    elif operacao == 2:
        print('Consultar')
    elif operacao == 3:
        sair = True
    else:
        operacao = 'Invalido'