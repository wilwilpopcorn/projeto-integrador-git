from flask import Flask, request, render_template_string
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="PI",
    password="131297",
    database="Assaltos"
)

app = Flask(__name__)

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

        # Aqui você pode processar os dados do formulário como quiser.
        # Por exemplo, você pode armazená-los em um banco de dados.
        #crud simples para inserção dos dados em bd mysql
        

        mycursor = db.cursor()
        sql = "INSERT INTO assaltos (nome, rua, bairro, periodo, idade, obs, escolaridade) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (nome, rua, bairro, periodo, idade, obs, escolaridade)
        mycursor.execute(sql, val)
        db.commit()
        print(mycursor.rowcount, "record inserted.")


    # Renderiza o formulário. Em uma aplicação real, você provavelmente
    # quereria usar rendertemplate() e manter seu HTML em um arquivo separado.
    return render_template_string(open("app\static\HTML\PaginaInicial.html").read())


@app.route('/login', methods=['GET','POST'])
def login():
    return render_template_string(open("app\static\HTML\login.html").read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)