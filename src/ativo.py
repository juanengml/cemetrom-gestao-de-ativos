from src.database import query_db, insert_db, update_db, delete_db

class Ativo:
    @staticmethod
    def listar_todos():
        return query_db("SELECT * FROM ativos")

    @staticmethod
    def buscar_por_id(id):
        return query_db("SELECT * FROM ativos WHERE id = ?", (id,), one=True)

    @staticmethod
    def criar(nome, empresa_id):
        return insert_db("INSERT INTO ativos (nome, empresa_id) VALUES (?, ?)", (nome, empresa_id))

    @staticmethod
    def atualizar(id, nome, empresa_id):
        update_db("UPDATE ativos SET nome = ?, empresa_id = ? WHERE id = ?", (nome, empresa_id, id))

    @staticmethod
    def excluir(id):
        delete_db("DELETE FROM ativos WHERE id = ?", (id,))