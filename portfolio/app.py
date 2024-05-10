from flask import Flask, render_template

app = Flask(__name__)

@app.route('/menu')
def principal():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000, host='localhost', debug=True)