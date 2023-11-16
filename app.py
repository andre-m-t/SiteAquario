from flask import Flask, render_template
import mysql.connector
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "85.10.205.173",
    "user": "aquariogohan",
    "password": "4cb12df0",
    "database": "aquariogohan"
}

@app.route('/projeto/')
def projeto():
    # Conectar ao banco de dados
    conexao = mysql.connector.connect(**db_config)

    # Criar um objeto cursor para interagir com o banco de dados
    cursor = conexao.cursor()

    # Exemplo de consulta SELECT
    consulta = "SELECT * FROM Dados"
    cursor.execute(consulta)

    # Recuperar os resultados da consulta
    resultados = cursor.fetchall()

    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()

    # Preparar dados para o gráfico
    labels = [str(result[3]) for result in resultados]  # assumindo que a data e hora estão na quarta coluna
    dados_ph = [result[1] for result in resultados]  # assumindo que o pH está na segunda coluna
    dados_temperatura = [result[2] for result in resultados]  # assumindo que a temperatura está na terceira coluna

    # Criar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(labels, dados_ph, label='pH', marker='o')
    plt.plot(labels, dados_temperatura, label='Temperatura', marker='o')
    plt.xlabel('Data e Hora')
    plt.ylabel('Valor')
    plt.title('Monitoramento de pH e Temperatura')
    plt.legend()
    plt.grid(True)
    
    # Salvar gráfico em memória
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    
    # Codificar imagem em base64 para exibir em HTML
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    
    # Renderizar a página HTML com os resultados e o gráfico
    return render_template('index.html', resultados=resultados, image_base64=image_base64)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
