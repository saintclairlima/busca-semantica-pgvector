import os
from dotenv import load_dotenv

load_dotenv()

chave_api = os.getenv("GEMINI_API_KEY")
if not chave_api:
    raise ValueError('A variável de ambiente GEMINI_API_KEY deve estar definida para usar o gerador de embeddings Gemini.')

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError('A variável de ambiente DATABASE_URL deve estar definida para realizar as operações de banco de dados.')

CHAVE_API_GEMINI: str = chave_api
DATABASE_URL: str = database_url
MODELO_EMBEDDINGS: str = "gemini-embedding-2"
TOP_K_RESULTADOS: int = 10

TIPOS_IMAGENS_PERMITIDOS = {
    "image/jpeg",
    "image/png",
    "image/webp"
}
