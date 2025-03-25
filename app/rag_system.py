from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

def create_rag_system(file_path):
    """Configura um pipeline RAG a partir de um documento de texto."""
    
    # Carregar e dividir
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    splits = text_splitter.split_documents(documents)
    print(f"Documento dividido em {len(splits)} partes.")
    
    # Configurar diretório do banco de vetores
    persist_directory = os.path.join(os.path.dirname(file_path), "chroma_db")
    os.makedirs(persist_directory, exist_ok=True)
    
    # Criar ou carregar embeddings
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:
        print("Carregando banco de vetores existente...")
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding
        )
    else:
        print("Criando novo banco de vetores...")
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=embedding,
            persist_directory=persist_directory
        )
        vectorstore.persist()
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    # Prompt 
    template = """
    "Answer based on the context below. If you don't know, say you don't know.\n\n"
    "Contexto: {context}\n\nPergunta: {question}\n\nResposta:"
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Configurar LLM e pipeline
    llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.1, "max_length": 512})
    
    rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser())
    
    return rag_chain