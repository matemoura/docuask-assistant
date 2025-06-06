import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import Ollama, OllamaEmbeddings


def get_retriever_from_file(uploaded_file):

    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif uploaded_file.name.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado. Use PDF ou DOCX.")
        
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model="llama3")
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

    return vectorstore.as_retriever()

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