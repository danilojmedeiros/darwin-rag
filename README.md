# Sistema RAG para "A Origem das Espécies"

Este projeto implementa um sistema de Retrieval-Augmented Generation (RAG) para consultas sobre o livro "A Origem das Espécies" de Charles Darwin.

## Arquitetura do Sistema

O sistema utiliza uma arquitetura RAG composta pelos seguintes componentes:

1. **Carregamento e Processamento de Documentos:** O texto do livro é carregado e segmentado em pequenos trechos.

2. **Criação de Embeddings e Indexação:** Os segmentos são convertidos em vetores utilizando embeddings do HuggingFace e armazenados em um banco vetorial (Chroma).

3. **API REST e Interface CLI:** O sistema fornece uma API REST e uma interface de linha de comando para interação.

4. **Contêiner Docker**: O projeto está empacotado em um contêiner para facilitar a implantação.

## Requisitos

- Docker e Docker Compose
- Token do HuggingFace (gratuito)

## Instalação e execução

### Usando Docker Compose

1. Clone este repositório:
   ```bash
   git clone https://github.com/danilojmedeiros/darwin-rag.git
   cd darwin-rag
   ```

2. Crie um arquivo `.env` com seu token HuggingFace:
   ```
   HUGGINGFACEHUB_API_TOKEN=seu_token
   ```

3. Execute o sistema:
   ```bash
   docker-compose up --build
   ```

### Usando o container individualmente

1. Construa a imagem:
   ```bash
   docker build -t darwin-rag .
   ```

2. Execute o contêiner:
   ```bash
   docker run -p 8000:8000 -e HUGGINGFACEHUB_API_TOKEN=seu_token darwin-rag
   ```

## Uso

### API REST
A API estará disponível em http://localhost:8000 e inclui os seguintes endpoints:

- `GET /`: Verifica status da API
- `POST /query/`: Envia consultas ao sistema RAG
  ```json
  {
    "question": "What does Darwin say about natural selection?"
  }
  ```
- `GET /get/?question=question_text` → Permite consulta direta pelo navegador.
- `GET /health/`: Verifica a saúde do sistema
- `GET /docs/` → Interface interativa via Swagger UI para testar a API.

### Testes via Navegador

Você pode testar a API diretamente pelo navegador usando URLs como:
```bash
http://localhost:8000/get/?question=What%20does%20Darwin%20say%20about%20select%20natural?
```

Além disso, a documentação interativa pode ser acessada em:
```bash
http://localhost:8000/docs
```

### Usando a API com curl

```bash
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/json" \
     -d '{"question":"What does Darwin say about natural selection?"}'
```

### Interface de linha de comando

Você também pode acessar o contêiner e usar a interface CLI:

```bash
# Acessar o contêiner
docker exec -it nome_do_container sh

# Modo interativo
python cli.py --interactive

# Consulta única
python cli.py --query "What does Darwin say about natural selection?"
```
## Arquitetura do sistema RAG

```mermaid
graph TD
    A[Usuário] -->|Envia requisição| B[API FastAPI]
    B --> |Consulta| C[Sistema RAG]
    
    subgraph "Sistema RAG"
        C1[Vetorizar e Indexar Documentos] 
        C2[Consulta ao Banco Vetorial]
        C3[Modelo de Linguagem (LLM)]
        
        C1 -->|Armazena embeddings| C2
        C2 -->|Retorna chunks relevantes| C3
        C3 -->|Gera resposta final| C
    end

    C --> |Resposta JSON| D["{\"response\": \"Texto gerado pelo LLM\"}"]
    
    subgraph "Componentes"
        C1a[Carrega documentos (TextLoader)]
        C1b[Divide em chunks (RecursiveCharacterTextSplitter)]
        C1c[Gera embeddings (HuggingFaceEmbeddings)]
        C1d[Armazena no banco vetorial (ChromaDB)]
        
        C2a[Busca por similaridade (ChromaDB)]
        C2b[Retorna os chunks mais relevantes]
        
        C3a[Usa Mistral-7B-Instruct]
        C3b[Contextualiza com chunks]
        C3c[Gera resposta final]
        
        C1a --> C1b --> C1c --> C1d
        C1d --> C2a --> C2b
        C2b --> C3a --> C3b --> C3c
    end
```

## Persistência de dados

O sistema mantém seus dados na pasta `./data` que é montada como um volume no contêiner. Isso inclui:
- O arquivo de texto original (origin_of_species.txt)
- O banco de dados vetorial (chroma_db)

## Personalização

Para usar com outros documentos, basta modificar as variáveis FILE_PATH nos arquivos main.py e rag_system.py

## Limitações

- O sistema usa o modelo mistralai/Mistral-7B-Instruct-v0.2 do HuggingFace, que tem capacidades mais limitadas que outros modelos robustos ou pagos.
- A qualidade das respostas depende da qualidade dos chunks recuperados

##  Melhoria na Capacidade de Lidar com Consultas Complexas e Ambiguidades
- Aprimorar a indexação dos documentos: Ajustar o chunk_size e chunk_overlap para otimizar a recuperação de informações sem perder contexto.

- Usar embeddings mais robustos: Testar modelos de embeddings maiores, para melhorar a representação semântica dos textos.

- Adicionar um mecanismo de fallback: Quando a confiança da resposta for baixa, retornar uma resposta genérica ou sugerir reformulação da pergunta.

## Melhoria no Desempenho da API
- Usar multiprocessing para gerar embeddings em paralelo e acelerar a indexação.

- Otimização das consultas: Ajustar search_kwargs dinamicamente com base na complexidade da pergunta.

- Alterar os hiperparâmetros do modelo Mistral-7B-Instruct para equilibrar qualidade e latência.

## Melhoria da Infraestrutura e Implantação
- Uso de cache para respostas frequentes.

- Adicionar suporte ao Kubernetes para facilitar a escalabilidade horizontal da API.

## Monitoramento e Observabilidade
- Logging estruturado: Melhorar os logs para capturar detalhes das requisições e erros.

- Métricas e alertas.