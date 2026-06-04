from google import genai
from google.genai import types

class EmbeddingService:

    def __init__(self, nome_modelo: str, chave_api: str, tamanho_lote: int=10):
        self.nome_modelo = nome_modelo
        self.cliente = genai.Client(api_key=chave_api)
        self.tamanho_lote = tamanho_lote

    def gerar_embedding_texto(self, textos: list[str]) -> list[list[float]]:
        """
        Gera embeddings fatiando o input para respeitar os limites de contexto.
        """
        embeddings = []
        total_documentos = len(textos)

        for i in range(0, total_documentos, self.tamanho_lote):
            lote_atual = textos[i : i + self.tamanho_lote]
            
            resultado = self.cliente.models.embed_content(
                model=self.nome_modelo,
                contents=lote_atual
            )

            if not resultado.embeddings:
                raise ValueError('A API do Gemini não retornou valores para a geração de embeddings')
            
            for embedding in resultado.embeddings:
                embeddings.append(embedding.values)

        return embeddings
    
    def gerar_embedding_imagem_bytes(self, imagem_bytes: bytes, mime_type: str) -> list[float]:

        part = types.Part.from_bytes(data=imagem_bytes, mime_type=mime_type)
        resultado = self.cliente.models.embed_content(
            model='gemini-embedding-2',
            contents=part,
            config=types.EmbedContentConfig(task_type='SEMANTIC_SIMILARITY')
        )

        if not resultado.embeddings:
            raise ValueError('A API do Gemini não retornou valores para a geração de embeddings')
        elif not resultado.embeddings[0].values:
            raise ValueError('A API do Gemini não retornou valores para a geração de embeddings')
        
        return resultado.embeddings[0].values