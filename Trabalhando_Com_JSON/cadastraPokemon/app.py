import json
from classes.pokemon import Pokemon

with open('json/pokemon.json') as json_file:
    data = json.load(json_file)



def adicionajson():
    nome = 'douglas'
    descricao = 'Teste def GEWGKOEWG:JEWG"KEWLGdescricao'
    data_ano = '2002-06-05'
    novo_id = max([lista["id"] for lista in data], default=0) + 1
    pokemon = Pokemon(novo_id, nome, descricao, data_ano)
    data.append(pokemon.converte_em_json())

    with open('json/pokemon.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

print(adicionajson())