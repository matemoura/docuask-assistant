import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from backend.database import get_latest_documents


def get_rag_chain():
    
    llm = Ollama(model="llama3")

    prompt = ChatPromptTemplate.from_template("""
    Você é um assistente especialista em analisar documentos. Use APENAS os trechos de contexto fornecidos para responder à pergunta.
    Se a informação não estiver no contexto, responda: "A informação não foi encontrada no documento."

    Contexto:
    {context}

    Pergunta:
    {question}

    Resposta:
    """)

    rag_chain = prompt | llm | StrOutputParser()
    
    return rag_chain

def build_context_from_latest_docs():
    latest_docs_metadata = get_latest_documents()
    if not latest_docs_metadata:
        return "Nenhum documento encontrado."

    all_texts = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    for doc_meta in latest_docs_metadata:
        file_path = doc_meta['file_path']
        if not os.path.exists(file_path):
            continue 

        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        
        docs = loader.load_and_split(text_splitter)
        all_texts.extend([doc.page_content for doc in docs])
        
    return "\n---\n".join(all_texts)