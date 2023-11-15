from flask import Blueprint, render_template

projeto = Blueprint(__name__, "Projeto")

@projeto.route("/")
def home():
    return render_template("index.html")

@projeto.route("/grupo")
def contato():
    return render_template("grupo.html")