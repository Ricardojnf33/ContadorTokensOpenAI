from flask import Flask, request, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

modelos = [
    {"nome": "GPT-4 8K", "entrada_usd": 0.03, "entrada_brl": 0.15279, "saida_usd": 0.06, "saida_brl": 0.30558},
    {"nome": "GPT-4 32K", "entrada_usd": 0.06, "entrada_brl": 0.30558, "saida_usd": 0.12, "saida_brl": 0.61116},
    {"nome": "GPT-3.5 Turbo 4K", "entrada_usd": 0.0015, "entrada_brl": 0.00764, "saida_usd": 0.002, "saida_brl": 0.01019},
    {"nome": "GPT-3.5 Turbo 16K", "entrada_usd": 0.003, "entrada_brl": 0.01528, "saida_usd": 0.004, "saida_brl": 0.02038},
    {"nome": "Davinci-002", "entrada_usd": 0.0060, "entrada_brl": 0.03056, "saida_usd": 0.0120, "saida_brl": 0.06112}
]

def arquivo_permitido(nome_arquivo):
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def contar_tokens(texto):
    return len(texto.split())

def calcular_custos(tokens):
    custos_calculados = []

    for modelo in modelos:
        custo_entrada_usd = (tokens / 1000) * modelo["entrada_usd"]
        custo_entrada_brl = (tokens / 1000) * modelo["entrada_brl"]
        custo_saida_usd = (tokens / 1000) * modelo["saida_usd"]
        custo_saida_brl = (tokens / 1000) * modelo["saida_brl"]

        custos_calculados.append({
            "modelo": modelo["nome"],
            "custo_entrada_usd": custo_entrada_usd,
            "custo_entrada_brl": custo_entrada_brl,
            "custo_saida_usd": custo_saida_usd,
            "custo_saida_brl": custo_saida_brl
        })

    return custos_calculados

@app.route('/', methods=['GET', 'POST'])
def carregar_arquivo():
    if request.method == 'POST':
        arquivo = request.files.get('file')
        
        if not arquivo or arquivo.filename == '':
            return render_template('upload.html', erro="Nenhum arquivo selecionado")
        
        if arquivo_permitido(arquivo.filename):
            nome_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
            arquivo.save(nome_arquivo)
            
            with open(nome_arquivo, 'r') as f:
                conteudo = f.read()
                tokens = contar_tokens(conteudo)
                print(f"Quantidade de tokens: {tokens}")  # Printando a quantidade de tokens
                custos = calcular_custos(tokens)
            
            return render_template('upload.html', custos=custos, total_tokens=tokens)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)


