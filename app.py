from flask import Flask, render_template
import mysql.connector

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

    # Renderizar a página HTML com os resultados
    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
    