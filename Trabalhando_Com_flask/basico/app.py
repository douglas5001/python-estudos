from flask import Flask, render_template, request

app = Flask(__name__)

usuarios = []

@app.route('/', methods=["POST"])
def principal():
    frutas = ['Banana', 'Goiaba', 'Maca', 'Uva']
    alunos = {'Douglas':4.5,'pedro':4.8,'Luana':10,'Camila':4.9,'Lucas':5,'Marcelo':8}

    if request.method == "POST":
        if request.form.get("usuario"):
            usuarios.append(request.form.get("usuario"))
    return render_template("index.html", frutas=frutas, alunos=alunos, usuarios=usuarios)

@app.route('/sobre')
def sobre():
    return render_template("sobre.html")

app.run(port=8000,host='localhost',debug=True)