import psycopg2
from pgvector.psycopg2 import register_vector

from config.settings import DATABASE_URL


class PostgresConnection:

    @staticmethod
    def get_connection():
        conn = psycopg2.connect(DATABASE_URL)
        register_vector(conn)
        return conn
