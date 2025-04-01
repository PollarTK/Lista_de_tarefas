import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key, nome text, senha text)''' )
    
    cursor.execute('''create table if not exists tarefas (id integer primary key, conteudo text, esta_concluida integer, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')

    conexao.commit()

def criar_usuario(formulario):
    # Verifica se ja existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] > 0):
        print("LOG: Já existe esse email cadastrado no banco!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute('''INSERT INTO usuarios (email, nome, senha)
                        VALUES (?, ?, ?)''', (formulario['email'], formulario['nome'], senha_criptografada))
    conexao.commit()
    return True

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] < 0):
        return False
        
    else:
        cursor.execute('''SELECT (senha) from usuarios WHERE email=?''',(formulario['email'],))
        senha_criptografada = cursor.fetchone()
        resultado_verificacao = check_password_hash(senha_criptografada[0], formulario['senha'])
        return resultado_verificacao

if __name__ == '__main__':
    criar_tabelas()