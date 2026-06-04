from typing import Literal
from pydantic import BaseModel

from config.settings import TOP_K_RESULTADOS

class SearchRequest(BaseModel):
    query: str
    top_k: int = TOP_K_RESULTADOS
    tipo: Literal["texto", "imagem"] | None = None