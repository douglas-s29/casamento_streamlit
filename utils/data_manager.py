"""
Módulo para gerenciamento de dados em arquivos JSON
"""
import json
import os
from pathlib import Path

# Diretório base para armazenamento de dados
DATA_DIR = Path(__file__).parent.parent / "data"


def ensure_data_dir():
    """Cria o diretório data/ se não existir"""
    DATA_DIR.mkdir(exist_ok=True)


def load_json(filename, default_data):
    """
    Carrega dados de um arquivo JSON
    
    Args:
        filename: Nome do arquivo JSON
        default_data: Dados padrão caso o arquivo não exista
        
    Returns:
        Dados carregados ou dados padrão
    """
    ensure_data_dir()
    filepath = DATA_DIR / filename
    
    try:
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Criar arquivo com dados padrão
            save_json(filename, default_data)
            return default_data
    except Exception as e:
        print(f"Erro ao carregar {filename}: {e}")
        return default_data


def save_json(filename, data):
    """
    Salva dados em um arquivo JSON
    
    Args:
        filename: Nome do arquivo JSON
        data: Dados a serem salvos
    """
    ensure_data_dir()
    filepath = DATA_DIR / filename
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar {filename}: {e}")


def get_default_items():
    """Retorna a lista padrão de itens do casamento"""
    return [
        {"id": 1, "item": "Vestido de noiva", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 2, "item": "Cabelo e maquiagem", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 3, "item": "Roupa do noivo", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 4, "item": "Igreja", "servico": "Igreja Bom Jesus", "preco": 800.0, "status": "Contratado", "comentarios": ""},
        {"id": 5, "item": "Espaço para a festa", "servico": "Chacara Da Maria", "preco": 1600.0, "status": "Contratado", "comentarios": ""},
        {"id": 6, "item": "Decoração (flores e móveis)", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 7, "item": "Buffet", "servico": "Marquinhos", "preco": 8400.0, "status": "Contratado", "comentarios": ""},
        {"id": 8, "item": "Doces e bolos", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 9, "item": "Fotografia", "servico": "O grande dia - Sá Teles Fotografia", "preco": 1780.0, "status": "Contratado", "comentarios": ""},
        {"id": 10, "item": "DJ", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": "Verificando necessidade"},
        {"id": 11, "item": "Noite de núpcias", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 12, "item": "Site dos noivos", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 13, "item": "Documentos do cartório", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
        {"id": 14, "item": "Enfeites pista de dança", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""}
    ]


def get_default_config():
    """Retorna a configuração financeira padrão"""
    return {
        "orcamento_maximo": 30000.0,
        "taxa_juros": 0.0035,
        "numero_meses": 12,
        "valor_inicial": 30000.0
    }


def get_default_tasks():
    """Retorna a lista padrão de tarefas"""
    return [
        {"id": 1, "tarefa": "Definir data do casamento", "concluida": False},
        {"id": 2, "tarefa": "Escolher e reservar igreja", "concluida": True},
        {"id": 3, "tarefa": "Contratar espaço para festa", "concluida": True},
        {"id": 4, "tarefa": "Contratar buffet", "concluida": True},
        {"id": 5, "tarefa": "Contratar fotógrafo", "concluida": True},
        {"id": 6, "tarefa": "Escolher vestido de noiva", "concluida": False},
        {"id": 7, "tarefa": "Escolher roupa do noivo", "concluida": False},
        {"id": 8, "tarefa": "Contratar decoração", "concluida": False},
        {"id": 9, "tarefa": "Escolher doces e bolo", "concluida": False},
        {"id": 10, "tarefa": "Decidir sobre DJ/música", "concluida": False},
        {"id": 11, "tarefa": "Fazer lista de convidados", "concluida": False},
        {"id": 12, "tarefa": "Escolher padrinhos e madrinhas", "concluida": False},
        {"id": 13, "tarefa": "Criar convites", "concluida": False},
        {"id": 14, "tarefa": "Enviar convites", "concluida": False},
        {"id": 15, "tarefa": "Definir cardápio", "concluida": False},
        {"id": 16, "tarefa": "Escolher alianças", "concluida": False},
        {"id": 17, "tarefa": "Reservar lua de mel", "concluida": False},
        {"id": 18, "tarefa": "Providenciar documentos do cartório", "concluida": False},
        {"id": 19, "tarefa": "Fazer lista de presentes", "concluida": False},
        {"id": 20, "tarefa": "Contratar maquiagem e cabelo", "concluida": False}
    ]
