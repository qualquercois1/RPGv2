import streamlit as st
import controllers.auth_controller as auth_controller

auth_controller.init_database()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['user_id'] = None

icon_url = "https://png.pngtree.com/png-vector/20190116/ourmid/pngtree-vector-shield-icon-png-image_322145.jpg"

st.logo(icon_url, link="http://localhost:8501")


login_page = st.Page("views/login.py", title="Login", icon="🔑", default=True)
home_page = st.Page("views/home.py", title="Pagina inicial", icon="🏠", default=False)
profile_page = st.Page("views/profile.py", title="Perfil", icon="👤", default=False)
create_character_page = st.Page("views/characters/new_character.py", title="Novo Personagem", default=False)
characters_page = st.Page("views/characters/characters.py", title="Personagens", default=False)
characters_sheet_page = st.Page("views/characters/character_sheet.py", title="Ficha do Personagem", icon="📜", default=False)
config_page = st.Page("views/config.py", title="Pagina de configuração", icon="⚙️", default=False)

if st.session_state['logged_in']:

    pages = {
        "Navegação": [home_page, profile_page],
        "Personagens": [create_character_page, characters_page, characters_sheet_page],
        "Configuração": [config_page],
    }

    nav = st.navigation(pages)

    with st.sidebar:
        st.write("Perfil:")
        st.page_link(profile_page, label=f"{st.session_state['username']}", icon="👤")
        st.write("")
        if st.button("Sair", use_container_width=True):
            auth_controller.logout()
            st.rerun()
    nav.run()
else:
    pages = {
        "Acesso": [login_page],
    }
    nav = st.navigation(pages)
    nav.run()