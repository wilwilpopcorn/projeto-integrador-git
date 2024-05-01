
from flask import Flask, request, render_template_string,render_templat

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="PI",
    password="131297",
    database="Assaltos"
)

app = Flask(__name__)

@app.route('/Paginainicial', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def reportincident():
    if request.method == 'POST':
        nome = request.form.get('nome')
        rua = request.form.get('rua')
        bairro = request.form.get('bairro')
        periodo = request.form.get('periodo')
        idade = request.form.get('idade')
        obs = request.form.get('obs')
        escolaridade = request.form.get('escolaridade')


        UF = ( 'SP' )
        link = f'https://viacep.com.br/ws/{rua}/{bairro}/{UF}/json/'


        mycursor = db.cursor()
        sql = "INSERT INTO assaltos (nome, rua, bairro, periodo, idade, obs, escolaridade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nome, rua, bairro, periodo, idade, obs, escolaridade)
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "record inserted.")

    return render_template_string(open("app\static\HTML\PaginaInicial.html").read())


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template_string(open("app\static\HTML\login.html").read())

@app.route('/consulta', methods=['GET','POST'])
def consulta():
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM assaltos")
    dados = mycursor.fetchall()
    html_string = open("app\static\HTML\consulta.html").read()
    return render_template_string(html_string, dados=dados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)