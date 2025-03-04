import sqlite3
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
#load_dotenv()

# Função para conectar ao banco de dados
def get_db():
    """
    Retorna uma conexão com o banco de dados SQLite.
    """
    db = sqlite3.connect("instance/cemetrom.db")
    db.row_factory = sqlite3.Row  # Para retornar dicionários em vez de tuplas
    return db

# Função para inicializar o banco de dados (cria tabelas se não existirem)
def init_db():
    """
    Cria as tabelas necessárias no banco de dados, se elas não existirem.
    """
    db = get_db()
    try:
        # Tabela de empresas
        db.execute('''
            CREATE TABLE IF NOT EXISTS empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')
        # Tabela de ativos
        db.execute('''
            CREATE TABLE IF NOT EXISTS ativos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                empresa_id INTEGER NOT NULL,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        db.commit()
    finally:
        db.close()

# Função para executar consultas genéricas
def query_db(query, args=(), one=False):
    """
    Executa uma consulta no banco de dados e retorna os resultados.
    :param query: A consulta SQL a ser executada.
    :param args: Parâmetros para a consulta (opcional).
    :param one: Se True, retorna apenas o primeiro resultado (opcional).
    :return: Resultado da consulta.
    """
    db = get_db()
    try:
        cursor = db.execute(query, args)
        results = cursor.fetchall()
        db.commit()
        return (results[0] if results else None) if one else results
    finally:
        db.close()

# Função para inserir dados
def insert_db(query, args=()):
    """
    Insere dados no banco de dados.
    :param query: A consulta SQL de inserção.
    :param args: Parâmetros para a consulta (opcional).
    :return: ID do registro inserido.
    """
    db = get_db()
    try:
        cursor = db.execute(query, args)
        db.commit()
        return cursor.lastrowid
    finally:
        db.close()

# Função para atualizar dados
def update_db(query, args=()):
    """
    Atualiza dados no banco de dados.
    :param query: A consulta SQL de atualização.
    :param args: Parâmetros para a consulta (opcional).
    """
    db = get_db()
    try:
        db.execute(query, args)
        db.commit()
    finally:
        db.close()

# Função para excluir dados
def delete_db(query, args=()):
    """
    Exclui dados do banco de dados.
    :param query: A consulta SQL de exclusão.
    :param args: Parâmetros para a consulta (opcional).
    """
    db = get_db()
    try:
        db.execute(query, args)
        db.commit()
    finally:
        db.close()

# Inicializa o banco de dados ao importar o módulo
init_db()