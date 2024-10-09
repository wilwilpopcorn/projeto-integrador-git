from flask import Flask, request, render_template, flash, redirect, session
import requests
from unidecode import unidecode
import mysql.connector

app = Flask(__name__)
app.secret_key = 'teste'  # Manter para usar flash messages

# Função para conectar ao banco de dados MySQL NÃO MEXER!!!!!
def get_db_connection():
    return mysql.connector.connect(
        host='RomuloBalsalobre.mysql.pythonanywhere-services.com',
        user='RomuloBalsalobre',
        password='testepi2024',
        database='RomuloBalsalobre$reports'
    )

@app.route('/Paginainicial', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def reportincident():
    if request.method == 'POST':
        rua = unidecode(request.form.get('rua').upper())
        bairro = unidecode(request.form.get('bairro'))
        periodo = request.form.get('periodo')
        obs = request.form.get('obs')

        # Verifica se o endereço digitado é válido
        UF = 'SP'
        if not rua or len(rua) < 3:
            flash('Rua inválida. Digite um nome de rua válido.', 'error')
            return redirect('/')

        response = requests.get(f'https://viacep.com.br/ws/{UF}/diadema/{rua}/json/')
        data = response.json()

        if not data or unidecode(rua).upper() != unidecode(data[0]['logradouro'].upper()) or unidecode(bairro) != unidecode(data[0]['bairro']):
            flash('Rua ou bairro inválido - OBS: Não digite o número da casa, apenas o nome da rua', 'error')
            return redirect('/')

        # Se tudo estiver correto, insere no banco de dados
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO assaltos (rua, bairro, periodo, obs, data) VALUES (%s, %s, %s, %s, NOW())"
            val = (rua.upper(), bairro, periodo, obs)
            cursor.execute(sql, val)
            conn.commit()
            flash('Endereço salvo com sucesso!', 'success')
        except mysql.connector.Error as err:
            flash(f'Erro ao gravar no banco de dados: {err}', 'error')
        finally:
            cursor.close()
            conn.close()

        return redirect('/')

    return render_template('PaginaInicial.html')

@app.route('/quemSomos', methods=['GET'])
def quemSomos():
    return render_template('quemSomos.html')

@app.route('/consulta', methods=['GET'])
def consulta():
    conn = None
    mycursor = None

    try:
        conn = get_db_connection()
        mycursor = conn.cursor()

        # Obter os parâmetros de consulta do request
        bairro = request.args.get('bairro')
        periodo = request.args.get('periodo')

        print(f"Bairro: {bairro}, Período: {periodo}")  # Verifique os parâmetros recebidos

        if bairro and periodo:
            query = "SELECT DISTINCT rua, bairro, periodo, COUNT(*) FROM assaltos WHERE bairro = %s AND periodo = %s GROUP BY rua, bairro, periodo"
            mycursor.execute(query, (bairro, periodo))
        elif bairro:
            query = "SELECT DISTINCT rua, bairro, periodo, COUNT(*) FROM assaltos WHERE bairro = %s GROUP BY rua, bairro, periodo"
            mycursor.execute(query, (bairro,))
        elif periodo:
            query = "SELECT DISTINCT rua, bairro, periodo, COUNT(*) FROM assaltos WHERE periodo = %s GROUP BY rua, bairro, periodo"
            mycursor.execute(query, (periodo,))
        else:
            query = "SELECT rua, bairro, periodo, COUNT(*) as quantidade FROM assaltos GROUP BY rua, bairro, periodo ORDER BY quantidade DESC"
            mycursor.execute(query)

        dados = mycursor.fetchall()
        # Para rodapé do site
        # Contar o total de casos
        mycursor.execute("SELECT COUNT(*) FROM assaltos")
        total_casos = int(mycursor.fetchone()[0])

        # Data da última atualização
        mycursor.execute("SELECT data FROM assaltos ORDER BY data DESC LIMIT 1")
        data_atualizacao = mycursor.fetchone()[0].strftime('%d-%m-%Y')

    #ChatGPT que mandou isso aqui, funcionou, nem toca
    except mysql.connector.Error as err:
        print(f"Erro ao executar a consulta: {err}")  # Exibir erros de consulta
        flash('Erro ao carregar os dados da consulta.', 'error')
        return redirect('/')
    except Exception as e:
        print(f"Ocorreu um erro: {e}")  # Captura qualquer outro erro
        flash('Ocorreu um erro inesperado.', 'error')
        return redirect('/')
    finally:
        if mycursor:
            mycursor.close()
        if conn:
            conn.close()

    return render_template('consulta.html', dados=dados, total_casos=total_casos, data_atualizacao=data_atualizacao)

if __name__ == '__main__':
    app.run(debug=True)
