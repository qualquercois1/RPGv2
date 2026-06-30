import streamlit as st
import controllers.character_controller as character_controller

st.title("👥 Meus Personagens")
st.markdown("Selecione um herói para visualizar sua ficha completa.")

personagens = character_controller.get_my_characters()

if not personagens:
    st.info("Você ainda não possui personagens. Vá até a Forja para criar um!")
else:
    with st.container(height=550, border=True):
        for char in personagens:
            with st.container(border=True):
                col_info, col_btn = st.columns([3, 1], vertical_alignment="center")
                
                with col_info:
                    st.subheader(f"🛡️ {char.name}")
                    st.write(f"**Raça:** {char.race} | **Classe:** {char.classe} | **Origem:** {char.region}")
                    
                with col_btn:
                    if st.button("Ver Ficha", key=f"btn_ver_{char.id}", use_container_width=True):
                        st.session_state['viewing_character_id'] = char.id
                        st.switch_page("views/characters/character_sheet.py")
