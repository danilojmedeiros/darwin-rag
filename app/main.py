import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from rag_system import create_rag_system
import uvicorn

app = FastAPI(title="Darwin's Origin of Species RAG API")

DATA_DIR = "/app/data"
FILE_PATH = os.path.join(DATA_DIR, "origin_of_species.txt")

class Query(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    """Configuração inicial: verifica se o arquivo de origem existe e inicia o RAG."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(FILE_PATH):
        print(f"Arquivo não encontrado em {FILE_PATH}. Criando um temporário...")
        
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write("On the Origin of Species by Charles Darwin - Placeholder text for testing")

    # NOTA: Dependendo do tamanho do arquivo, seria melhor acessar o arquivo diretamente de um storage em vez de depender de um arquivo local na pasta da aplicação.
    
    print("Inicializando o sistema RAG...")
    global rag_chain
    rag_chain = create_rag_system(FILE_PATH)
    print("RAG Inicializado")

@app.get("/")
def read_root():
    """Verifica se a API está rodando."""
    return {"status": "online", "message": "Darwin's Origin of Species RAG API"}

@app.post("/query/")
def query_rag(query: Query):
    """Consulta o sistema RAG via POST."""
    try:
        return {"response": rag_chain.invoke(query.question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta: {str(e)}")

@app.get("/get/")
async def get_query(question: str):
    """Consulta o sistema RAG via GET."""
    try:
        return {"question": question, "response": rag_chain.invoke(question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta: {str(e)}")

@app.get("/health/")
def health_check():
    """Checa o status do sistema."""
    return {"status": "healthy", "file_loaded": os.path.exists(FILE_PATH)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)