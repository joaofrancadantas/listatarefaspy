from flask import Flask, render_template, request, jsonify, make_response
from markupsafe import escape
from pymongo import MongoClient
from bson.objectid import ObjectId

conexao = MongoClient("...")
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
    return render_template('index.html')

@app.route('/criar-tarefa/<tarefa>', methods=['POST'])
def criar_tarefa(tarefa):
    if request.method == 'POST':
        dados = {
            "tarefa": tarefa
        }
        resposta = colecao.insert_one(dados)
        return jsonify({'ok': True, '_id': str(resposta.inserted_id)}), 201






if __name__ == '__main__':
    app.run(debug=True)