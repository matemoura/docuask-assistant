import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.core import get_retriever_from_file, get_rag_chain


st.set_page_config(page_title="IA para Documentos", layout="wide")
st.title("🤖 Converse com seus Documentos")
st.markdown("Faça o upload de um arquivo PDF ou Word e faça perguntas sobre o conteúdo.")


@st.cache_resource(show_spinner="Processando documento...")
def cached_get_retriever(uploaded_file):
    return get_retriever_from_file(uploaded_file)

uploaded_file = st.file_uploader("Escolha um arquivo PDF ou Word", type=["pdf", "docx"])

if uploaded_file:
    st.download_button(
        label="Clique para baixar o arquivo original",
        data=uploaded_file.getvalue(),
        file_name=uploaded_file.name,
    )
    
    try:
        retriever = cached_get_retriever(uploaded_file)
        st.success(f"Arquivo **{uploaded_file.name}** processado com sucesso!")
        
        question = st.text_input("Faça sua pergunta sobre o documento:", placeholder="Qual o resumo do documento?")
        
        if question:
            retrieved_docs = retriever.invoke(question)
            context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
            rag_chain = get_rag_chain()
            
            with st.spinner("Gerando resposta..."):
                answer = rag_chain.invoke({"context": context, "question": question})
                st.write(answer)
                
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")