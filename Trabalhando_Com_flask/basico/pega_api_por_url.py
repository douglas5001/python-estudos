import urllib.request, json

url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)

print(jsondata['results'])