import streamlit as st

st.set_page_config(page_title='Disciplinas', page_icon='📖')

st.title("Gestão de disciplinas")

tab_lista, tab_novo = st.tabs("Listar", "Nova disciplina")

with tab_novo:
    st.subheader('Cadastrar novas matérias')
    with st.form('form_disciplina'):
        nome = st.text_input('Nome da Disciplina')
        professor = st.text_input('Nome do professor')
        dia_semana = st.selectbox('Dia da aula', ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'])
        
        submitted = st.form_submit_button('Salvar')
        if submitted:
            st.success(f'Disciplina {nome} cadastrada! (Simulação)')

with tab_lista:
    st.info('A conexão com o Xano virá na Tarefa 13.')
    st.dataframe([
    {'Nome': 'Python Basics', 'Professor': 'Oriel', 'Dia': 'Seg'},
    {'Nome': 'No-Code Advance', 'Professor': 'Giuliano', 'Dia': 'Qui'},
    ], width='stretch')
