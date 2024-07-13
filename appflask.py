from flask import Flask, jsonify, send_file, request
import google.generativeai as gmeni
from credenciais import *
from tempfile import NamedTemporaryFile
import os

app = Flask(__name__)

# Configuração da API do Google GenerativeAI
gmeni.configure(api_key=API_KEY)

# Rota para gerar o arquivo HTML e obter o link para download
@app.route('/gerar_html', methods=['GET'])
def gerar_html():
    model = gmeni.GenerativeModel('gemini-pro')
    input_text = f"Crie uma landing page simples voltada para  um escritorio de advocacia, utilizando HTML e com as sessões início, sobre nós e contato respectivamente. O CSS precisa ser escrito no mesmo arquivo"
    response = model.generate_content(input_text)
    generated_html = response.text
    generated_html = generated_html.replace("```html", "").replace("```", "")

    # Conteúdo do arquivo HTML a ser gerado
    html_content = generated_html

    # Nome do arquivo temporário
    filename = 'exemplo.html'

    # Criação do arquivo HTML temporário
    with NamedTemporaryFile(delete=False, suffix='.html') as f:
        temp_filename = f.name
        f.write(html_content.encode('utf-8'))

    # Preparar o caminho absoluto para o arquivo temporário
    temp_path = os.path.abspath(temp_filename)

    # Construir o URL para download do arquivo
    download_url = f"{request.url_root}download/{filename}"

    # Responder com o URL para download
    return jsonify({'download_url': download_url}), 200

# Rota para fazer o download do arquivo HTML
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    temp_path = os.path.join(os.getcwd(), filename)
    return send_file(temp_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
