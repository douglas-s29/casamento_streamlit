"""
Módulo para gerenciamento de dados no Supabase
Fornece funções para CRUD de items, tasks e config
"""
import streamlit as st
from supabase import create_client, Client
from typing import List, Dict, Optional, Any


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


def update_task(task_id: int, concluida: bool) -> bool:
    """
    Atualiza o status de conclusão de uma tarefa
    
    Args:
        task_id: ID da tarefa
        concluida: Novo status de conclusão
        
    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = init_supabase()
        data = {"concluida": concluida}
        supabase.table('tasks').update(data).eq('id', task_id).execute()
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
