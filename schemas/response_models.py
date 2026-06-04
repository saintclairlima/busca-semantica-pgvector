from pydantic import BaseModel
from typing import List, Optional

class TemaSchema(BaseModel):
    nome: str
    subtemas: List[str]
    dominancia: float

class DatabaseResponse(BaseModel):
    indice: Optional[str] = None
    url: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    conteudo: Optional[str] = None
    modelo: Optional[str] = None
    task_type: Optional[str] = None
    cosine_distance: float

class SearchResponse(BaseModel):
    resultados: List[DatabaseResponse]
