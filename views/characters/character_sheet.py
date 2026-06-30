import streamlit as st
import controllers.character_controller as character_controller
import base64
from utils.charts import get_hexagon_chart_html, get_attributes_html

if 'viewing_character_id' not in st.session_state or st.session_state['viewing_character_id'] is None:
    st.warning("Nenhum personagem selecionado.")
    st.switch_page("views/characters/characters.py")

char_id = st.session_state['viewing_character_id']
char = character_controller.get_character_by_id(char_id)

if not char:
    st.error("Erro ao carregar o personagem.")
    st.stop()

st.markdown("""
    <style>
        /* Remove a barra lateral da renderização */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        /* Remove o botão superior esquerdo (setinha) que reabre a sidebar */
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        /* Opcional: Ajusta a margem do topo para preencher o espaço vazio */
        [data-testid="stHeader"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

if st.button("⬅️ Voltar para a Galeria"):
    st.session_state['viewing_character_id'] = None
    st.switch_page("views/characters/characters.py")

st.divider()

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
    b64_attr = base64.b64encode(attr_html.encode('utf-8')).decode('utf-8')
    st.iframe(src=f"data:text/html;charset=utf-8;base64,{b64_attr}", height=250)
    
    st.write("")
    
    hex_html = get_hexagon_chart_html(**attributes)
    hex_html = '<meta charset="UTF-8">' + hex_html
    b64_hex = base64.b64encode(hex_html.encode('utf-8')).decode('utf-8')
    
    st.markdown('<div style="margin-top: -50px;">', unsafe_allow_html=True)
    st.iframe(src=f"data:text/html;charset=utf-8;base64,{b64_hex}", height=520)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Ir para inventario"):
    st.switch_page("views/inventory/itens.py")