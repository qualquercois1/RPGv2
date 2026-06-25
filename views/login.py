import streamlit as st
import controllers.auth_controller as auth_controller

st.title("🛡️ Portal de Acesso")
st.markdown("Bem-vindo! Por favor, faça login ou registre-se para continuar.")

aba_login, aba_registro = st.tabs(["Login", "Novo Registro"])

with aba_login:
    with st.form("login_form"):
        st.subheader("Acessar sua conta")
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")

        if login_button:

            if auth_controller.login(username, password):
                st.success("Bem-vindo!")
                st.rerun()
            else:
                st.error("Nome de usuário ou senha incorretos.")

with aba_registro:
    with st.form("register_form"):
        st.subheader("Criar uma nova conta")
        new_username = st.text_input("Escolha um nome de usuário")
        new_password = st.text_input("Crie uma senha", type="password")
        confirm_password = st.text_input("Confirme a senha", type="password")

        register_button = st.form_submit_button("Registrar")

        if register_button:
            if new_password != confirm_password:
                st.error("As senhas não coincidem.")
            elif not new_username or not new_password:
                st.error("Por favor, preencha todos os campos.")
            else:
                success = auth_controller.register(new_username, new_password)
                if success:
                    st.success("Conta criada com sucesso! Agora você pode fazer login.")
                    if auth_controller.login(new_username, new_password):
                        st.rerun()
                else:
                    st.error("O nome de usuário já existe. Escolha outro.")