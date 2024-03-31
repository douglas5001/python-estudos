import json

carros_dictionary = {
    "marca":"honda",
    "modelo":"HRV",
    "cor":"prata"
}
#Dictionary -> Objeto Json

carros_list = ["honda", "volkswagem", "ford", "fiat", "chevrolet"]
#list -> array json

carros_tupla = ("honda", "volkswagem", "ford", "fiat", "chevrolet")
#tupla -> array json

carros_json = json.dumps(carros_dictionary)
carros_jsonLIST = json.dumps(carros_list)
carros_jsonTUPLA = json.dumps(carros_tupla)

print('=====')
print(carros_json)
print('=====')
print(carros_jsonLIST)
print('=====')
print(carros_jsonTUPLA)
print('=====\n')
#modicando
carros_json = json.dumps(carros_dictionary, indent=4, separators=(": ","="), sort_keys=True)#modificado
print(carros_json) #ordenando em ordem alfabetica