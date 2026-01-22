"""
Módulo para gerenciamento de dados no Supabase
Fornece funções para CRUD de items, tasks e config
"""
import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Optional, Any, Union


def init_supabase() -> Client:
    """
    Inicializa e retorna o cliente Supabase
    
    Returns:
        Cliente Supabase autenticado
    """
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Supabase: {e}")
        raise


# ==================== OPERAÇÕES DE ITEMS ====================

@st.cache_data(ttl=10)
def get_all_items() -> List[Dict[str, Any]]:
    """
    Busca todos os itens do casamento do Supabase
    
    Returns:
        Lista de itens
    """
    try:
        supabase = init_supabase()
        response = supabase.table('items').select('*').order('id').execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar itens: {e}")
        return []


def add_item(item: str, servico: str = "", preco: float = 0.0, 
             status: str = "Pendente", comentarios: str = "") -> bool:
    """
    Adiciona um novo item ao Supabase
    
    Args:
        item: Nome do item
        servico: Nome do serviço/fornecedor
        preco: Preço do item
        status: Status (Pendente/Contratado)
        comentarios: Comentários adicionais
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        data = {
            "item": item,
            "servico": servico,
            "preco": preco,
            "status": status,
            "comentarios": comentarios
        }
        supabase.table('items').insert(data).execute()
        get_all_items.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao adicionar item: {e}")
        return False


def update_item(item_id: int, data: Dict[str, Any]) -> bool:
    """
    Atualiza um item existente no Supabase
    
    Args:
        item_id: ID do item
        data: Dicionário com os campos a serem atualizados
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        supabase.table('items').update(data).eq('id', item_id).execute()
        get_all_items.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar item: {e}")
        return False


def delete_item(item_id: int) -> bool:
    """
    Deleta um item do Supabase
    
    Args:
        item_id: ID do item a ser deletado
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        supabase.table('items').delete().eq('id', item_id).execute()
        get_all_items.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao deletar item: {e}")
        return False


def update_all_items(items: List[Dict[str, Any]]) -> bool:
    """
    Atualiza múltiplos itens de uma vez (usado para edição em massa)
    
    Args:
        items: Lista de itens com seus dados atualizados
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        for item in items:
            item_id = item.get('id')
            if item_id:
                # Remove o ID antes de atualizar
                item_data = {k: v for k, v in item.items() if k != 'id'}
                supabase.table('items').update(item_data).eq('id', item_id).execute()
        get_all_items.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar itens: {e}")
        return False


# ==================== OPERAÇÕES DE TASKS ====================

@st.cache_data(ttl=10)
def get_all_tasks() -> List[Dict[str, Any]]:
    """
    Busca todas as tarefas do Supabase
    
    Returns:
        Lista de tarefas
    """
    try:
        supabase = init_supabase()
        response = supabase.table('tasks').select('*').order('id').execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar tarefas: {e}")
        return []


def add_task(tarefa: str, concluida: bool = False) -> bool:
    """
    Adiciona uma nova tarefa ao Supabase
    
    Args:
        tarefa: Descrição da tarefa
        concluida: Se a tarefa está concluída
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        data = {
            "tarefa": tarefa,
            "concluida": concluida
        }
        supabase.table('tasks').insert(data).execute()
        get_all_tasks.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao adicionar tarefa: {e}")
        return False


def update_task(task_id: int, data: Union[bool, Dict[str, Any]]) -> bool:
    """
    Atualiza uma tarefa (status de conclusão e/ou nome)
    
    Args:
        task_id: ID da tarefa
        data: Dicionário com campos a atualizar ou bool para concluida (compatibilidade)
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        # Compatibilidade com chamadas antigas passando bool
        if isinstance(data, bool):
            update_data = {"concluida": data}
        else:
            update_data = data
        supabase.table('tasks').update(update_data).eq('id', task_id).execute()
        get_all_tasks.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar tarefa: {e}")
        return False


