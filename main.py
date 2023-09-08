import streamlit as st
import pandas as pd
import base64

# Configurações iniciais do Streamlit
st.title('Criar/editar metas 📝')
st.write("Insira suas metas e monitore seu progresso!")

# Função para download do dataframe
def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    return href

# Se o dataframe ainda não existe, vamos criá-lo
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["NOME", "META", "VALOR"])

# Formulário para adicionar metas
with st.form(key="add_goal"):
    name = st.text_input("Nome")
    meta_name = st.number_input("Meta (Soma total de valores que quero atingir)", value=0)
    # meta_value = st.number_input("Valor", value=0.0)
    submit_button = st.form_submit_button("Adicionar/Atualizar Valor")

    # Quando o formulário for enviado, adiciona a meta ao dataframe
    if submit_button:
        st.session_state.data.loc[len(st.session_state.data)] = [name, meta_name, 0]
        st.success(f"Valor para {name} adicionado com sucesso!")

        # Verifica se a meta foi atingida
        total_value = st.session_state.data[st.session_state.data["NOME"] == name]['VALOR'].sum()
        if total_value >= meta_name:
            st.success(f"Parabéns, {name}! Você conseguiu!")


# Edição e Exclusão de Entradas
# ... [código anterior]

# Edição e Exclusão de Entradas
# ...

# Edição e Exclusão de Entradas
with st.expander("Editar ou Excluir Metas"):
    if not st.session_state.data.empty:  # Verifique se o dataframe não está vazio
        # Selecione o índice da meta
        index_to_edit_or_delete = st.selectbox("Selecione o índice da meta para editar ou excluir", st.session_state.data.index)

        # Seção de edição
        new_name = st.text_input("Editar Nome", st.session_state.data.at[index_to_edit_or_delete, 'NOME'])
        new_meta = st.number_input("Editar Meta", value=st.session_state.data.at[index_to_edit_or_delete, 'META'])
        new_value = st.number_input("Editar Valor", value=st.session_state.data.at[index_to_edit_or_delete, 'VALOR'])

        with st.form(key="edit_delete_form"):
            form_submit_button = st.form_submit_button("Salvar Alterações")

            # Atualizar os valores se o botão for pressionado
            if form_submit_button:
                st.session_state.data.at[index_to_edit_or_delete, 'NOME'] = new_name
                st.session_state.data.at[index_to_edit_or_delete, 'META'] = new_meta
                st.session_state.data.at[index_to_edit_or_delete, 'VALOR'] = new_value
                st.success("Meta atualizada com sucesso!")
        
        # Seção de exclusão (movido para fora do formulário)
        if st.button("Excluir Meta", key='delete'):
            st.session_state.data = st.session_state.data.drop(index_to_edit_or_delete)  # Remove a linha com base no índice
            st.success("Meta excluída com sucesso!")
    else:
        st.write("Nenhuma meta disponível para edição ou exclusão.")

# ...



# ... [código posterior]




# Exibe o dataframe
st.write("Seus dados até o momento:")
st.write(st.session_state.data)

# Download do dataframe
st.markdown(get_table_download_link(st.session_state.data, "metas_data"), unsafe_allow_html=True)

# Gráfico de linha
# st.write("Progresso das Metas:")
# for name in st.session_state.data["NOME"].unique():
#    st.line_chart(st.session_state.data[st.session_state.data["NOME"] == name][["VALOR"]].cumsum(), use_container_width=True)
