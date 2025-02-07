from flask import Flask, request, jsonify
import sqlite3

# Inicializo o flask e inicializa o database
app = Flask(__name__)
DATABASE = 'database.db'


# Faz a conexao ao database + sqlite3
def get_db():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


# Rota de GET para selecionar as tarefas no banco de dados
def get_data():
    conexao = get_db()
    tarefas = conexao.execute(' SELECT * FROM tarefas ').fetchall()
    conexao.close()
    return jsonify([dict(tarefa) for tarefa in tarefas])


# Rota para adicioanr uma nova tarefa na lista
def add_data():
    nova_tarefa = request.json
    conexao = get_db()
    nova_tarefa = conexao.execute(
        ' INSERT INTO tarefas (tarefa) VALUES (?) ',
        (nova_tarefa['tarefa'],)
    )
    # Apos insercao no banco, sempre deve commitar para nao perder a informacao
    conexao.commit()
    conexao.close()
    
    # Mensagem de retorno para Sucesso
    return jsonify({'message': 'Tarefa adicionada com sucesso!'}), 201

def atualizar_data(id):
    tarefa_atualizada = request.json
    conexao = get_db()
    conexao.execute(
        'UPDATE tarefas SET title = ?, completed = ? WHERE id = ?',
        (tarefa_atualizada['title'], tarefa_atualizada['completed'], id))
    
    conexao.commit()
    conexao.close()
    return jsonify({'message': 'Tarefa atualizada com sucesso!'}), 200

def deletar_data(id):
    conexao = get_db()
    conexao.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()
    
    return jsonify({'message': 'Tarefa deletada com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
