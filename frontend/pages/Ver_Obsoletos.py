import streamlit as st
import pandas as pd

st.set_page_config(page_title="Documentos Obsoletos", layout="wide")

st.title("🗂️ Visualizar Documentos Obsoletos")

mock_data = {
    "Nome do Documento": ["IT-001", "FORM-05"],
    "Setor": ["Manutenção", "Qualidade"],
    "Revisão": [0, 2],
    "Status": ["Obsoleto", "Obsoleto"],
    "Data": ["2024-01-10", "2024-03-15"]
}
df = pd.DataFrame(mock_data)

st.info("Aqui são listados todos os documentos que já foram substituídos por uma nova revisão.")

setores = df["Setor"].unique()
for setor in setores:
    with st.expander(f"▼ Setor: {setor}"):
        st.dataframe(df[df["Setor"] == setor])