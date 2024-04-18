from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'IP'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bola@2020'
app.config['MYSQL_DB'] = 'db_mysql'

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


if __name__ == "__main__":
    app.run(port=8000, host='localhost', debug=True)
