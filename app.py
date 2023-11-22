from flask import Flask, render_template, request, jsonify
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
    lb = []
    for i in resultados:
        vl_.append(i[1])
        temp.append(i[2])
        lb.append(i[3].isoformat())
    
    vl_ph = json.dumps(vl_)
    vl_temp = json.dumps(temp)
    vl_lb = json.dumps(lb)
    # Fechar o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()
    # Renderizar a página HTML com os resultados
    return render_template('index.html', resultados=resultados, vl_ph = vl_ph, vl_temp = vl_temp, label= vl_lb)

@app.route('/FiltroAtivo', methods=['POST'])
def buscarPorData():
    dtIni = request.form['initialDate']
    dtFinal = request.form['finalDate']
    try:
        dt_a = datetime.strptime(dtIni, '%Y-%m-%d')
        dt_b = datetime.strptime(dtFinal, '%Y-%m-%d')
    except ValueError:
        dt_a = "2020-10-10"
        dt_b = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
    con = mysql.connector.connect(**db_config)
    cur = con.cursor()
    sql = f"SELECT * FROM Dados WHERE DATE(data) BETWEEN '{dt_a}' AND '{dt_b}'"
    _rs = None
    try:
        cur.execute(sql)
        _rs = cur.fetchall()
    except Exception as e:
        _rs = None
        print(e)
    cur.close()
    con.close()
    vl_ph = []
    vl_temp = []
    vl_label = []
    if _rs != None:
        vl_ = []
        temp = []
        lb = []

        for i in _rs:
            vl_.append(i[1])
            temp.append(i[2])
            lb.append(i[3].isoformat())
        vl_ph = json.dumps(vl_)
        vl_temp = json.dumps(temp)
        vl_label = json.dumps(lb)
    
    return jsonify({'vl_ph':vl_ph , 'vl_temp':vl_temp, 'label':vl_label})
    

@app.route('/grupo/')
def grupo():
    return render_template('grupo.html')

# Garantir que o aplicativo só será executado se este script for o principal
if __name__ == "__main__":
    # Obter a porta do ambiente do Heroku ou usar 5000 como padrão
    port = int(os.environ.get("PORT", 5000))
    
    # Executar o aplicativo na porta especificada
    app.run(host="0.0.0.0", port=port)
