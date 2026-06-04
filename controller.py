from fastapi import APIRouter, HTTPException, Query, FastAPI, Depends, UploadFile, File
from fastapi.responses import JSONResponse

from config.settings import MODELO_EMBEDDINGS, CHAVE_API_GEMINI, TIPOS_IMAGENS_PERMITIDOS
from schemas.request_models import SearchRequest
from schemas.response_models import SearchResponse
from services.embedding_service import EmbeddingService
from services.postgres_vector_repository import PostgresVectorRepository

router = APIRouter()

# Inicialização dos serviços
embedding_service = EmbeddingService(
    nome_modelo=MODELO_EMBEDDINGS,
    chave_api=CHAVE_API_GEMINI
)
repositorio = PostgresVectorRepository()

def gerar_embedding_texto(texto):
    try:
        return embedding_service.gerar_embedding_texto([texto])[0]    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def gerar_embedding_imagem_bytes(imagem_bytes: bytes, mime_type: str) -> list[float]:
    try:
        return embedding_service.gerar_embedding_imagem_bytes(imagem_bytes, mime_type)   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def buscar_similaridade(embedding: list[float], top_k: int, tipo: str|None):
    try:
        resultados = repositorio.buscar_registros_similares(
            embedding=embedding,
            top_k=top_k,
            tipo=tipo
        )
        return {"resultados": resultados}
    except Exception as e:        
        raise HTTPException(status_code=500, detail=str(e))

def buscar_por_texto(query: str, top_k: int, tipo: str|None):
    try:
        embedding = gerar_embedding_texto(query)
        return buscar_similaridade(embedding=embedding, top_k=top_k, tipo=tipo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def buscar_por_imagem(arquivo: UploadFile, top_k: int, tipo: str|None):
    if arquivo.content_type not in TIPOS_IMAGENS_PERMITIDOS:
        raise HTTPException(status_code=400, detail=f"Tipo não suportado: {arquivo.content_type}")
    try:
        imagem_bytes = await arquivo.read()
        embedding = gerar_embedding_imagem_bytes(imagem_bytes=imagem_bytes, mime_type=arquivo.content_type)

        return buscar_similaridade(embedding=embedding, top_k=top_k, tipo=tipo)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/consulta-texto", response_model=SearchResponse, response_class=JSONResponse)
async def buscar_por_texto_get(
    query: str = Query(..., description="Texto a ser buscado"),
    top_k: int = Query(..., description="Quantidade de resultados"),
    tipo: str|None = Query(..., description="Tipo esperado de resultado")
):
    return buscar_por_texto(query, top_k, tipo)

@router.post("/consulta-texto", response_model=SearchResponse)
async def buscar_por_texto_post(request: SearchRequest):
    return buscar_por_texto(request.query, request.top_k, request.tipo)

@router.post("/consulta-imagem", response_model=SearchResponse)
async def buscar_por_imagem_post(
    arquivo: UploadFile = File(...), top_k: int = 10, tipo: str|None = None):
    return await buscar_por_imagem(arquivo=arquivo, top_k=top_k, tipo=tipo)