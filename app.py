from flask import Flask, render_template, request, redirect, url_for, flash
from src.database import get_db, query_db, insert_db, update_db, delete_db
import os
#from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
#load_dotenv()

# Configuração do Flask
app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"

# Rota principal (lista de ativos)
@app.route('/')
def listar_ativos():
    """
    Exibe a lista de ativos cadastrados.
    """
    ativos = query_db("SELECT * FROM ativos")
    return render_template('ativos.html', ativos=ativos)

# Rota para adicionar ativo
@app.route('/adicionar_ativo', methods=['GET', 'POST'])
def adicionar_ativo():
    """
    Adiciona um novo ativo ao banco de dados.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        empresa_id = request.form['empresa_id']

        if not nome or not empresa_id:
            flash('Preencha todos os campos!', 'error')
        else:
            insert_db("INSERT INTO ativos (nome, empresa_id) VALUES (?, ?)", (nome, empresa_id))
            flash('Ativo adicionado com sucesso!', 'success')
            return redirect(url_for('listar_ativos'))

    empresas = query_db("SELECT * FROM empresas")
    return render_template('adicionar_ativo.html', empresas=empresas)

# Rota para editar ativo
@app.route('/editar_ativo/<int:id>', methods=['GET', 'POST'])
def editar_ativo(id):
    """
    Edita um ativo existente.
    """
    if request.method == 'POST':
        nome = request.form['nome']
        empresa_id = request.form['empresa_id']

        if not nome or not empresa_id:
            flash('Preencha todos os campos!', 'error')
        else:
            update_db("UPDATE ativos SET nome = ?, empresa_id = ? WHERE id = ?", (nome, empresa_id, id))
            flash('Ativo atualizado com sucesso!', 'success')
            return redirect(url_for('listar_ativos'))

    ativo = query_db("SELECT * FROM ativos WHERE id = ?", (id,), one=True)
    empresas = query_db("SELECT * FROM empresas")
    return render_template('editar_ativo.html', ativo=ativo, empresas=empresas)

# Rota para excluir ativo
@app.route('/excluir_ativo/<int:id>')
def excluir_ativo(id):
    """
    Exclui um ativo do banco de dados.
    """
    delete_db("DELETE FROM ativos WHERE id = ?", (id,))
    flash('Ativo excluído com sucesso!', 'success')
    return redirect(url_for('listar_ativos'))

# Rota para listar empresas
@app.route('/empresas')
def listar_empresas():
    """
    Exibe a lista de empresas cadastradas.
    """
    empresas = query_db("SELECT * FROM empresas")
    return render_template('empresas.html', empresas=empresas)

# Rota para adicionar empresa
@app.route('/adicionar_empresa', methods=['GET', 'POST'])
def adicionar_empresa():
    """
    Adiciona uma nova empresa ao banco de dados.
    """
    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Preencha o nome da empresa!', 'error')
        else:
            insert_db("INSERT INTO empresas (nome) VALUES (?)", (nome,))
            flash('Empresa adicionada com sucesso!', 'success')
            return redirect(url_for('listar_empresas'))

    return render_template('adicionar_empresa.html')

# Rota para editar empresa
@app.route('/editar_empresa/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    """
    Edita uma empresa existente.
    """
    if request.method == 'POST':
        nome = request.form['nome']

        if not nome:
            flash('Preencha o nome da empresa!', 'error')
        else:
            update_db("UPDATE empresas SET nome = ? WHERE id = ?", (nome, id))
            flash('Empresa atualizada com sucesso!', 'success')
            return redirect(url_for('listar_empresas'))

    empresa = query_db("SELECT * FROM empresas WHERE id = ?", (id,), one=True)
    return render_template('editar_empresa.html', empresa=empresa)

# Rota para excluir empresa
@app.route('/excluir_empresa/<int:id>')
def excluir_empresa(id):
    """
    Exclui uma empresa do banco de dados.
    """
    delete_db("DELETE FROM empresas WHERE id = ?", (id,))
    flash('Empresa excluída com sucesso!', 'success')
    return redirect(url_for('listar_empresas'))

# Rota para gerar relatório
@app.route('/relatorio')
def gerar_relatorio():
    """
    Gera um relatório de ativos por empresa.
    """
    relatorio = query_db("""
        SELECT empresas.nome AS empresa, COUNT(ativos.id) AS total_ativos
        FROM empresas
        LEFT JOIN ativos ON empresas.id = ativos.empresa_id
        GROUP BY empresas.id
    """)
    return render_template('relatorio.html', relatorio=relatorio)

# Inicia o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=1234)