from flask import Flask, render_template, request, redirect, url_for, flash, session  # importando a biblioteca Flask
import database
import sqlite3

app = Flask(__name__) # criando um objeto do flask chamado app

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

'''@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    usuario = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']

    if database.criar_usuario(email, usuario, senha):
        return "Usuário criado com sucesso"
    else:
        return "Isso não funcionou"   '''

if __name__ == '__main__':
    app.run(debug=True)