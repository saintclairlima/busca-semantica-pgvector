from typing import Any

from psycopg2.extras import RealDictCursor
from config.settings import TOP_K_RESULTADOS
from database.connection import PostgresConnection

class PostgresVectorRepository:
    def buscar_registros_similares(self, embedding: list[float], top_k: int=TOP_K_RESULTADOS, tipo: str|None=None):
        conexao = None
        cursor = None

        try:
            conexao = PostgresConnection.get_connection()            
            cursor = conexao.cursor(cursor_factory=RealDictCursor)
            query = """
            SELECT
                indice,
                url,
                tipo,
                descricao,
                conteudo,
                modelo,
                task_type,
                embeddings <=> %s::vector AS cosine_distance
            FROM gemini_embedding_2
            """

            params: list[Any] = [embedding]

            if tipo is not None:
                query += " WHERE tipo = %s"
                params.append(tipo)

            query += """
            ORDER BY cosine_distance ASC
            LIMIT %s
            """

            cursor.execute(query, (embedding, tipo, top_k))
            resultados = cursor.fetchall()
            return resultados
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()
