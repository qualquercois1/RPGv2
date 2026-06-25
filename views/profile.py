import streamlit as st
from models.user import User

if not st.session_state['logged_in']:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

st.title("📊 Perfil do Usuário")

current_user = User.get_user_by_name(st.session_state['username'])

if current_user:
    with st.container(border=True):
        st.subheader(f"Informações do Usuário {current_user.username}")
        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**ID do Usuário:** {current_user.id}")
            st.write(f"**Nome de Usuário:** {current_user.username}")
            st.markdown("**Status da Conta:** 🟢 Ativo")

        with col2:
            st.markdown("**Tipo de Acesso:** Usuário Padrão")
            st.markdown("**Banco de dados Vinculado:** `rpg.db`")
            st.markdown("**Segurança:** 🔒 Senha criptografada com bcrypt")

    st.write("")

    st.subheader("📈 Estatísticas do Sistema")
    
    with st.container(border=True):
        st.write("Aqui estão algumas estatísticas relacionadas ao seu uso do sistema:")
        st.divider()
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.metric(label="Nível do Usuário", value="Level 1", delta="Iniciante")
        with col_meta2:
            st.metric(label="Sessões Iniciadas", value="12", delta="+2 esta semana")
        with col_meta3:
            st.metric(label="Ações Executadas", value="147")

else:
    st.error("Erro ao carregar os dados do perfil. Usuário não encontrado no banco de dados.")