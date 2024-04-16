from flask import Flask, render_template, request, redirect, url_for
from classes.usuario import Usuario
import json

app = Flask(__name__)

with open('data/usuarios.json') as file_json:
    data = json.load(file_json)


@app.route('/')
def principal():
    return render_template("index.html", data=data)
    
@app.route('/login', methods=["POST", "GET"])
def menu_login():
    if request.method == "POST":
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        for usuario in data:
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return redirect(url_for('menu_admin'))
                
        else:
            mensagem = 'Acesso negado'
    else:
        mensagem = 'Erro'

    return render_template("login.html", mensagem=mensagem)

@app.route('/admin', methods=["GET", "POST", "DELETE"])
def menu_admin():

    return render_template("admin.html")

app.run(port=8000,host='localhost',debug=True)