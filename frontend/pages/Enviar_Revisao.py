import streamlit as st

st.set_page_config(page_title="Enviar Nova Revisão", layout="centered")

st.title("📤 Enviar Nova Revisão de Documento")

with st.form("new_revision_form", clear_on_submit=True):
    st.text_input("Nome do Documento", key="doc_name", placeholder="Ex: IT-001 - Instrução de Trabalho")
    st.text_input("Setor Responsável", key="doc_sector", placeholder="Ex: Manutenção")
    st.number_input("Nova Revisão (Número)", min_value=0, step=1, key="doc_revision")
    uploaded_file = st.file_uploader("Selecione o arquivo (PDF ou DOCX)", type=["pdf", "docx"])

    submitted = st.form_submit_button("Enviar")

    if submitted:
        if uploaded_file is not None and st.session_state.doc_name and st.session_state.doc_sector:
            # A lógica para salvar o arquivo e atualizar o DB virá aqui
            st.success(f"Formulário enviado com sucesso para o arquivo: {uploaded_file.name}")
            st.balloons()
        else:
            st.error("Por favor, preencha todos os campos e selecione um arquivo.")