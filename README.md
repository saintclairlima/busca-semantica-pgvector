# Busca Semântica com PGVector e Gemini Embedding

API de busca semântica construída com FastAPI, PostgreSQL + PGVector e Gemini Embedding 2.

# Resumo da Configuração e Inicialização
## 1. Clonar o repositório

```bash
git clone https://github.com/saintclairlima/busca-semantica-pgvector.git

cd busca-semantica-pgvector
```

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 3. Criar arquivo `.env`

```bash
cp .env_template .env
```

Substituir os valores

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco
GEMINI_API_KEY=sua_chave_gemini
```

## 4. Inicializar

```bash
uvicorn main:app
```

Ou adicionar opções:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
`host`: Expõe para acesso irrestrito dentro da rede

`port`: define a porta a ser usada. Em ambientes como o Supabase, deve ser usado como valor a variável de ambiente `$PORT` (`--port $PORT`).

`reload`: reinicia a aplicação quando há mudança nos arquivos de código (para ambientes de desenvolvimento)

Por padrão, a API ficará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

Documentação ReDoc:

```text
http://localhost:8000/redoc
```

---

# Sobre o projeto

O projeto permite realizar consultas por similaridade utilizando texto ou imagens. A partir da consulta enviada, um embedding é gerado pelo modelo Gemini Embedding 2 e comparado com embeddings previamente armazenados no PostgreSQL utilizando a extensão PGVector.

## O que o projeto faz

Esta API fornece um mecanismo de busca vetorial capaz de encontrar conteúdos semanticamente semelhantes a partir de:

- Consultas textuais
- Consultas por imagem

O fluxo geral funciona da seguinte forma:

1. O usuário envia um texto ou uma imagem.
2. A API gera um embedding utilizando o modelo Gemini Embedding 2.
3. O embedding é comparado com vetores armazenados no PostgreSQL.
4. O PGVector calcula a distância de similaridade.
5. Os registros mais próximos são retornados ordenados por relevância.

### Casos de uso

- Busca semântica de documentos
- Recuperação de conteúdo por similaridade
- Sistemas RAG (Retrieval-Augmented Generation)
- Busca multimodal (texto ↔ imagem)
- Catálogos de conteúdo indexado
- Sistemas de recomendação baseados em embeddings

---

# Tecnologias Utilizadas

- Python
- FastAPI
- PostgreSQL
- PGVector
- Gemini Embedding 2
- Psycopg2
- Pydantic
- Uvicorn

---

# Estrutura do Repositório

```text
busca-semantica-pgvector/
│
├── config/
│   └── settings.py
│
├── database/
│   └── connection.py
│
├── schemas/
│   ├── request_models.py
│   └── response_models.py
│
├── services/
│   ├── embedding_service.py
│   └── postgres_vector_repository.py
│
├── controller.py
├── main.py
├── requirements.txt
├── .env_template
└── README.md
```

## Descrição dos Componentes

### `main.py`

Ponto de entrada da aplicação.

Responsável por:

- Inicializar o FastAPI
- Configurar CORS
- Registrar as rotas da API

---

### `controller.py`

Camada responsável pelos endpoints HTTP.

Implementa:

#### Busca por texto

```http
GET /consulta-texto
POST /consulta-texto
```

Recebe uma consulta textual, gera o embedding correspondente e retorna os registros mais similares.

#### Busca por imagem

```http
POST /consulta-imagem
```

Recebe um arquivo de imagem, gera seu embedding e executa a busca vetorial.

Também concentra:

- Tratamento de erros
- Validação de tipos de imagem
- Integração entre serviços e repositório

---

### `config/settings.py`

Centraliza as configurações da aplicação.

Variáveis utilizadas:

| Variável | Descrição |
|-----------|------------|
| DATABASE_URL | String de conexão PostgreSQL |
| GEMINI_API_KEY | Chave da API Gemini |

Constantes internas:

```python
MODELO_EMBEDDINGS = "gemini-embedding-2"
TOP_K_RESULTADOS = 10
```

---

### `database/connection.py`

Responsável pela conexão com PostgreSQL.

Funções:

- Cria conexão via Psycopg2
- Registra suporte ao tipo vetorial PGVector

---

### `services/embedding_service.py`

Camada responsável pela geração dos embeddings.

Implementa:

#### Embeddings de texto

```python
gerar_embedding_texto()
```

- Recebe uma lista de textos
- Faz processamento em lotes
- Chama a API Gemini

#### Embeddings de imagem

```python
gerar_embedding_imagem_bytes()
```

- Recebe bytes da imagem
- Utiliza Gemini Embedding 2
- Configura o task type como:

```python
SEMANTIC_SIMILARITY
```

---

### `services/postgres_vector_repository.py`

Camada de acesso aos dados vetoriais.

Responsável por:

- Consultar a tabela vetorial
- Executar busca por similaridade
- Ordenar resultados pela distância vetorial

A consulta utiliza:

```sql
embeddings <=> %s::vector
```

que representa a distância de similaridade do PGVector.

Tabela esperada:

```sql
gemini_embedding_2
```

Campos utilizados:

```sql
indice
url
tipo
descricao
conteudo
modelo
task_type
embeddings
```

---

### `schemas/request_models.py`

Modelos de entrada da API.

Exemplo:

```json
{
  "query": "inteligência artificial",
  "top_k": 10,
  "tipo": "texto"
}
```

---

### `schemas/response_models.py`

Modelos de saída.

Exemplo:

```json
{
  "resultados": [
    {
      "indice": "123",
      "url": "https://...",
      "tipo": "texto",
      "descricao": "...",
      "conteudo": "...",
      "modelo": "gemini-embedding-2",
      "task_type": "SEMANTIC_SIMILARITY",
      "cosine_distance": 0.12
    }
  ]
}
```

---

# Estrutura Esperada do Banco de Dados

O projeto pressupõe que exista uma tabela semelhante a:

```sql
CREATE TABLE gemini_embedding_2 (
    indice TEXT,
    url TEXT,
    tipo TEXT,
    descricao TEXT,
    conteudo TEXT,
    modelo TEXT,
    task_type TEXT,
    embeddings VECTOR(3072)
);
```

Também é necessário que a extensão PGVector esteja instalada:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

# Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/saintclairlima/busca-semantica-pgvector.git

cd busca-semantica-pgvector
```

