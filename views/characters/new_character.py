import streamlit as st
import controllers.character_controller as character_controller

st.title("🛡️ Forja de Personagens")

with st.form('form_criar_personagem', border=True):
    st.subheader('🗡️ Hora de criar um novo herói.')
    st.markdown("Preencha os detalhes para registrar sua nova lenda no sistema.")
    
    st.divider()

    st.markdown("### 📜 Identidade e Origem")
    col_id1, col_id2, col_id3 = st.columns(3)
    
    with col_id1:
        name = st.text_input("Nome do Personagem")

        race = st.selectbox("Raça", ["Humano", "Elfo", "Anão", "Orc", "Draconato"])
        
    with col_id2:
        classe = st.selectbox("Classe", ["Guerreiro", "Mago", "Ladino", "Arqueiro", "Paladino", "Clérigo"])
        age = st.number_input("Idade", min_value=1, max_value=1000, step=1)
        
    with col_id3:
        region = st.text_input("Reino de Origem")

    st.divider()

    st.markdown("### 👁️ Aparência Física")
    col_ap1, col_ap2 = st.columns(2)
    
    with col_ap1:
        height = st.number_input("Altura (m)", min_value=0.5, max_value=3.0, step=0.01)
        physical = st.selectbox("Porte Físico", ["Magro", "Atlético", "Musculoso", "Robusto", "Franzino"])
        
    with col_ap2:
        eye_color = st.text_input("Cor dos Olhos")
        skin_color = st.text_input("Tom de Pele")

    st.divider()

    st.markdown("### ⚔️ Atributos (Distribuição de Pontos)")
    col_attr1, col_attr2, col_attr3 = st.columns(3)
    
    with col_attr1:
        attr_str = st.number_input("Força", min_value=1, max_value=100, value=10)
        attr_int = st.number_input("Inteligência", min_value=1, max_value=100, value=10)
        
    with col_attr2:
        attr_agi = st.number_input("Agilidade", min_value=1, max_value=100, value=10)
        attr_sur = st.number_input("Sobrevivência", min_value=1, max_value=100, value=10)
        
    with col_attr3:
        attr_vit = st.number_input("Vitalidade", min_value=1, max_value=100, value=10)
        attr_mag = st.number_input("Magia", min_value=1, max_value=100, value=10)

    st.divider()
    submit_button = st.form_submit_button("Forjar Personagem", use_container_width=True)

    if submit_button:
        if not name or not region:
            st.warning("⚠️ O Nome e o Reino de Origem são obrigatórios!")
        else:
            sucesso, mensagem = character_controller.register_character(
                name, age, eye_color, skin_color, classe, height, physical, race, region, 
                attr_str, attr_agi, attr_vit, attr_int, attr_sur, attr_mag
            )
            
            if sucesso:
                st.success(mensagem)
                st.balloons()
            else:
                st.error(mensagem)