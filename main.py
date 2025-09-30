from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from pymongo import MongoClient
from bson.objectid import ObjectId

conexao = MongoClient(...)
database = conexao.get_database('meubanco')
colecao = database.get_collection('tarefas')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lista-tarefas', methods=['GET','POST'])
def lista_tarefas():   
    tarefasCadastradas = list(colecao.find())
    tarefasProntas = [{'_id': str(tarefa['_id']), 'tarefa': tarefa.get('tarefa', '')} for tarefa in tarefasCadastradas]
    return jsonify(tarefasProntas)


@app.route('/deletar/<tarefa_id>', methods=['POST'])
def deletar_tarefa(tarefa_id):
    if request.method == 'POST':
        resultado = colecao.delete_one({'_id': ObjectId(tarefa_id)})
        print(resultado)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)