import streamlit as st
import pandas as pd
from backend.database import get_obsolete_documents

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()

st.title("🗂️ Visualizar Documentos Obsoletos")

obsolete_docs = get_obsolete_documents()

if not obsolete_docs:
    st.info("Nenhum documento obsoleto encontrado.")
else:
    df = pd.DataFrame(obsolete_docs)
    df = df.rename(columns={
        'name': 'Nome do Documento', 'sector': 'Setor', 
        'revision': 'Revisão', 'created_at': 'Data de Criação'
    })
    
    st.info("Aqui são listados todos os documentos que já foram substituídos por uma nova revisão.")

    setores = df["Setor"].unique()
    for setor in setores:
        with st.expander(f"▼ Setor: {setor}"):
            st.dataframe(df[df["Setor"] == setor])