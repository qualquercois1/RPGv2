import streamlit as st
import controllers.character_controller as character_controller
from models.item import Item 

st.title("🎒 Gerenciamento de Inventário")

char_id = st.session_state.get('viewing_character_id')

if not char_id:
    st.warning("⚠️ Nenhum personagem selecionado. Volte para a galeria.")
    if st.button("Voltar para Personagens"):
        st.switch_page("views/characters/characters.py")
    st.stop()

character = character_controller.get_character_by_id(char_id)

if character:
    st.subheader(f"Dono do Inventário: {character.name} ({character.classe})")
    
    peso_atual = character.get_current_weight()
    peso_maximo = character.max_capacity
    
    col_peso1, col_peso2 = st.columns([2, 1])
    with col_peso1:
        porcentagem_uso = min(peso_atual / peso_maximo, 1.0) if peso_maximo > 0 else 0.0
        st.progress(porcentagem_uso)
    with col_peso2:
        st.markdown(f"**Carga:** `{peso_atual:.1f}kg` / `{peso_maximo:.1f}kg`")
        
    if peso_atual > peso_maximo:
        st.error("⚠️ **Sobrecarga!** Este personagem ultrapassou o limite de peso e está lento.")

    st.divider()

    with st.container(border=True):
        st.subheader("📦 Itens na Mochila")
        
        itens = character.get_inventory()
        
        if not itens:
            st.info("Sua mochila está completamente vazia. Adicione itens abaixo para começar sua jornada!")
        else:
            tab_equip, tab_consumiveis, tab_geral = st.tabs(["⚔️ Equipamentos", "🧪 Consumíveis", "📜 Geral"])
            
            with tab_equip:
                equipamentos = [i for i in itens if i.item_type in ["Arma", "Armadura", "Acessório"]]
                if not equipamentos:
                    st.caption("Nenhum equipamento na mochila.")
                for item in equipamentos:
                    with st.container(border=True):
                        col_txt, col_actions = st.columns([3, 1], vertical_alignment="center")
                        with col_txt:
                            status_equip = "🟢 [EQUIPADO] " if item.is_equipped == 1 else "🎒 "
                            st.markdown(f"**{status_equip}{item.name}** *({item.rarity})*")
                            st.caption(f"Qtd: {item.quantity} | Peso Unitário: {item.weight}kg | {item.description}")
                        with col_actions:
                            if item.is_equipped == 1:
                                if st.button("Desequipar", key=f"unequip_{item.id}", use_container_width=True):
                                    item.is_equipped = 0
                                    item.save()
                                    st.rerun()
                            else:
                                if st.button("Equipar", key=f"equip_{item.id}", use_container_width=True):
                                    item.is_equipped = 1
                                    item.save()
                                    st.rerun()
                                    
                            if st.button("Descartar", key=f"del_eq_{item.id}", type="primary", use_container_width=True):
                                item.delete()
                                st.rerun()

            with tab_consumiveis:
                consumiveis = [i for i in itens if i.item_type in ["Consumível", "Pocão"]]
                if not consumiveis:
                    st.caption("Nenhum consumível na mochila.")
                for item in consumiveis:
                    with st.container(border=True):
                        col_txt, col_actions = st.columns([3, 1], vertical_alignment="center")
                        with col_txt:
                            st.markdown(f"🧪 **{item.name}** *({item.rarity})*")
                            st.caption(f"Quantidade: {item.quantity} | Peso Total: {item.weight * item.quantity}kg")
                            if item.description:
                                st.write(f"*{item.description}*")
                        with col_actions:
                            if st.button("Usar (Gastar 1)", key=f"use_{item.id}", use_container_width=True):
                                if item.quantity > 1:
                                    item.quantity -= 1
                                    item.save()
                                else:
                                    item.delete()
                                st.rerun()

            with tab_geral:
                geral = [i for i in itens if i.item_type not in ["Arma", "Armadura", "Acessório", "Consumível", "Pocão"]]
                if not geral:
                    st.caption("Nenhum item geral na mochila.")
                for item in geral:
                    with st.container(border=True):
                        col_txt, col_actions = st.columns([3, 1], vertical_alignment="center")
                        with col_txt:
                            st.markdown(f"📦 **{item.name}** *({item.rarity})*")
                            st.caption(f"Qtd: {item.quantity} | Peso: {item.weight}kg | {item.description}")
                        with col_actions:
                            if st.button("Largar", key=f"drop_{item.id}", type="primary", use_container_width=True):
                                item.delete()
                                st.rerun()

    st.write("")

    with st.expander("🛠️ Forjar / Encontrar Novo Item"):
        with st.form("form_add_item", clear_on_submit=True):
            st.markdown("### 🎲 Registrar Item Encontrado")
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                new_name = st.text_input("Nome do Item", placeholder="Ex: Espada de Ferro, Poção de Mana")
                new_type = st.selectbox("Tipo do Item", ["Geral", "Arma", "Armadura", "Acessório", "Consumível"])
                new_rarity = st.selectbox("Raridade", ["Comum", "Incomum", "Raro", "Épico", "Lendário"])
                
            with col_f2:
                new_qty = st.number_input("Quantidade", min_value=1, value=1, step=1)
                new_weight = st.number_input("Peso Unitário (kg)", min_value=0.0, value=0.5, step=0.1)
                new_desc = st.text_area("Descrição / Efeitos", placeholder="O que esse item faz ou qual a história dele?")
                
            submit_item = st.form_submit_button("Colocar na Mochila", use_container_width=True)
            
            if submit_item:
                if not new_name:
                    st.warning("⚠️ O item precisa de um nome!")
                else:
                    novo_item = Item(
                        character_id=char_id,
                        name=new_name,
                        description=new_desc,
                        item_type=new_type,
                        quantity=new_qty,
                        weight=new_weight,
                        rarity=new_rarity
                    )
                    if novo_item.save():
                        st.success(f"🎒 {new_name} foi guardado na mochila com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao salvar o item no banco.")
else:
    st.error("Personagem inválido ou não encontrado.")