import streamlit as st
import pandas as pd
import base64

# Configurações iniciais do Streamlit
st.title('Criar/editar metas 📝')
st.write("Insira suas metas e monitore seu progresso!")

csv_file = "metas_data.csv"

# Ler os dados do CSV
try:
    data = pd.read_csv(csv_file)
except FileNotFoundError:
    data = pd.DataFrame(columns=["NOME", "META", "VALOR"])
    data.to_csv(csv_file, index=False)

# Função para download do dataframe
def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    return href

# Formulário para adicionar metas
with st.form(key="add_goal"):
    name = st.text_input("Nome")
    meta_name = st.number_input("Meta (Soma total de valores que quero atingir)", value=0)
    submit_button = st.form_submit_button("Adicionar/Atualizar Valor")

    if submit_button:
        data.loc[len(data)] = [name, meta_name, 0]
        data.to_csv(csv_file, index=False)
        st.success(f"Valor para {name} adicionado com sucesso!")

# Edição e Exclusão de Entradas
with st.expander("Editar ou Excluir Metas"):
    if not data.empty:  # Verifique se o dataframe não está vazio
        index_to_edit_or_delete = st.selectbox("Selecione o índice da meta para editar ou excluir", data.index)
        new_name = st.text_input("Editar Nome", data.at[index_to_edit_or_delete, 'NOME'])
        new_meta = st.number_input("Editar Meta", value=data.at[index_to_edit_or_delete, 'META'])
        new_value = st.number_input("Editar Valor", value=data.at[index_to_edit_or_delete, 'VALOR'])

        with st.form(key="edit_delete_form"):
            form_submit_button = st.form_submit_button("Salvar Alterações")
            if form_submit_button:
                data.at[index_to_edit_or_delete, 'NOME'] = new_name
                data.at[index_to_edit_or_delete, 'META'] = new_meta
                data.at[index_to_edit_or_delete, 'VALOR'] = new_value
                st.success("Meta atualizada com sucesso!")
                data.to_csv(csv_file, index=False)

        if st.button("Excluir Meta", key='delete'):
            data = data.drop(index_to_edit_or_delete)
            data.to_csv(csv_file, index=False)
            st.success("Meta excluída com sucesso!")
    else:
        st.write("Nenhuma meta disponível para edição ou exclusão.")

# Exibe o dataframe
st.write("Seus dados até o momento:")
st.write(data)

# Download do dataframe
st.markdown(get_table_download_link(data, "metas_data"), unsafe_allow_html=True)
