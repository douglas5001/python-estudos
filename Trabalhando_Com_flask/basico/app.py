from flask import Flask, render_template, request
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.sqlite3"

db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self,nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch


@app.route('/', methods=["POST","GET"])
def principal():
    #frutas = ['Banana', 'Goiaba', 'Maca', 'Uva']
    if request.method == "POST":
        if request.form.get("fruta"):
            frutas.append(request.form.get("fruta"))
    return render_template("index.html", frutas=frutas)

@app.route('/sobre', methods=["GET", "POST"])
def sobre():
    #notas = {'Fulano':5.0, 'Beltrano':6.0, 'Aluno':7.0, 'Sicrano':8.5, 'Rodrigo':9.5}
    if request.method == "POST":
        if request.form.get("aluno") and request.form.get('nota'):
            registros.append({"aluno": request.form.get("aluno"),"nota": request.form.get("nota")})
    
    return render_template("sobre.html", registros=registros)

#Rotas Dinamicas
@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"
    elif propriedade == 'drama':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"
    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=bb6669d1b8e291a4619d7c01807870bc"

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    return render_template("filmes.html", filmes=jsondata['results'])

@app.route('/cursos')
def lista_cursos():
    return render_template("cursos.html", cursos=cursos.query.all())

@app.route('/cria_curdso')
def cria_curso():
    return render_template("curso.html")


#app.run(port=8000,host='localhost',debug=True)
if __name__ =="__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8000,host='localhost', debug=True,)