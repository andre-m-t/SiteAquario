from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "85.10.205.173",
    "user": "aquariogohan",
    "password": "4cb12df0",
    "database": "aquariogohan"
}

@app.route('/grupo/')
def grupo():
    return render_template('grupo.html')


# Rota para a página inicial
@app.route('/')
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

    # Renderizar a página HTML com os resultados
    return render_template('index.html', resultados=resultados)


# Garantir que o aplicativo só será executado se este script for o principal
if __name__ == "__main__":
    # Obter a porta do ambiente do Heroku ou usar 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    
    # Executar o aplicativo na porta especificada
    app.run(host="0.0.0.0", port=port)
