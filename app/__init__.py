from flask import Flask
from flask import Flask, request, rendertemplatestring

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def reportincident():
    if request.method == 'POST':
        nome = request.form.get('nome')
        rua = request.form.get('rua')
        bairro = request.form.get('bairro')
        horario = request.form.get('horario')
        ocorrido = request.form.get('ocorrido')

        # Aqui você pode processar os dados do formulário como quiser.
        # Por exemplo, você pode armazená-los em um banco de dados.
        print(f'Nome: {nome}')
        print(f'Rua: {rua}')
        print(f'Bairro: {bairro}')
        print(f'Horário: {horario}')
        print(f'Ocorrido: {ocorrido}')

        link = f'https://viacep.com.br/ws/{rua}/{bairro}json/'
                                
    # Renderiza o formulário. Em uma aplicação real, você provavelmente
    # quereria usar rendertemplate() e manter seu HTML em um arquivo separado.
    return render_template_string(open("Inicio.html").read())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)