---

## 2. Criar ambiente virtual

### Linux/macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variáveis de ambiente

Copie o template:

```bash
cp .env_template .env
```

Configure:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/banco
GEMINI_API_KEY=sua_chave_gemini
```

---

# Inicialização

Inicie o servidor:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

Documentação ReDoc:

```text
http://localhost:8000/redoc
```

---

# Exemplos de Uso

## Consulta por texto (GET)

```http
GET /consulta-texto?query=inteligencia%20artificial&top_k=10&tipo=texto
```

---

## Consulta por texto (POST)

```http
POST /consulta-texto
Content-Type: application/json
```

```json
{
  "query": "inteligência artificial",
  "top_k": 10,
  "tipo": "texto"
}
```

---

## Consulta por imagem

```http
POST /consulta-imagem
```

Multipart Form Data:

```text
arquivo=<imagem.jpg>
top_k=10
tipo=imagem
```

---

# Fluxo da Busca Semântica

```text
Usuário
   │
   ▼
Texto ou Imagem
   │
   ▼
Gemini Embedding 2
   │
   ▼
Embedding Vetorial
   │
   ▼
PGVector
   │
   ▼
Busca por Similaridade
   │
   ▼
Top K Resultados
```

---

# Limitações e Observações

- A API não realiza indexação de documentos.
- Os embeddings devem existir previamente na tabela.
- O projeto é apenas a camada de consulta.
- O modelo utilizado é fixo (`gemini-embedding-2`).
- O filtro por tipo depende dos valores armazenados na coluna `tipo`.
- Atualmente são aceitas apenas imagens:
  - JPEG
  - PNG
  - WEBP

---

# Dependências

```text
fastapi
uvicorn
google-genai
psycopg2-binary
pgvector
python-dotenv
python-multipart
pydantic
```

---

# Arquitetura Resumida

```text
FastAPI
   │
   ├── Controller
   │
   ├── EmbeddingService
   │        │
   │        └── Gemini Embedding 2
   │
   └── PostgresVectorRepository
            │
            └── PostgreSQL + PGVector
```

Essa arquitetura mantém separadas as responsabilidades de API, geração de embeddings e persistência/consulta vetorial, facilitando manutenção e evolução do projeto.
