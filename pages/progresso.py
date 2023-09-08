import streamlit as st
import pandas as pd
import base64

# Configurações iniciais do Streamlit
st.title('📈 Meu progresso')

# Função para download do dataframe
def get_table_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    return href

# Formulário para adicionar metas
with st.expander("Add dados"):
    with st.form(key="add_goal"):
        
        # Se há nomes no dataframe, usa eles como opções, senão, usa uma lista vazia
        available_names = st.session_state.data["NOME"].unique().tolist() if 'data' in st.session_state else []
        
        name = st.selectbox("Nome", options=available_names)
        meta_value = st.number_input("Valor", value=0)
        submit_button = st.form_submit_button("Adicionar/Atualizar Valor")

        # Quando o formulário for enviado, adiciona a meta ao dataframe
        if submit_button and not st.session_state.data.empty:
            meta_name = st.session_state.data[st.session_state.data["NOME"] == name]['META'].iloc[0]
            st.session_state.data.loc[len(st.session_state.data)] = [name, meta_name, meta_value]
            st.success(f"Valor para {name} adicionado com sucesso!")

            # Verifica se a meta foi atingida
            total_value = st.session_state.data[st.session_state.data["NOME"] == name]['VALOR'].sum()
            if total_value >= meta_name:
                st.success(f"Parabéns, {name}! Você conseguiu!")

            # Gráfico da meta escolhida
            st.write(f"Progresso da Meta: {name}")
            st.line_chart(st.session_state.data[st.session_state.data["NOME"] == name][["VALOR"]].cumsum(), use_container_width=True)
