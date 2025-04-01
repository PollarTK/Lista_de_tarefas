from flask import Flask, render_template, request, session, redirect, url_for
import database
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # criando um objeto do flask chamado app
app.secret_key = "SENHA SECRETA"

@app.route('/')
def Pagina_inicial():
    return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST" :
        form = request.form

        if database.login(form) == True:
            session['usuario'] = form['email']
            return redirect(url_for('lista'))

        else:
            return "Ocorreu um Erro ao Fazer login"
    else:
        return render_template('login.html')

@app.route('/lista')
def lista():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template('lista.html')

# GET serve para "pegar" as informações de uma pagina
# POST serve para enviar informações
@app.route('/cadastro', methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        form = request.form

        if database.criar_usuario(form) == True:
            return render_template('login.html')
        
        else:
            return "Ocorreu um erro ao cadastrar o Usuário"

    else:
        return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)