def delete_task(task_id: int) -> bool:
    """
    Deleta uma tarefa do Supabase
    
    Args:
        task_id: ID da tarefa a ser deletada
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        supabase.table('tasks').delete().eq('id', task_id).execute()
        get_all_tasks.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao deletar tarefa: {e}")
        return False


# ==================== OPERAÇÕES DE CONFIG ====================

@st.cache_data(ttl=10)
def get_config() -> Dict[str, float]:
    """
    Busca as configurações financeiras do Supabase
    
    Returns:
        Dicionário com as configurações
    """
    try:
        supabase = init_supabase()
        response = supabase.table('config').select('*').execute()
        
        # Converter lista de chave-valor para dicionário
        config = {}
        if response.data:
            for row in response.data:
                config[row['chave']] = float(row['valor'])
        
        # Garantir que todas as chaves existam
        default_config = {
            'orcamento_maximo': 30000.0,
            'taxa_juros': 0.0035,
            'numero_meses': 12.0,
            'valor_inicial': 30000.0
        }
        
        for key, default_value in default_config.items():
            if key not in config:
                config[key] = default_value
        
        return config
    except Exception as e:
        st.error(f"❌ Erro ao buscar configurações: {e}")
        # Retornar configurações padrão em caso de erro
        return {
            'orcamento_maximo': 30000.0,
            'taxa_juros': 0.0035,
            'numero_meses': 12.0,
            'valor_inicial': 30000.0
        }


def update_config(chave: str, valor: float) -> bool:
    """
    Atualiza uma configuração financeira no Supabase
    
    Args:
        chave: Nome da configuração
        valor: Novo valor
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        
        # Verificar se a chave já existe
        response = supabase.table('config').select('*').eq('chave', chave).execute()
        
        if response.data:
            # Atualizar
            supabase.table('config').update({'valor': valor}).eq('chave', chave).execute()
        else:
            # Inserir
            supabase.table('config').insert({'chave': chave, 'valor': valor}).execute()
        
        get_config.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar configuração: {e}")
        return False


def update_all_config(config_dict: Dict[str, float]) -> bool:
    """
    Atualiza todas as configurações financeiras de uma vez
    
    Args:
        config_dict: Dicionário com todas as configurações
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        for chave, valor in config_dict.items():
            if not update_config(chave, valor):
                return False
        return True
    except Exception as e:
        st.error(f"❌ Erro ao atualizar configurações: {e}")
        return False


# ==================== OPERAÇÕES DE CATEGORIAS ====================

@st.cache_data(ttl=10)
def get_all_categorias() -> List[Dict[str, Any]]:
    """
    Busca todas as categorias
    
    Returns:
        Lista de categorias
    """
    try:
        supabase = init_supabase()
        response = supabase.table('categorias').select('*').order('nome').execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar categorias: {e}")
        return []


def add_categoria(nome: str) -> Optional[List[Dict[str, Any]]]:
    """
    Adiciona nova categoria
    
    Args:
        nome: Nome da categoria
        
    Returns:
        Dados da categoria criada ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        data = {"nome": nome}
        response = supabase.table('categorias').insert(data).execute()
        get_all_categorias.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao adicionar categoria: {e}")
        return None


def update_categoria(id: int, nome: str) -> Optional[List[Dict[str, Any]]]:
    """
    Atualiza categoria existente
    
    Args:
        id: ID da categoria
        nome: Novo nome
        
    Returns:
        Dados da categoria atualizada ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        data = {"nome": nome}
        response = supabase.table('categorias').update(data).eq('id', id).execute()
        get_all_categorias.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao atualizar categoria: {e}")
        return None


def delete_categoria(id: int) -> Optional[List[Dict[str, Any]]]:
    """
    Deleta categoria (e todos orçamentos relacionados via CASCADE)
    
    Args:
        id: ID da categoria
        
    Returns:
        Dados da categoria deletada ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        response = supabase.table('categorias').delete().eq('id', id).execute()
        get_all_categorias.clear()  # Limpa o cache
        get_all_orcamentos.clear()  # Limpa cache de orçamentos também
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao deletar categoria: {e}")
        return None


# ==================== OPERAÇÕES DE ORÇAMENTOS ====================

@st.cache_data(ttl=10)
def get_all_orcamentos() -> List[Dict[str, Any]]:
    """
    Busca todos orçamentos com informação de categoria
    
    Returns:
        Lista de orçamentos
    """
    try:
        supabase = init_supabase()
        response = supabase.table('orcamentos').select('*, categorias(nome)').execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar orçamentos: {e}")
        return []


def add_orcamento(categoria_id: int, fornecedor: str, valor: float, 
                  telefone: str = "", observacao: str = "") -> Optional[List[Dict[str, Any]]]:
    """
    Adiciona novo orçamento
    
    Args:
        categoria_id: ID da categoria
        fornecedor: Nome do fornecedor
        valor: Valor do orçamento
        telefone: Telefone de contato
        observacao: Observações
        
    Returns:
        Dados do orçamento criado ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        data = {
            "categoria_id": categoria_id,
            "fornecedor": fornecedor,
            "valor": valor,
            "telefone": telefone,
            "observacao": observacao
        }
        response = supabase.table('orcamentos').insert(data).execute()
        get_all_orcamentos.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao adicionar orçamento: {e}")
        return None


def update_orcamento(id: int, data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Atualiza orçamento existente
    
    Args:
        id: ID do orçamento
        data: Dicionário com campos a atualizar
        
    Returns:
        Dados do orçamento atualizado ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        response = supabase.table('orcamentos').update(data).eq('id', id).execute()
        get_all_orcamentos.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao atualizar orçamento: {e}")
        return None


def delete_orcamento(id: int) -> Optional[List[Dict[str, Any]]]:
    """
    Deleta orçamento
    
    Args:
        id: ID do orçamento
        
    Returns:
        Dados do orçamento deletado ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        response = supabase.table('orcamentos').delete().eq('id', id).execute()
        get_all_orcamentos.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao deletar orçamento: {e}")
        return None


