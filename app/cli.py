#!/usr/bin/env python3
from rag_system import create_rag_system
import os
import requests
import argparse

# Caminho para o arquivo
DATA_DIR = "/app/data"
FILE_PATH = os.path.join(DATA_DIR, "origin_of_species.txt")

def check_local_file(output_path):
    """Verifica se o arquivo existe e está acessível."""
    if os.path.exists(output_path):
        print(f"Arquivo encontrado: {output_path}")
        return True
    print(f"Arquivo não encontrado em {output_path}.")
    return False

def main():
    """Inicializa o sistema RAG e gerencia as consultas via linha de comando."""
    parser = argparse.ArgumentParser(description="Sistema RAG para 'A Origem das Espécies'")
    parser.add_argument("--interactive", action="store_true", help="Inicia o modo interativo")
    parser.add_argument("--query", type=str, help="Faz uma única consulta e encerra")
    args = parser.parse_args()
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Verifica se o arquivo existe, senão cria um temporário
    if not check_local_file(FILE_PATH):
        print("Criando arquivo temporário para evitar erros.")
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write("On the Origin of Species by Charles Darwin - Placeholder text for testing")
        print(f"Arquivo temporário criado em {FILE_PATH}")

    # Inicializa o sistema RAG
    print("Carregando sistema RAG...")
    rag_chain = create_rag_system(FILE_PATH)
    print("Sistema pronto para uso!")
    
    if args.query:
        # Consulta única e saída
        try:
            print(f"\nPergunta: {args.query}")
            print(f"Resposta: {rag_chain.invoke(args.query)}\n")
        except Exception as e:
            print(f"Erro ao processar a consulta: {str(e)}")
        return
    
    # Modo interativo
    print("\n=== Sistema RAG: 'A Origem das Espécies' de Charles Darwin ===")
    print("Digite 'sair' para encerrar\n")

    while True:
        user_query = input("Pergunta: ")
        if user_query.lower() == "sair":
            print("Encerrando...")
            break
        try:
            print(f"\nResposta: {rag_chain.invoke(user_query)}\n")
        except Exception as e:
            print(f"Erro ao processar a consulta: {str(e)}")

if __name__ == "__main__":
    main()