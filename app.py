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
    get_config, update_config, update_all_config
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
     "✅ Checklist", "📊 Relatórios"]
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
    
    # Alertas
    if porcentagem_usada > 80:
        st.warning("⚠️ Atenção! Você já utilizou mais de 80% do orçamento!")
    elif porcentagem_usada > 90:
        st.error("🚨 Cuidado! Orçamento quase esgotado!")
    
    # Barra de progresso do orçamento
    st.markdown("### 📈 Progresso do Orçamento")
    st.progress(min(porcentagem_usada / 100, 1.0))
    st.caption(f"Utilizado: {formatar_moeda(total_orcado)} de {formatar_moeda(orcamento_maximo)}")
    
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
            "📈 Taxa de Juros Mensal (%)",
            min_value=0.0,
            value=config.get('taxa_juros', 0.0035) * 100,
            step=0.01,
            format="%.2f"
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
    
    # Filtro
    filtro_tarefa = st.selectbox(
        "Filtrar tarefas:",
        ["Todas", "Pendentes", "Concluídas"]
    )
    
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
    st.markdown("### 📊 Progresso Geral")
    st.progress(porcentagem / 100)
    st.caption(f"{porcentagem:.1f}% concluído")
    
    st.markdown("---")
    
    # Lista de tarefas
    st.markdown("### 📋 Lista de Tarefas")
    
    # Aplicar filtro
    if filtro_tarefa == "Pendentes":
        tasks_filtradas = [t for t in tasks if not t.get('concluida', False)]
    elif filtro_tarefa == "Concluídas":
        tasks_filtradas = [t for t in tasks if t.get('concluida', False)]
    else:
        tasks_filtradas = tasks
    
    # Exibir tarefas com checkboxes
    for i, task in enumerate(tasks):
        # Verificar se a tarefa está no filtro
        if filtro_tarefa == "Pendentes" and task.get('concluida', False):
            continue
        if filtro_tarefa == "Concluídas" and not task.get('concluida', False):
            continue
        
        col1, col2 = st.columns([0.1, 0.9])
        
        with col1:
            # Checkbox para marcar como concluída
            concluida_atual = task.get('concluida', False)
            concluida_nova = st.checkbox(
                "✓",
                value=concluida_atual,
                key=f"task_{task['id']}",
                label_visibility="collapsed"
            )
            
            # Atualizar se mudou
            if concluida_nova != concluida_atual:
                with st.spinner("⏳ Atualizando no Supabase..."):
                    if update_task(task['id'], concluida_nova):
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar tarefa.")
        
        with col2:
            # Exibir tarefa
            if task.get('concluida', False):
                st.markdown(f"~~{task['tarefa']}~~")
            else:
                st.markdown(f"**{task['tarefa']}**")
    
    st.markdown("---")
    
    # Formulário para adicionar nova tarefa
    st.markdown("### ➕ Adicionar Nova Tarefa")
    
    with st.form("nova_tarefa_form"):
        nova_tarefa = st.text_input("Descrição da tarefa *")
        submitted = st.form_submit_button("Adicionar Tarefa", type="primary")
        
        if submitted and nova_tarefa:
            with st.spinner("⏳ Adicionando ao Supabase..."):
                if add_task(nova_tarefa, False):
                    st.success(f"✅ Tarefa '{nova_tarefa}' adicionada!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar tarefa. Tente novamente.")


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

# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "💕 Feito com amor para o planejamento do seu casamento dos sonhos! 💕"
    "</div>",
    unsafe_allow_html=True
)
