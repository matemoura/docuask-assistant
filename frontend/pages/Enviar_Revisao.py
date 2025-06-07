import streamlit as st
import os
from backend.database import add_document, set_document_obsolete

if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("Você precisa fazer login para acessar esta página.")
    st.stop()

st.title("📤 Enviar Nova Revisão de Documento")

STORAGE_DIR = "document_storage"
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

with st.form("new_revision_form", clear_on_submit=True):
    doc_name = st.text_input("Nome do Documento", placeholder="Ex: IT-001 - Instrução de Trabalho")
    doc_sector = st.text_input("Setor Responsável", placeholder="Ex: Manutenção")
    doc_revision = st.number_input("Nova Revisão (Número)", min_value=0, step=1)
    uploaded_file = st.file_uploader("Selecione o arquivo (PDF ou DOCX)", type=["pdf", "docx"])

    submitted = st.form_submit_button("Enviar")

    if submitted:
        if uploaded_file and doc_name and doc_sector:
            file_path = os.path.join(STORAGE_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            set_document_obsolete(doc_name, doc_sector)
            
            add_document(doc_name, doc_sector, doc_revision, 'current', file_path)
            
            st.success(f"Documento '{doc_name}' (Rev. {doc_revision}) enviado e salvo com sucesso!")
            st.balloons()
        else:
            st.error("Por favor, preencha todos os campos e selecione um arquivo.")