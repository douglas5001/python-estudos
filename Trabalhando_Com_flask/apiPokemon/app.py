from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


# Carregar variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Configurações do banco de dados
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# Conexão com o banco de dados
mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/pokemon', methods=["GET"])
def get_all_pokemons():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

@app.route('/pokemonweb', methods=["GET"])
def get_all_pokemonsweb():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokemons")
    result = cursor.fetchall()
    cursor.close()
    return render_template('index.html', pokemons=result)

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/cadastropokemon', methods=["GET", "POST"])
def cadastropokemon():
    if request.method == "POST":
        nome = request.form['nome']
        descricao = request.form['descricao']
        imagem = request.files['imagem']
        
        if imagem:
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Salve o caminho da imagem no banco de dados ou faça o que for necessário com ela
            
            # Aqui você pode prosseguir com a inserção no banco de dados, incluindo o caminho da imagem
        
        return redirect(url_for('principal'))  # Redireciona para a página principal após o cadastro

    return render_template('cadastro.html')

@app.route('/pokemonname', methods=["GET"])
def get_allpokemons():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute("SELECT nome FROM pokemons")
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

@app.route('/pokemon/<int:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    cursor = mysql.cursor()
    cursor.execute("DELETE FROM pokemons WHERE id=%s", (pokemon_id,))
    mysql.commit()
    cursor.close()
    return jsonify({'message': 'Pokemon deletado com sucesso!'})



if __name__ == "__main__":
    app.run(port=8000, host='localhost', debug=True)
