from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.alunos import AlunoNaoEncontrado, listar_alunos, aluno_por_id, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_blueprint = Blueprint('alunos', __name__)

# ROTA PRINCIPAL PARA ALUNOS
@alunos_blueprint.route('/', methods=['GET'])
def get_index():
    return render_template("index.html")  # Se houver um template de index

# ROTA PARA LISTAR TODOS OS ALUNOS
@alunos_blueprint.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = listar_alunos()
    return render_template("alunos/alunos.html", alunos=alunos)

# ROTA PARA OBTER UM ALUNO ESPECÍFICO POR ID
@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_id.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# ROTA PARA EXIBIR FORMULÁRIO DE CRIAÇÃO DE UM NOVO ALUNO
@alunos_blueprint.route('/alunos/adicionar', methods=['GET'])
def adicionar_aluno_page():
    return render_template('alunos/criarAlunos.html')

# ROTA PARA CRIAR UM NOVO ALUNO
@alunos_blueprint.route('/alunos', methods=['POST'])
def create_aluno():
    try:
        novo_aluno = {
            'nome': request.form['nome'],
            'idade': int(request.form['idade']),
            'data_nascimento': request.form.get('data_nascimento'),
            'nota_primeiro_semestre': float(request.form.get('nota_primeiro_semestre', 0)),
            'nota_segundo_semestre': float(request.form.get('nota_segundo_semestre', 0)),
            'turma_id': int(request.form.get('turma_id'))
        }

        adicionar_aluno(novo_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except ValueError:
        return jsonify({'message': 'Dados inválidos fornecidos'}), 400

# ROTA PARA EXIBIR FORMULÁRIO PARA EDITAR UM ALUNO
@alunos_blueprint.route('/alunos/<int:id_aluno>/editar', methods=['GET'])
def editar_aluno_page(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/aluno_update.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

@alunos_blueprint.route('/alunos/<int:id_aluno>', methods=['POST'])
def update_aluno(id_aluno):
    try:
        idade = request.form.get('idade')
        if idade is not None and idade.strip():
            idade = int(idade)
        else:
            raise ValueError("Idade não pode ser vazia")

        turma_id = request.form.get('turma_id')
        if turma_id is not None and turma_id.strip():
            turma_id = int(turma_id)
        else:
            raise ValueError("Turma ID não pode ser vazio")

        novos_dados = {
            'nome': request.form['nome'],
            'idade': idade,
            'data_nascimento': request.form.get('data_nascimento'),
            'nota_primeiro_semestre': float(request.form.get('nota_primeiro_semestre', 0)),
            'nota_segundo_semestre': float(request.form.get('nota_segundo_semestre', 0)),
            'turma_id': turma_id
        }
        atualizar_aluno(id_aluno, novos_dados)
        return redirect(url_for('alunos.get_aluno', id_aluno=id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400

# ROTA PARA DELETAR UM ALUNO
@alunos_blueprint.route('/alunos/delete/<int:id_aluno>', methods=['POST'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return redirect(url_for('alunos.get_alunos'))
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
