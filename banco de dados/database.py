import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("tarefas.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key, nome text, senha text)''' )
    
    cursor.execute('''create table if not exists tarefas id integer primary key, conteudo text, esta_concluida integer, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')

    conexao.commit()

if __name__ == '__main__':
    criar_tabelas()