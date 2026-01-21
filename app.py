"""
💍 Gerenciador de Casamento
Aplicação em Streamlit para planejamento completo de casamento
Com persistência de dados no Supabase (PostgreSQL na nuvem)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.supabase_client import (
    get_all_items, add_item, update_item, delete_item, update_all_items,
    get_all_tasks, add_task, update_task, delete_task,
    get_config, update_config, update_all_config,
    get_all_categorias, add_categoria, update_categoria, delete_categoria,
    get_all_orcamentos, add_orcamento, update_orcamento, delete_orcamento
)
from utils.calculations import (
    calcular_total_orcado, calcular_reserva, calcular_porcentagem_usada,
    calcular_investimento_mensal, formatar_moeda, calcular_porcentagem_tarefas
)

# Configuração da página (mobile-first)
st.set_page_config(
    page_title="💍 Gerenciador de Casamento",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar começa fechada em mobile
)


def load_mobile_css():
    """Carrega CSS responsivo para mobile"""
    st.markdown("""
    <style>
        /* ========== DESKTOP STYLES ========== */
        .main {
            background-color: #FFF5F7;
        }
        .stButton>button {
            background-color: #FF69B4;
            color: white;
        }
        .stButton>button:hover {
            background-color: #FF1493;
            color: white;
        }
        
        /* ========== MOBILE OPTIMIZATION ========== */
        @media (max-width: 768px) {
            /* Aumentar fonte base para evitar zoom automático no iOS */
            html {
                font-size: 16px !important;
            }
            
            /* Sidebar colapsável automática */
            section[data-testid="stSidebar"] {
                width: 0px;
            }
            
            section[data-testid="stSidebar"][aria-expanded="true"] {
                width: 80vw;
            }
            
            /* Botões touch-friendly (mínimo 44x44px - Apple guidelines) */
            .stButton button {
                min-height: 48px !important;
                width: 100% !important;
                font-size: 16px !important;
                margin: 8px 0 !important;
                padding: 12px 24px !important;
            }
            
            /* Inputs maiores e mais fáceis de tocar */
            .stTextInput input,
            .stNumberInput input,
            .stSelectbox select,
            .stTextArea textarea {
                min-height: 48px !important;
                font-size: 16px !important;
                padding: 12px !important;
            }
            
            /* Métricas responsivas */
            [data-testid="stMetricValue"] {
                font-size: 24px !important;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 14px !important;
            }
            
            [data-testid="stMetricDelta"] {
                font-size: 12px !important;
            }
            
            /* Tabelas com scroll horizontal suave */
            .dataframe {
                font-size: 12px !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch;
            }
            
            /* Cards para substituir tabelas em mobile */
            .mobile-card {
                background: #262730;
                border-radius: 12px;
                padding: 16px;
                margin: 12px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }
            
            .mobile-card-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 12px;
                color: #fff;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .mobile-card-row {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #3d3d4a;
            }
            
            .mobile-card-row:last-child {
                border-bottom: none;
            }
            
            .mobile-card-label {
                font-size: 14px;
                color: #a0a0a0;
                flex: 0 0 40%;
            }
            
            .mobile-card-value {
                font-size: 14px;
                color: #fff;
                font-weight: 500;
                flex: 1;
                text-align: right;
            }
            
            /* Expanders mais espaçados */
            .streamlit-expanderHeader {
                font-size: 16px !important;
                padding: 16px !important;
                min-height: 48px !important;
            }
            
            /* Títulos responsivos */
            h1 {
                font-size: 28px !important;
                line-height: 1.3 !important;
            }
            
            h2 {
                font-size: 22px !important;
                line-height: 1.3 !important;
            }
            
            h3 {
                font-size: 18px !important;
                line-height: 1.3 !important;
            }
            
            /* Checkbox maiores */
            input[type="checkbox"] {
                width: 24px !important;
                height: 24px !important;
            }
            
            /* Form submit buttons */
            .stFormSubmitButton button {
                min-height: 48px !important;
                width: 100% !important;
                font-size: 16px !important;
            }
            
            /* Radio buttons maiores */
            .stRadio label {
                padding: 12px !important;
                font-size: 16px !important;
            }
            
            /* Dividers com mais espaço */
            hr {
                margin: 24px 0 !important;
            }
        }
        
        /* ========== TABLET (768px - 1024px) ========== */
        @media (min-width: 768px) and (max-width: 1024px) {
            .stButton button {
                min-height: 44px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)


# Carregar CSS responsivo
load_mobile_css()

# Header
st.title("💍 Gerenciador de Casamento")
st.markdown("### Organize seu grande dia com amor e planejamento! 💕")
st.markdown("---")

# Carregar dados do Supabase
with st.spinner("⏳ Carregando dados do Supabase..."):
    items = get_all_items()
    config = get_config()
    tasks = get_all_tasks()

# Sidebar para navegação
st.sidebar.title("📋 Menu de Navegação")
menu_option = st.sidebar.radio(
    "Escolha uma seção:",
    ["🏠 Dashboard", "📋 Itens do Casamento", "💰 Planejamento Financeiro", 
     "✅ Checklist", "📊 Relatórios", "💸 Orçamentos"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💝 Dicas")
st.sidebar.info("💡 Mantenha seu orçamento atualizado regularmente!")


# ==================== HELPER FUNCTIONS ====================
# ==================== SEÇÃO: DASHBOARD ====================
if menu_option == "🏠 Dashboard":
    st.header("🏠 Dashboard - Visão Geral")
    
    # Calcular métricas principais
    total_orcado = calcular_total_orcado(items)
    orcamento_maximo = config.get('orcamento_maximo', 30000.0)
    reserva = calcular_reserva(orcamento_maximo, total_orcado)
    porcentagem_usada = calcular_porcentagem_usada(orcamento_maximo, total_orcado)
    
    # Métricas em colunas (2 colunas para mobile-friendly)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "💰 Orçamento Máximo",
            formatar_moeda(orcamento_maximo)
        )
    
    with col2:
        st.metric(
            "📊 Total Orçado",
            formatar_moeda(total_orcado),
            delta=f"{porcentagem_usada:.1f}% usado",
            delta_color="inverse"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.metric(
            "💵 Reserva Disponível",
            formatar_moeda(reserva),
            delta=f"{100-porcentagem_usada:.1f}% livre"
        )
    
    with col4:
        porcentagem_tarefas = calcular_porcentagem_tarefas(tasks)
        st.metric(
            "✅ Tarefas Concluídas",
            f"{porcentagem_tarefas:.0f}%",
            delta=f"{sum(1 for t in tasks if t.get('concluida', False))}/{len(tasks)}"
        )
    
    # Barra de progresso do orçamento com porcentagem visível
    st.markdown(f"### 📈 Progresso do Orçamento - {porcentagem_usada:.1f}% Utilizado")
    st.progress(min(porcentagem_usada / 100, 1.0))
    st.write(f"**{formatar_moeda(total_orcado)}** de **{formatar_moeda(orcamento_maximo)}** ({porcentagem_usada:.1f}% usado)")
    
    # Alertas visuais baseados na porcentagem
    if porcentagem_usada >= 90:
        st.error("⚠️ Atenção! Orçamento quase esgotado!")
    elif porcentagem_usada >= 80:
        st.warning("⚡ Cuidado! Você já usou mais de 80% do orçamento.")
    elif porcentagem_usada >= 50:
        st.info("📊 Acompanhe o orçamento - você já usou mais de 50%.")
    else:
        st.success("✅ Ótimo! Você ainda tem mais de 50% do orçamento disponível.")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🥧 Distribuição dos Gastos")
        # Filtrar apenas itens com preço > 0
        items_com_preco = [item for item in items if item['preco'] > 0]
        
        if items_com_preco:
            df_gastos = pd.DataFrame(items_com_preco)
            fig = px.pie(
                df_gastos,
                values='preco',
                names='item',
                title='Distribuição por Item',
                color_discrete_sequence=px.colors.sequential.RdPu
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Adicione itens com preços para ver o gráfico de distribuição.")
    
    with col2:
        st.markdown("### 📊 Status dos Itens")
        # Contar itens por status
        status_count = {}
        for item in items:
            status = item.get('status', 'Pendente')
            status_count[status] = status_count.get(status, 0) + 1
        
        df_status = pd.DataFrame(
            list(status_count.items()),
            columns=['Status', 'Quantidade']
        )
        
        fig = px.bar(
            df_status,
            x='Status',
            y='Quantidade',
            title='Itens por Status',
            color='Status',
            color_discrete_map={'Contratado': '#90EE90', 'Pendente': '#FFB6C1'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Próximas tarefas pendentes
    st.markdown("### 📝 Próximas Tarefas Pendentes")
    tarefas_pendentes = [t for t in tasks if not t.get('concluida', False)][:5]
    
    if tarefas_pendentes:
        for tarefa in tarefas_pendentes:
            st.markdown(f"- ⏳ {tarefa['tarefa']}")
    else:
        st.success("🎉 Parabéns! Todas as tarefas foram concluídas!")


# ==================== SEÇÃO: ITENS DO CASAMENTO ====================
elif menu_option == "📋 Itens do Casamento":
    st.header("📋 Itens do Casamento")
    
    # Filtro de status
    col1, col2 = st.columns([3, 1])
    with col1:
        filtro_status = st.selectbox(
            "Filtrar por status:",
            ["Todos", "Contratado", "Pendente"]
        )
    
    # Aplicar filtro
    if filtro_status == "Todos":
        items_filtrados = items
    else:
        items_filtrados = [item for item in items if item.get('status') == filtro_status]
    
    # Converter para DataFrame
    df_items = pd.DataFrame(items_filtrados)
    
    # Renomear colunas para exibição
    if not df_items.empty:
        df_items_display = df_items.copy()
        
        # Remover coluna created_at se existir (vem do Supabase)
        if 'created_at' in df_items_display.columns:
            df_items_display = df_items_display.drop('created_at', axis=1)
        
        # Agora renomear as 6 colunas restantes
        df_items_display.columns = ['ID', 'Item', 'Serviço', 'Preço', 'Status', 'Comentários']
        
        # Editor de dados
        st.markdown("### 📝 Tabela de Itens")
        edited_df = st.data_editor(
            df_items_display,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Preço": st.column_config.NumberColumn(
                    "Preço (R$)",
                    format="R$ %.2f",
                    min_value=0.0
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pendente", "Contratado"],
                    required=True
                )
            },
            hide_index=True
        )
        
        # Botão para salvar alterações
        if st.button("💾 Salvar Alterações", use_container_width=True, type="primary"):
            # Converter de volta para formato original
            edited_df.columns = ['id', 'item', 'servico', 'preco', 'status', 'comentarios']
            items_atualizados = edited_df.to_dict('records')
            
            with st.spinner("⏳ Salvando no Supabase..."):
                if update_all_items(items_atualizados):
                    st.success("✅ Alterações salvas com sucesso no Supabase!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar alterações. Tente novamente.")
    
    # Formulário para adicionar novo item
    st.markdown("### ➕ Adicionar Novo Item")
    with st.form("novo_item_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            novo_item = st.text_input("Item *", placeholder="Ex: Lembrancinhas")
        
        with col2:
            novo_servico = st.text_input("Serviço/Fornecedor", placeholder="Nome do fornecedor")
        
        with col3:
            novo_preco = st.number_input("Preço (R$)", min_value=0.0, step=100.0)
        
        col4, col5 = st.columns(2)
        
        with col4:
            novo_status = st.selectbox("Status", ["Pendente", "Contratado"])
        
        with col5:
            novos_comentarios = st.text_input("Comentários", placeholder="Observações")
        
        submitted = st.form_submit_button("➕ Adicionar Item", use_container_width=True, type="primary")
        
        if submitted and novo_item:
            with st.spinner("⏳ Adicionando ao Supabase..."):
                if add_item(novo_item, novo_servico, float(novo_preco), novo_status, novos_comentarios):
                    st.success(f"✅ Item '{novo_item}' adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar item. Tente novamente.")
    
    # Mostrar total
    total_atual = calcular_total_orcado(items_filtrados)
    st.markdown(f"### 💰 Total ({filtro_status}): {formatar_moeda(total_atual)}")


# ==================== SEÇÃO: PLANEJAMENTO FINANCEIRO ====================
elif menu_option == "💰 Planejamento Financeiro":
    st.header("💰 Planejamento Financeiro")
    
    st.markdown("### ⚙️ Configurações Financeiras")
    
    col1, col2 = st.columns(2)
    
    with col1:
        orcamento_maximo = st.number_input(
            "💵 Orçamento Máximo (R$)",
            min_value=0.0,
            value=config.get('orcamento_maximo', 30000.0),
            step=1000.0
        )
        
        taxa_juros = st.number_input(
            "💹 Taxa de Juros Mensal (%)",
            min_value=0.0,
            max_value=100.0,
            value=config.get('taxa_juros', 0.0035) * 100,
            step=0.01,
            format="%.2f",
            help="Taxa de juros mensal em % (ex: 0.35 para 0,35% ao mês)"
        )
    
    with col2:
        numero_meses = st.number_input(
            "📅 Número de Meses",
            min_value=1,
            value=int(config.get('numero_meses', 12)),
            step=1
        )
        
        valor_inicial = st.number_input(
            "💰 Valor Inicial Disponível (R$)",
            min_value=0.0,
            value=config.get('valor_inicial', 30000.0),
            step=1000.0
        )
    
    # Botão para salvar configurações
    if st.button("💾 Salvar Configurações", use_container_width=True, type="primary"):
        config_atualizada = {
            "orcamento_maximo": orcamento_maximo,
            "taxa_juros": taxa_juros / 100,
            "numero_meses": float(numero_meses),
            "valor_inicial": valor_inicial
        }
        
        with st.spinner("⏳ Salvando no Supabase..."):
            if update_all_config(config_atualizada):
                st.success("✅ Configurações salvas com sucesso no Supabase!")
                st.rerun()
            else:
                st.error("❌ Erro ao salvar configurações. Tente novamente.")
    
    st.markdown("---")
    st.markdown("### 📊 Análise Financeira")
    
    # Cálculos automáticos
    total_orcado = calcular_total_orcado(items)
    reserva = calcular_reserva(orcamento_maximo, total_orcado)
    porcentagem_usada = calcular_porcentagem_usada(orcamento_maximo, total_orcado)
    
    # Calcular investimento mensal necessário
    investimento_mensal = calcular_investimento_mensal(
        valor_inicial,
        orcamento_maximo,
        config.get('taxa_juros', 0.0035),
        int(config.get('numero_meses', 12))
    )
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💰 Total Orçado",
            formatar_moeda(total_orcado)
        )
        st.metric(
            "💵 Reserva Disponível",
            formatar_moeda(reserva)
        )
    
    with col2:
        st.metric(
            "📊 Porcentagem Utilizada",
            f"{porcentagem_usada:.2f}%"
        )
        st.metric(
            "💳 Valor Inicial",
            formatar_moeda(valor_inicial)
        )
    
    with col3:
        st.metric(
            "📈 Investimento Mensal Recomendado",
            formatar_moeda(investimento_mensal)
        )
        st.metric(
            "📅 Meses Restantes",
            f"{numero_meses} meses"
        )
    
    # Alertas
    if porcentagem_usada > 80:
        st.warning("⚠️ Atenção! Você já utilizou mais de 80% do orçamento!")
    
    if porcentagem_usada > 100:
        st.error("🚨 Alerta! Orçamento excedido!")
    
    # Gráfico de evolução do investimento
    st.markdown("### 📈 Projeção de Investimento")
    
    meses = list(range(numero_meses + 1))
    valores_acumulados = []
    
    for mes in meses:
        if mes == 0:
            valores_acumulados.append(valor_inicial)
        else:
            # Valor futuro com aportes mensais
            fator = (1 + config.get('taxa_juros', 0.0035)) ** mes
            valor_futuro_inicial = valor_inicial * fator
            
            if investimento_mensal > 0:
                valor_aportes = investimento_mensal * ((fator - 1) / config.get('taxa_juros', 0.0035))
            else:
                valor_aportes = 0
            
            valores_acumulados.append(valor_futuro_inicial + valor_aportes)
    
    df_projecao = pd.DataFrame({
        'Mês': meses,
        'Valor Acumulado': valores_acumulados
    })
    
    fig = px.line(
        df_projecao,
        x='Mês',
        y='Valor Acumulado',
        title='Projeção de Valor Acumulado ao Longo dos Meses',
        markers=True
    )
    
    # Adicionar linha do orçamento máximo
    fig.add_hline(
        y=orcamento_maximo,
        line_dash="dash",
        line_color="red",
        annotation_text="Orçamento Máximo"
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==================== SEÇÃO: CHECKLIST ====================
elif menu_option == "✅ Checklist":
    st.title("✅ Checklist de Tarefas")
    st.write("Organize e acompanhe todas as tarefas do seu casamento")
    
    # Adicionar nova tarefa
    with st.expander("➕ Adicionar Nova Tarefa"):
        with st.form("form_add_task"):
            nova_tarefa = st.text_input("Descrição da tarefa", placeholder="Ex: Escolher vestido de noiva")
            submitted = st.form_submit_button("➕ Adicionar Tarefa", use_container_width=True, type="primary")
            if submitted:
                if nova_tarefa:
                    with st.spinner("⏳ Adicionando ao Supabase..."):
                        result = add_task(nova_tarefa, False)
                        if result:
                            st.success("✅ Tarefa adicionada!")
                            st.rerun()
                else:
                    st.error("❌ Digite uma descrição para a tarefa!")
    
    # Listar tarefas
    if tasks:
        # Calcular progresso
        concluidas = sum(1 for t in tasks if t.get('concluida', False))
        total = len(tasks)
        porcentagem = (concluidas / total * 100) if total > 0 else 0
        
        # Métrica de progresso
        col1, col2 = st.columns([2, 1])
        with col1:
            st.metric(
                label="📊 Progresso Geral",
                value=f"{porcentagem:.0f}%",
                delta=f"{concluidas}/{total} tarefas concluídas"
            )
        with col2:
            st.metric(
                label="🎯 Faltam",
                value=f"{total - concluidas}",
                delta=f"tarefas"
            )
        
        st.progress(porcentagem / 100)
        
        st.divider()
        
        # Inicializar seleção no session_state
        if 'selected_task_id' not in st.session_state:
            st.session_state.selected_task_id = None
        if 'editing_task_mode' not in st.session_state:
            st.session_state.editing_task_mode = False
        
        # Filtro
        filtro_tarefa = st.selectbox(
            "Filtrar tarefas:",
            ["Todas", "Pendentes", "Concluídas"]
        )
        
        st.markdown("### 📋 Lista de Tarefas")
        
        # Listar tarefas (sem botões ao lado)
        for task in tasks:
            # Aplicar filtro
            if filtro_tarefa == "Pendentes" and task.get('concluida', False):
                continue
            if filtro_tarefa == "Concluídas" and not task.get('concluida', False):
                continue
            
            # Destacar tarefa selecionada
            is_selected = st.session_state.selected_task_id == task['id']
            
            col1, col2 = st.columns([0.5, 9.5])
            
            with col1:
                # Checkbox para marcar como concluída
                checked = st.checkbox(
                    "",
                    value=task.get('concluida', False),
                    key=f"check_{task['id']}",
                    label_visibility="collapsed"
                )
                if checked != task.get('concluida', False):
                    with st.spinner("⏳ Atualizando..."):
                        if update_task(task['id'], {"concluida": checked}):
                            st.rerun()
            
            with col2:
                # Texto da tarefa (clicável para selecionar)
                if is_selected:
                    # Destacar com background (usando markdown)
                    if task.get('concluida', False):
                        st.markdown(f"### 🔵 ~~{task['tarefa']}~~")
                    else:
                        st.markdown(f"### 🔵 {task['tarefa']}")
                else:
                    # Botão invisível para seleção
                    if task.get('concluida', False):
                        if st.button(f"~~{task['tarefa']}~~", key=f"select_{task['id']}", use_container_width=True):
                            st.session_state.selected_task_id = task['id']
                            st.session_state.editing_task_mode = False
                            st.rerun()
                    else:
                        if st.button(task['tarefa'], key=f"select_{task['id']}", use_container_width=True):
                            st.session_state.selected_task_id = task['id']
                            st.session_state.editing_task_mode = False
                            st.rerun()
        
        # Área de ação para tarefa selecionada
        if st.session_state.selected_task_id is not None:
            st.divider()
            
            selected_task = next((t for t in tasks if t['id'] == st.session_state.selected_task_id), None)
            
            if selected_task:
                if not st.session_state.editing_task_mode:
                    # Mostrar tarefa selecionada com botões de ação
                    st.info(f"📌 **Tarefa selecionada:** {selected_task['tarefa']}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Editar Tarefa", use_container_width=True, type="primary"):
                            st.session_state.editing_task_mode = True
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ Deletar Tarefa", use_container_width=True):
                            with st.spinner("⏳ Deletando..."):
                                if delete_task(selected_task['id']):
                                    st.session_state.selected_task_id = None
                                    st.session_state.editing_task_mode = False
                                    st.success("✅ Tarefa deletada!")
                                    st.rerun()
                    
                    with col3:
                        if st.button("❌ Cancelar Seleção", use_container_width=True):
                            st.session_state.selected_task_id = None
                            st.session_state.editing_task_mode = False
                            st.rerun()
                
                else:
                    # Modo de edição
                    st.warning(f"✏️ **Editando tarefa:** {selected_task['tarefa']}")
                    
                    with st.form("form_edit_selected_task"):
                        novo_texto = st.text_input("Novo nome da tarefa:", value=selected_task['tarefa'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("✅ Salvar Alteração", use_container_width=True, type="primary"):
                                if novo_texto:
                                    with st.spinner("⏳ Salvando..."):
                                        if update_task(selected_task['id'], {"tarefa": novo_texto}):
                                            st.session_state.editing_task_mode = False
                                            st.success("✅ Tarefa atualizada!")
                                            st.rerun()
                                else:
                                    st.error("❌ O nome da tarefa não pode estar vazio!")
                        with col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                st.session_state.editing_task_mode = False
                                st.rerun()
    else:
        st.info("📝 Nenhuma tarefa cadastrada ainda. Adicione tarefas acima para começar!")


# ==================== SEÇÃO: RELATÓRIOS ====================
elif menu_option == "📊 Relatórios":
    st.header("📊 Relatórios e Análises")
    
    # Calcular métricas
    total_orcado = calcular_total_orcado(items)
    orcamento_maximo = config.get('orcamento_maximo', 30000.0)
    
    # Gráfico de barras - Gastos por item
    st.markdown("### 📊 Gastos por Item")
    
    items_com_preco = [item for item in items if item['preco'] > 0]
    
    if items_com_preco:
        df_gastos = pd.DataFrame(items_com_preco)
        df_gastos = df_gastos.sort_values('preco', ascending=True)
        
        fig = px.bar(
            df_gastos,
            y='item',
            x='preco',
            orientation='h',
            title='Gastos por Item (R$)',
            labels={'preco': 'Preço (R$)', 'item': 'Item'},
            color='preco',
            color_continuous_scale='RdPu'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Adicione itens com preços para visualizar este gráfico.")
    
    # Gráfico de pizza - Distribuição percentual
    st.markdown("### 🥧 Distribuição Percentual dos Gastos")
    
    if items_com_preco:
        fig = px.pie(
            df_gastos,
            values='preco',
            names='item',
            title='Distribuição Percentual',
            color_discrete_sequence=px.colors.sequential.RdPu
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela resumo
    st.markdown("### 📋 Resumo: Itens Contratados vs Pendentes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Itens Contratados")
        itens_contratados = [item for item in items if item.get('status') == 'Contratado']
        
        if itens_contratados:
            df_contratados = pd.DataFrame(itens_contratados)
            df_display = df_contratados[['item', 'servico', 'preco']].copy()
            df_display.columns = ['Item', 'Serviço', 'Preço (R$)']
            st.dataframe(df_display, hide_index=True, use_container_width=True)
            st.markdown(f"**Total: {formatar_moeda(sum(item['preco'] for item in itens_contratados))}**")
        else:
            st.info("Nenhum item contratado ainda.")
    
    with col2:
        st.markdown("#### ⏳ Itens Pendentes")
        itens_pendentes = [item for item in items if item.get('status') == 'Pendente']
        
        if itens_pendentes:
            df_pendentes = pd.DataFrame(itens_pendentes)
            df_display = df_pendentes[['item', 'preco']].copy()
            df_display.columns = ['Item', 'Preço (R$)']
            st.dataframe(df_display, hide_index=True, use_container_width=True)
            st.markdown(f"**Total: {formatar_moeda(sum(item['preco'] for item in itens_pendentes))}**")
        else:
            st.success("Todos os itens foram contratados! 🎉")
    
    # Download dos dados
    st.markdown("---")
    st.markdown("### 💾 Download dos Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV de itens
        if items:
            df_items_download = pd.DataFrame(items)
            csv_items = df_items_download.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Itens (CSV)",
                data=csv_items,
                file_name="itens_casamento.csv",
                mime="text/csv"
            )
    
    with col2:
        # CSV de tarefas
        if tasks:
            df_tasks_download = pd.DataFrame(tasks)
            csv_tasks = df_tasks_download.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Download Tarefas (CSV)",
                data=csv_tasks,
                file_name="tarefas_casamento.csv",
                mime="text/csv"
            )
    
    with col3:
        # Resumo geral
        resumo_texto = f"""RESUMO FINANCEIRO DO CASAMENTO

Orçamento Máximo: {formatar_moeda(orcamento_maximo)}
Total Orçado: {formatar_moeda(total_orcado)}
Reserva Disponível: {formatar_moeda(orcamento_maximo - total_orcado)}
Porcentagem Utilizada: {calcular_porcentagem_usada(orcamento_maximo, total_orcado):.2f}%

Itens Contratados: {len([i for i in items if i.get('status') == 'Contratado'])}
Itens Pendentes: {len([i for i in items if i.get('status') == 'Pendente'])}

Tarefas Concluídas: {sum(1 for t in tasks if t.get('concluida', False))} de {len(tasks)}
Progresso: {calcular_porcentagem_tarefas(tasks):.1f}%
"""
        
        st.download_button(
            label="📥 Download Resumo (TXT)",
            data=resumo_texto,
            file_name="resumo_casamento.txt",
            mime="text/plain"
        )


# ==================== SEÇÃO: ORÇAMENTOS ====================
elif menu_option == "💸 Orçamentos":
    st.header("💸 Orçamentos")
    
    # Carregar dados
    categorias = get_all_categorias()
    orcamentos = get_all_orcamentos()
    
    # ===== SEÇÃO 1: GERENCIAR CATEGORIAS (colapsável) =====
    with st.expander("📁 Gerenciar Categorias"):
        st.write("**Categorias de serviços disponíveis**")
        
        # Adicionar categoria
        with st.form("form_add_categoria_inline"):
            col1, col2 = st.columns([3, 1])
            with col1:
                nova_categoria = st.text_input("Nova categoria", placeholder="Ex: Flores")
            with col2:
                submitted_cat = st.form_submit_button("➕ Adicionar", use_container_width=True)
            
            if submitted_cat and nova_categoria:
                result = add_categoria(nova_categoria)
                if result:
                    st.success(f"✅ Categoria '{nova_categoria}' adicionada!")
                    st.rerun()
        
        # Listar categorias
        if categorias:
            st.divider()
            df_cat = pd.DataFrame(categorias)
            
            # Remover created_at
            if 'created_at' in df_cat.columns:
                df_cat = df_cat.drop('created_at', axis=1)
            
            df_cat.columns = ['ID', 'Nome']
            
            st.dataframe(df_cat, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # ===== SEÇÃO 2: ORÇAMENTOS RECEBIDOS =====
    
    # Filtro por categoria
    col1, col2 = st.columns([3, 1])
    with col1:
        cat_options = ["Todas"] + [cat['nome'] for cat in categorias]
        filtro_cat = st.selectbox("Filtrar por categoria:", cat_options)
    
    # Aplicar filtro
    if filtro_cat == "Todas":
        orcamentos_filtrados = orcamentos
    else:
        orcamentos_filtrados = [
            orc for orc in orcamentos 
            if orc.get('categorias', {}).get('nome') == filtro_cat
        ]
    
    # Converter para DataFrame
    if orcamentos_filtrados:
        # Preparar dados para exibição
        orcamentos_display = []
        for orc in orcamentos_filtrados:
            orcamentos_display.append({
                'id': orc['id'],
                'categoria': orc['categorias']['nome'],
                'categoria_id': orc['categoria_id'],
                'fornecedor': orc['fornecedor'],
                'valor': float(orc['valor']),
                'telefone': orc.get('telefone', ''),
                'observacao': orc.get('observacao', '')
            })
        
        df_orcamentos = pd.DataFrame(orcamentos_display)
        
        # Preparar DataFrame para exibição (sem categoria_id)
        df_display = df_orcamentos[['id', 'categoria', 'fornecedor', 'valor', 'telefone', 'observacao']].copy()
        df_display.columns = ['ID', 'Categoria', 'Fornecedor', 'Valor', 'Telefone', 'Observação']
        
        # Criar mapeamento de categorias para SelectboxColumn
        categorias_dict = {cat['nome']: cat['id'] for cat in categorias}
        categorias_nomes = list(categorias_dict.keys())
        
        # Editor de dados (IGUAL Itens do Casamento)
        st.markdown("### 📝 Tabela de Orçamentos")
        edited_df = st.data_editor(
            df_display,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    disabled=True  # ID não editável
                ),
                "Categoria": st.column_config.SelectboxColumn(
                    "Categoria",
                    options=categorias_nomes,
                    required=True
                ),
                "Fornecedor": st.column_config.TextColumn(
                    "Fornecedor",
                    required=True
                ),
                "Valor": st.column_config.NumberColumn(
                    "Valor (R$)",
                    format="R$ %.2f",
                    min_value=0.0,
                    required=True
                ),
                "Telefone": st.column_config.TextColumn(
                    "Telefone"
                ),
                "Observação": st.column_config.TextColumn(
                    "Observação"
                )
            },
            hide_index=True
        )
        
        # Botão para salvar alterações (IGUAL Itens do Casamento)
        if st.button("💾 Salvar Alterações", use_container_width=True, type="primary"):
            # Converter de volta para formato original
            edited_df.columns = ['id', 'categoria', 'fornecedor', 'valor', 'telefone', 'observacao']
            
            # Converter nome de categoria para categoria_id
            orcamentos_atualizados = []
            for idx, row in edited_df.iterrows():
                categoria_nome = row['categoria']
                categoria_id = categorias_dict.get(categoria_nome)
                
                if categoria_id:
                    orcamentos_atualizados.append({
                        'id': int(row['id']),
                        'categoria_id': categoria_id,
                        'fornecedor': row['fornecedor'],
                        'valor': float(row['valor']),
                        'telefone': row['telefone'],
                        'observacao': row['observacao']
                    })
            
            # Salvar no Supabase
            with st.spinner("⏳ Salvando no Supabase..."):
                sucesso = True
                for orc in orcamentos_atualizados:
                    orc_id = orc.pop('id')
                    result = update_orcamento(orc_id, orc)
                    if not result:
                        sucesso = False
                        break
                
                if sucesso:
                    st.success("✅ Alterações salvas com sucesso no Supabase!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar alterações. Tente novamente.")
        
        # Mostrar totais
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            total_filtrado = df_display['Valor'].sum()
            st.metric("💰 Total (filtrado)", f"R$ {total_filtrado:,.2f}")
        
        with col2:
            qtd_orcamentos = len(df_display)
            st.metric("📊 Quantidade", f"{qtd_orcamentos} orçamento(s)")
    
    else:
        st.info("ℹ️ Nenhum orçamento cadastrado nesta categoria.")
    
    # ===== FORMULÁRIO ADICIONAR NOVO ORÇAMENTO (IGUAL Itens do Casamento) =====
    st.divider()
    st.markdown("### ➕ Adicionar Novo Orçamento")
    
    with st.form("novo_orcamento_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if categorias:
                nova_categoria = st.selectbox(
                    "Categoria *",
                    options=[cat['nome'] for cat in categorias]
                )
            else:
                st.warning("⚠️ Adicione categorias primeiro!")
                nova_categoria = None
        
        with col2:
            novo_fornecedor = st.text_input(
                "Fornecedor *",
                placeholder="Nome do fornecedor"
            )
        
        with col3:
            novo_valor = st.number_input(
                "Valor (R$) *",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )
        
        col4, col5 = st.columns(2)
        
        with col4:
            novo_telefone = st.text_input(
                "Telefone",
                placeholder="(11) 98765-4321"
            )
        
        with col5:
            nova_observacao = st.text_input(
                "Observação",
                placeholder="Detalhes adicionais"
            )
        
        submitted = st.form_submit_button("➕ Adicionar Orçamento", use_container_width=True, type="primary")
        
        if submitted:
            if nova_categoria and novo_fornecedor:
                # Obter categoria_id
                categoria_id = next(
                    (cat['id'] for cat in categorias if cat['nome'] == nova_categoria),
                    None
                )
                
                if categoria_id:
                    with st.spinner("⏳ Adicionando ao Supabase..."):
                        result = add_orcamento(
                            categoria_id=categoria_id,
                            fornecedor=novo_fornecedor,
                            valor=novo_valor,
                            telefone=novo_telefone,
                            observacao=nova_observacao
                        )
                        
                        if result:
                            st.success(f"✅ Orçamento de '{novo_fornecedor}' adicionado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao adicionar orçamento. Tente novamente.")
                else:
                    st.error("❌ Categoria inválida!")
            else:
                st.error("❌ Os campos 'Categoria' e 'Fornecedor' são obrigatórios!")
    
    # ===== TOTAIS POR CATEGORIA =====
    if orcamentos:
        st.divider()
        st.markdown("### 📊 Totais por Categoria")
        
        totais = {}
        for orc in orcamentos:
            cat_nome = orc['categorias']['nome']
            totais[cat_nome] = totais.get(cat_nome, 0) + float(orc['valor'])
        
        # Criar DataFrame para exibição
        df_totais = pd.DataFrame([
            {'Categoria': cat, 'Total': valor}
            for cat, valor in sorted(totais.items())
        ])
        
        st.dataframe(
            df_totais,
            column_config={
                "Total": st.column_config.NumberColumn(
                    "Total (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown(f"### 💰 **TOTAL GERAL: R$ {sum(totais.values()):,.2f}**")


# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "💕 Feito com amor para o planejamento do seu casamento dos sonhos! 💕"
    "</div>",
    unsafe_allow_html=True
)
