from flask import Flask, render_template, request
import mysql.connector
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": "85.10.205.173",
    "user": "aquariogohan",
    "password": "4cb12df0",
    "database": "aquariogohan"
}

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
    vl_ = []
    temp = []
    for i in resultados:
        vl_.append(i[1])
        temp.append(i[2])

    vl_ph = json.dumps(vl_)
    vl_temp = json.dumps(temp)
    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()
    # COLETANDO DADOS ATRAVES DO FILTRO 
    # dt_a = request.form["initialDate"]
    # dt_b = request.form["finalDate"]

    dt_a = "2023-01-10"
    dt_b = "2023-11-01"
    # conversao
    dt_a = datetime.strptime(dt_a, '%Y-%m-%d')
    dt_b = datetime.strptime(dt_b, '%Y-%m-%d')
    # pesquisa no banco
    filtro = buscarPorData(dt_a, dt_b)
    filter_ph = []
    filter_temp = []
    for j in filtro:
        filter_ph.append[j[1]]
        filter_temp.append[j[2]]
    ph_f = json.dumps(filter_ph)
    temp_f = json.dumps(filter_temp)
    # Renderizar a página HTML com os resultados
    return render_template('index.html', resultados=resultados, vl_ph = vl_ph, vl_temp = vl_temp, ph_f = ph_f, temp_f=temp_f)

def buscarPorData(dtIni:datetime.date, dtFinal:datetime.date)->list:
    con = mysql.connector.connect(**db_config)
    cur = con.cursor()
    sql = f"SELECT * FROM Dados WHERE DATE(data) BETWEEN '{dtIni}' AND '{dtFinal}'"
    _rs = None
    try:
        cur.execute(sql)
        _rs = cur.fetchall()
        cur.close()
        con.close()
    except Exception as e:
        _rs = None
        print(e)
    return _rs
    

@app.route('/grupo/')
def grupo():
    return render_template('grupo.html')

# Garantir que o aplicativo só será executado se este script for o principal
if __name__ == "__main__":
    # Obter a porta do ambiente do Heroku ou usar 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    
    # Executar o aplicativo na porta especificada
    app.run(host="0.0.0.0", port=port)
