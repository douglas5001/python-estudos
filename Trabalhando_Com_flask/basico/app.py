from flask import Flask, render_template, request


app = Flask(__name__)

frutas = []
registros = []

@app.route('/', methods=["POST","GET"])
def principal():
    frutas = ['Banana', 'Goiaba', 'Maca', 'Uva']
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

app.run(port=8000,host='localhost',debug=True)