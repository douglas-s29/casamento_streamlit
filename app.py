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

# Configuração da página
st.set_page_config(
    page_title="💍 Gerenciador de Casamento",
    page_icon="💍",
    layout="wide"
)

# CSS customizado para melhorar a aparência
st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

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


# ==================== SEÇÃO: DASHBOARD ====================
if menu_option == "🏠 Dashboard":
    st.header("🏠 Dashboard - Visão Geral")
    
    # Calcular métricas principais
    total_orcado = calcular_total_orcado(items)
    orcamento_maximo = config.get('orcamento_maximo', 30000.0)
    reserva = calcular_reserva(orcamento_maximo, total_orcado)
    porcentagem_usada = calcular_porcentagem_usada(orcamento_maximo, total_orcado)
    
    # Métricas em colunas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Orçamento Máximo",
            formatar_moeda(orcamento_maximo)
        )
    
    with col2:
        st.metric(
            "📊 Total Orçado",
            formatar_moeda(total_orcado),
            delta=f"{porcentagem_usada:.1f}% usado"
        )
    
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
            f"{porcentagem_tarefas:.0f}%"
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
        if st.button("💾 Salvar Alterações", type="primary"):
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
        
        submitted = st.form_submit_button("Adicionar Item", type="primary")
        
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
    if st.button("💾 Salvar Configurações", type="primary"):
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
    st.header("✅ Checklist de Tarefas")
    
    # Adicionar nova tarefa
    with st.expander("➕ Adicionar Nova Tarefa"):
        with st.form("form_add_task"):
            nova_tarefa = st.text_input("Descrição da tarefa")
            submitted = st.form_submit_button("Adicionar", type="primary")
            if submitted and nova_tarefa:
                with st.spinner("⏳ Adicionando ao Supabase..."):
                    result = add_task(nova_tarefa, False)
                    if result:
                        st.success("✅ Tarefa adicionada!")
                        st.rerun()
    
    # Calcular progresso
    total_tarefas = len(tasks)
    tarefas_concluidas = sum(1 for t in tasks if t.get('concluida', False))
    porcentagem = calcular_porcentagem_tarefas(tasks)
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📝 Total de Tarefas", total_tarefas)
    
    with col2:
        st.metric("✅ Concluídas", tarefas_concluidas)
    
    with col3:
        st.metric("⏳ Pendentes", total_tarefas - tarefas_concluidas)
    
    # Barra de progresso
    st.markdown(f"### 📊 Progresso Geral - {porcentagem:.0f}% Concluído")
    st.progress(porcentagem / 100)
    
    st.markdown("---")
    
    # Filtro
    filtro_tarefa = st.selectbox(
        "Filtrar tarefas:",
        ["Todas", "Pendentes", "Concluídas"]
    )
    
    # Lista de tarefas
    st.markdown("### 📋 Lista de Tarefas")
    
    if tasks:
        for task in tasks:
            # Aplicar filtro
            if filtro_tarefa == "Pendentes" and task.get('concluida', False):
                continue
            if filtro_tarefa == "Concluídas" and not task.get('concluida', False):
                continue
            
            col1, col2, col3, col4 = st.columns([1, 5, 1, 1])
            
            with col1:
                # Checkbox para marcar como concluída
                checked = st.checkbox("", value=task.get('concluida', False), 
                                    key=f"check_{task['id']}", 
                                    label_visibility="collapsed")
                if checked != task.get('concluida', False):
                    with st.spinner("⏳ Atualizando..."):
                        if update_task(task['id'], {"concluida": checked}):
                            st.rerun()
            
            with col2:
                if task.get('concluida', False):
                    st.write(f"~~{task['tarefa']}~~")  # Texto riscado
                else:
                    st.write(task['tarefa'])
            
            with col3:
                if st.button("✏️", key=f"edit_task_{task['id']}"):
                    st.session_state[f'editing_task_{task["id"]}'] = True
            
            with col4:
                if st.button("🗑️", key=f"del_task_{task['id']}"):
                    with st.spinner("⏳ Deletando..."):
                        if delete_task(task['id']):
                            st.success("Tarefa deletada!")
                            st.rerun()
            
            # Formulário de edição
            if st.session_state.get(f'editing_task_{task["id"]}'):
                with st.form(f"form_edit_task_{task['id']}"):
                    novo_texto = st.text_input("Editar tarefa", value=task['tarefa'])
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Salvar"):
                            with st.spinner("⏳ Salvando..."):
                                if update_task(task['id'], {"tarefa": novo_texto}):
                                    st.session_state[f'editing_task_{task["id"]}'] = False
                                    st.success("Tarefa atualizada!")
                                    st.rerun()
                    with col_cancel:
                        if st.form_submit_button("Cancelar"):
                            st.session_state[f'editing_task_{task["id"]}'] = False
                            st.rerun()
    else:
        st.info("Nenhuma tarefa cadastrada. Adicione a primeira tarefa acima!")


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
    st.title("💸 Orçamentos")
    st.write("Gerencie orçamentos recebidos organizados por categoria")
    
    # ====== SEÇÃO 1: GERENCIAR CATEGORIAS ======
    st.subheader("📁 Gerenciar Categorias")
    
    # Botão adicionar categoria
    with st.expander("➕ Adicionar Nova Categoria"):
        with st.form("form_add_categoria"):
            nova_categoria = st.text_input("Nome da Categoria")
            submitted = st.form_submit_button("Adicionar", type="primary")
            if submitted and nova_categoria:
                with st.spinner("⏳ Adicionando..."):
                    result = add_categoria(nova_categoria)
                    if result:
                        st.success(f"✅ Categoria '{nova_categoria}' adicionada!")
                        st.rerun()
    
    # Listar categorias
    categorias = get_all_categorias()
    if categorias:
        st.markdown("#### Categorias Cadastradas")
        
        # Cabeçalho
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.write("**ID**")
        with col2:
            st.write("**Nome**")
        with col3:
            st.write("**Ações**")
        with col4:
            st.write("")
        
        st.divider()
        
        for idx, row in enumerate(categorias):
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            
            with col1:
                st.write(row['id'])
            with col2:
                st.write(row['nome'])
            with col3:
                if st.button(f"✏️ Editar", key=f"edit_cat_{row['id']}"):
                    st.session_state[f'editing_cat_{row["id"]}'] = True
            with col4:
                if st.button(f"🗑️ Deletar", key=f"del_cat_{row['id']}"):
                    with st.spinner("⏳ Deletando..."):
                        if delete_categoria(row['id']):
                            st.success("Categoria deletada!")
                            st.rerun()
            
            # Formulário de edição (se ativado)
            if st.session_state.get(f'editing_cat_{row["id"]}'):
                with st.form(f"form_edit_cat_{row['id']}"):
                    novo_nome = st.text_input("Novo nome", value=row['nome'])
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Salvar"):
                            with st.spinner("⏳ Salvando..."):
                                if update_categoria(row['id'], novo_nome):
                                    st.session_state[f'editing_cat_{row["id"]}'] = False
                                    st.success("Categoria atualizada!")
                                    st.rerun()
                    with col_cancel:
                        if st.form_submit_button("Cancelar"):
                            st.session_state[f'editing_cat_{row["id"]}'] = False
                            st.rerun()
    else:
        st.info("Nenhuma categoria cadastrada. Adicione a primeira categoria acima!")
    
    st.divider()
    
    # ====== SEÇÃO 2: ORÇAMENTOS ======
    st.subheader("💰 Orçamentos Recebidos")
    
    # Filtro por categoria
    if categorias:
        cat_options = ["Todas"] + [cat['nome'] for cat in categorias]
        filtro_cat = st.selectbox("Filtrar por categoria:", cat_options)
    else:
        st.warning("⚠️ Cadastre categorias primeiro para adicionar orçamentos.")
        filtro_cat = "Todas"
    
    # Botão adicionar orçamento
    if categorias:
        with st.expander("➕ Adicionar Novo Orçamento"):
            with st.form("form_add_orcamento"):
                cat_selecionada = st.selectbox("Categoria", [cat['nome'] for cat in categorias])
                fornecedor = st.text_input("Fornecedor")
                valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
                telefone = st.text_input("Telefone")
                observacao = st.text_area("Observação")
                
                submitted = st.form_submit_button("Adicionar Orçamento", type="primary")
                if submitted and cat_selecionada and fornecedor:
                    with st.spinner("⏳ Adicionando..."):
                        cat_id = next(c['id'] for c in categorias if c['nome'] == cat_selecionada)
                        result = add_orcamento(cat_id, fornecedor, valor, telefone, observacao)
                        if result:
                            st.success("✅ Orçamento adicionado!")
                            st.rerun()
    
    # Listar orçamentos
    orcamentos = get_all_orcamentos()
    if orcamentos:
        # Filtrar se necessário
        orcamentos_filtrados = orcamentos
        if filtro_cat != "Todas":
            orcamentos_filtrados = [o for o in orcamentos if o['categorias']['nome'] == filtro_cat]
        
        # Exibir tabela
        if orcamentos_filtrados:
            st.markdown("#### Orçamentos Cadastrados")
            
            # Cabeçalho
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 3, 1, 1])
            with col1:
                st.write("**Categoria**")
            with col2:
                st.write("**Fornecedor**")
            with col3:
                st.write("**Valor**")
            with col4:
                st.write("**Telefone**")
            with col5:
                st.write("**Observação**")
            with col6:
                st.write("")
            with col7:
                st.write("")
            
            st.divider()
            
            for orc in orcamentos_filtrados:
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 3, 1, 1])
                
                with col1:
                    st.write(orc['categorias']['nome'])
                with col2:
                    st.write(orc['fornecedor'])
                with col3:
                    st.write(f"R$ {orc['valor']:,.2f}")
                with col4:
                    st.write(orc.get('telefone', ''))
                with col5:
                    st.write(orc.get('observacao', ''))
                with col6:
                    if st.button("✏️", key=f"edit_orc_{orc['id']}"):
                        st.session_state[f'editing_orc_{orc["id"]}'] = True
                with col7:
                    if st.button("🗑️", key=f"del_orc_{orc['id']}"):
                        with st.spinner("⏳ Deletando..."):
                            if delete_orcamento(orc['id']):
                                st.success("Orçamento deletado!")
                                st.rerun()
                
                # Formulário de edição
                if st.session_state.get(f'editing_orc_{orc["id"]}') and categorias:
                    with st.form(f"form_edit_orc_{orc['id']}"):
                        cat_edit = st.selectbox("Categoria", [cat['nome'] for cat in categorias], 
                                               index=[cat['nome'] for cat in categorias].index(orc['categorias']['nome']))
                        forn_edit = st.text_input("Fornecedor", value=orc['fornecedor'])
                        val_edit = st.number_input("Valor", value=float(orc['valor']), step=0.01, format="%.2f")
                        tel_edit = st.text_input("Telefone", value=orc.get('telefone', ''))
                        obs_edit = st.text_area("Observação", value=orc.get('observacao', ''))
                        
                        col_save, col_cancel = st.columns(2)
                        with col_save:
                            if st.form_submit_button("Salvar"):
                                with st.spinner("⏳ Salvando..."):
                                    cat_id = next(c['id'] for c in categorias if c['nome'] == cat_edit)
                                    data = {
                                        "categoria_id": cat_id,
                                        "fornecedor": forn_edit,
                                        "valor": val_edit,
                                        "telefone": tel_edit,
                                        "observacao": obs_edit
                                    }
                                    if update_orcamento(orc['id'], data):
                                        st.session_state[f'editing_orc_{orc["id"]}'] = False
                                        st.success("Orçamento atualizado!")
                                        st.rerun()
                        with col_cancel:
                            if st.form_submit_button("Cancelar"):
                                st.session_state[f'editing_orc_{orc["id"]}'] = False
                                st.rerun()
        else:
            st.info(f"Nenhum orçamento cadastrado para a categoria '{filtro_cat}'.")
        
        st.divider()
        
        # Totais por categoria
        st.subheader("📊 Totais por Categoria")
        totais = {}
        for orc in orcamentos:  # Pegar todos sem filtro
            cat_nome = orc['categorias']['nome']
            totais[cat_nome] = totais.get(cat_nome, 0) + float(orc['valor'])
        
        # Exibir em colunas
        if totais:
            for cat, total in sorted(totais.items()):
                st.write(f"**{cat}:** R$ {total:,.2f}")
            
            st.write("─" * 40)
            st.write(f"**TOTAL GERAL:** R$ {sum(totais.values()):,.2f}")
    else:
        st.info("Nenhum orçamento cadastrado. Adicione o primeiro orçamento acima!")


# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "💕 Feito com amor para o planejamento do seu casamento dos sonhos! 💕"
    "</div>",
    unsafe_allow_html=True
)
