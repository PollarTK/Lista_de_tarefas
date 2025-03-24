from flask import Flask, render_template  # importando a biblioteca Flask


app = Flask(__name__) # criando um objeto do flask chamado

@app.route('/')
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)