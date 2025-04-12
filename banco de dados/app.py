from flask import Flask, render_template, request, session, redirect, url_for
import database
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # criando um objeto do flask chamado app
app.secret_key = "SENHA SECRETA"

@app.route('/')
def Pagina_inicial():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if database.fazer_login(form) == True:
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('lista'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/lista')
def lista():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    lista_tarefas = database.buscar_tarefas(session['usuario'])
    print(lista_tarefas)

    return render_template('lista.html', tarefas=lista_tarefas)

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

@app.route('/criar_tarefa', methods=["POST"])
def criar_tarefa():
    form = request.form

    if database.criar_tarefa(form['conteudo'], session['usuario']) == True:
        return redirect(url_for('lista'))
    else:
        return("Ocorreu um erro ao cadastrar a tarefa!")

@app.route('/tarefas/atualizar/<int:id>', methods=["GET"])
def marcar_tarefa(id):
    if database.marcar_tarefa(id):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao marcar tarefa como feita!"

@app.route('/tarefas/excluir/<int:id>', methods=["GET"])
def excluir_tarefa(id):

    email = session['usuario']

    if database.excluir_tarefa(id, email):
        return redirect(url_for('lista'))
    else:
        return "Ocorreu um erro ao excluir a tarefa!"

@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']

    if database.excluir_usuario(email):
        return redirect(url_for('cadastro'))
    else:
        return "Ocorreu um erro ao excluir o usuário"

@app.route('/tarefas/editar/<int:id>', methods=["GET", "POST"])
def editar_tarefa(id):
    # pega o e-mail da sessão para verificar se é o dono da tarefa
    email = session['usuario']
    if (request.method == "GET"):
        conteudo_tarefa = database.buscar_conteudo_tarefa(id)
        return render_template('editar.html', tarefa=conteudo_tarefa, id=id)
    if (request.method == "POST"):
        form = request.form
        novo_conteudo = form['conteudo']
        database.editar_tarefa(novo_conteudo, id)
        return redirect(url_for('lista'))
 
if __name__ == '__main__':
    app.run(debug=True)