from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import router

app = FastAPI(title="API de Busca por Similaridade - PGVector e Gemini Embedding 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],     # Allows listed origins
    allow_credentials=False, # Allows cookies/authentication headers
    allow_methods=["*"],     # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allows all custom headers
)

app.include_router(router)