from src.database import query_db, insert_db, update_db, delete_db

class Empresa:
    @staticmethod
    def listar_todas():
        return query_db("SELECT * FROM empresas")

    @staticmethod
    def buscar_por_id(id):
        return query_db("SELECT * FROM empresas WHERE id = ?", (id,), one=True)

    @staticmethod
    def criar(nome):
        return insert_db("INSERT INTO empresas (nome) VALUES (?)", (nome,))

    @staticmethod
    def atualizar(id, nome):
        update_db("UPDATE empresas SET nome = ? WHERE id = ?", (nome, id))

    @staticmethod
    def excluir(id):
        delete_db("DELETE FROM empresas WHERE id = ?", (id,))