# ==================== OPERAÇÕES DE AGENDAMENTOS ====================

@st.cache_data(ttl=10)
def get_all_agendamentos() -> List[Dict[str, Any]]:
    """
    Retorna todos os agendamentos
    
    Returns:
        Lista de agendamentos ordenados por data e hora
    """
    try:
        supabase = init_supabase()
        response = supabase.table("agendamentos").select("*").order("data", desc=False).order("hora", desc=False).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar agendamentos: {e}")
        return []


def get_agendamentos_by_data(data: str) -> List[Dict[str, Any]]:
    """
    Retorna agendamentos de uma data específica
    
    Args:
        data: Data no formato YYYY-MM-DD
        
    Returns:
        Lista de agendamentos da data especificada
    """
    try:
        supabase = init_supabase()
        response = supabase.table("agendamentos").select("*").eq("data", data).order("hora", desc=False).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar agendamentos: {e}")
        return []


def get_proximos_agendamentos(dias: int = 7) -> List[Dict[str, Any]]:
    """
    Retorna agendamentos dos próximos X dias
    
    Args:
        dias: Número de dias para buscar agendamentos futuros
        
    Returns:
        Lista de agendamentos dos próximos dias
    """
    try:
        from datetime import datetime, timedelta
        hoje = datetime.now().date()
        data_limite = hoje + timedelta(days=dias)
        
        supabase = init_supabase()
        response = supabase.table("agendamentos").select("*").gte("data", str(hoje)).lte("data", str(data_limite)).order("data", desc=False).order("hora", desc=False).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ Erro ao buscar próximos agendamentos: {e}")
        return []


def add_agendamento(data: str, hora: str, categoria: str, local: str, 
                   endereco: str = "", telefone: str = "", contato: str = "", 
                   observacao: str = "", status: str = "⏳ Agendado", 
                   link: str = "", cor: str = "#FF69B4") -> Optional[List[Dict[str, Any]]]:
    """
    Adiciona novo agendamento
    
    Args:
        data: Data no formato YYYY-MM-DD
        hora: Hora no formato HH:MM:SS
        categoria: Categoria do agendamento
        local: Local/fornecedor
        endereco: Endereço completo
        telefone: Telefone de contato
        contato: Nome do contato
        observacao: Observações adicionais
        status: Status do agendamento
        link: Link para Google Maps ou site
        cor: Cor para exibir no calendário
        
    Returns:
        Dados do agendamento criado ou None em caso de erro
    """
    try:
        # Validar dados antes de inserir
        if not data or not hora or not categoria or not local:
            st.error("❌ Campos obrigatórios faltando")
            return None
        
        supabase = init_supabase()
        agend_data = {
            "data": str(data),
            "hora": str(hora),
            "categoria": categoria,
            "local": local,
            "endereco": endereco,
            "telefone": telefone,
            "contato": contato,
            "observacao": observacao,
            "status": status,
            "link": link,
            "cor": cor
        }
        response = supabase.table("agendamentos").insert(agend_data).execute()
        get_all_agendamentos.clear()  # Limpa o cache
        
        if response.data:
            return response.data
        else:
            st.error("❌ Nenhum dado retornado do Supabase")
            return None
            
    except Exception as e:
        st.error(f"❌ Erro ao adicionar agendamento: {str(e)}")
        # Log detalhado para debug
        import traceback
        st.write("Traceback completo:")
        st.code(traceback.format_exc())
        return None


def update_agendamento(id: int, data: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Atualiza agendamento existente
    
    Args:
        id: ID do agendamento
        data: Dicionário com campos a atualizar
        
    Returns:
        Dados do agendamento atualizado ou None em caso de erro
    """
    try:
        supabase = init_supabase()
        response = supabase.table("agendamentos").update(data).eq("id", id).execute()
        get_all_agendamentos.clear()  # Limpa o cache
        return response.data
    except Exception as e:
        st.error(f"❌ Erro ao atualizar agendamento: {e}")
        return None


def delete_agendamento(id: int) -> bool:
    """
    Deleta agendamento
    
    Args:
        id: ID do agendamento
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        supabase.table("agendamentos").delete().eq("id", id).execute()
        get_all_agendamentos.clear()  # Limpa o cache
        return True
    except Exception as e:
        st.error(f"❌ Erro ao deletar agendamento: {e}")
        return False
