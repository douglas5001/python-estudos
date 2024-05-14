from flask import Flask, render_template
import urllib.request, json

app = Flask(__name__)

@app.route('/')
def principal():
    url = "http://localhost:8000/produtos"
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    produtos = json.loads(dados)
    return render_template('index.html', produtos=produtos)

app.run(host='localhost', port=8001, debug=True)
