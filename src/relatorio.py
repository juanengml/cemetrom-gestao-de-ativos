from src.database import query_db

class Relatorio:
    @staticmethod
    def ativos_por_empresa():
        return query_db("""
            SELECT empresas.nome AS empresa, COUNT(ativos.id) AS total_ativos
            FROM empresas
            LEFT JOIN ativos ON empresas.id = ativos.empresa_id
            GROUP BY empresas.id
        """)