import streamlit as st
import controllers.character_controller as character_controller
import base64
from utils.charts import get_hexagon_chart_html, get_attributes_html

if 'viewing_character_id' not in st.session_state:
    st.session_state['viewing_character_id'] = None


if st.session_state['viewing_character_id'] is None:
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
                            st.rerun()
else:
    
    char_id = st.session_state['viewing_character_id']
    char = character_controller.get_character_by_id(char_id)
    
    if char:
        if st.button("⬅️ Voltar para a Galeria"):
            st.session_state['viewing_character_id'] = None
            st.rerun()
            
        with st.container(border=True):
            st.title(f"🛡️ {char.name}")
            st.caption(f"{char.race} | {char.classe}")
            st.divider()
            
            col_id, col_fisico = st.columns(2)
            
            with col_id:
                st.markdown("### 📜 Identidade")
                st.write(f"**Origem:** {char.region}")
                st.write(f"**Idade:** {char.age} anos")
                
            with col_fisico:
                st.markdown("### 👁️ Biologia")
                st.write(f"**Porte Físico:** {char.physical}")
                st.write(f"**Altura:** {char.height}m")
                st.write(f"**Pele/Olhos:** {char.skin_color} / {char.eye_color}")
                
            st.divider()
            
            st.markdown("### ⚔️ Atributos de Combate")

            attributes = {
                'f' : char.attribute_strength,
                'a' : char.attribute_agility,
                'i' : char.attribute_intelligence, 
                'v' : char.attribute_vitality,
                's' : char.attribute_survival,
                'm' : char.attribute_magic
            }
            
            attr_html = get_attributes_html(**attributes)
            attr_html = '<meta charset="UTF-8">' + attr_html
            b64_html = base64.b64encode(attr_html.encode('utf-8')).decode('utf-8')
            data_url = f"data:text/html;base64,{b64_html}"
            st.iframe(src=data_url, height=230)
            
            st.write("")
            
            hex_html = get_hexagon_chart_html(**attributes)
            hex_html = '<meta charset="UTF-8">' + hex_html
            b64_html = base64.b64encode(hex_html.encode('utf-8')).decode('utf-8')
            st.markdown('<div style="margin-top: -50px;">', unsafe_allow_html=True)
            st.iframe(src=f"data:text/html;charset=utf-8;base64,{b64_html}", height=520)
            st.markdown('</div>', unsafe_allow_html=True)

            
    else:
        st.error("Personagem não encontrado.")
        if st.button("Voltar"):
            st.session_state['viewing_character_id'] = None
            st.rerun()