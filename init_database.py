"""
Script para inicializar o banco de dados Supabase
Cria as tabelas e insere dados iniciais
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar utils
sys.path.insert(0, str(Path(__file__).parent))

try:
    import streamlit as st
    from utils.supabase_client import init_supabase
    
    # Configurar secrets manualmente para execução standalone
    if not hasattr(st, 'secrets') or 'supabase' not in st.secrets:
        # Tentar carregar do arquivo secrets.toml
        import toml
        secrets_path = Path(__file__).parent / '.streamlit' / 'secrets.toml'
        if secrets_path.exists():
            secrets = toml.load(secrets_path)
            st.secrets.update(secrets)
except Exception as e:
    print(f"Erro ao importar: {e}")
    print("Certifique-se de ter instalado as dependências: pip install -r requirements.txt")
    sys.exit(1)


def create_tables():
    """Cria as tabelas no Supabase (se não existirem)"""
    print("📋 Criando tabelas no Supabase...")
    
    supabase = init_supabase()
    
    # Nota: As tabelas precisam ser criadas através do SQL Editor do Supabase
    # Este script apenas verifica se existem e insere dados
    
    print("ℹ️  As tabelas devem ser criadas manualmente no Supabase SQL Editor.")
    print("ℹ️  Use os seguintes comandos SQL:")
    print()
    print("-- Tabela items")
    print("""
CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  item TEXT NOT NULL,
  servico TEXT DEFAULT '',
  preco DECIMAL(10,2) DEFAULT 0.00,
  status TEXT DEFAULT 'Pendente',
  comentarios TEXT DEFAULT '',
  created_at TIMESTAMP DEFAULT NOW()
);
    """)
    
    print("-- Tabela config")
    print("""
CREATE TABLE IF NOT EXISTS config (
  id SERIAL PRIMARY KEY,
  chave TEXT UNIQUE NOT NULL,
  valor DECIMAL(10,2) NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW()
);
    """)
    
    print("-- Tabela tasks")
    print("""
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  tarefa TEXT NOT NULL,
  concluida BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);
    """)


def insert_initial_data():
    """Insere dados iniciais nas tabelas"""
    print("\n📝 Inserindo dados iniciais...")
    
    supabase = init_supabase()
    
    # Verificar se já existem dados
    try:
        items_response = supabase.table('items').select('id').limit(1).execute()
        if items_response.data:
            print("⚠️  Tabela 'items' já contém dados. Pulando inserção de items.")
        else:
            # Inserir items iniciais
            items_data = [
                {"item": "Vestido de noiva", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Cabelo e maquiagem", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Roupa do noivo", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Igreja", "servico": "Igreja Bom Jesus", "preco": 800.00, "status": "Contratado", "comentarios": ""},
                {"item": "Espaço para a festa", "servico": "Chacara Da Maria", "preco": 1600.00, "status": "Contratado", "comentarios": ""},
                {"item": "Decoração (flores e móveis)", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Buffet", "servico": "Marquinhos", "preco": 8400.00, "status": "Contratado", "comentarios": ""},
                {"item": "Doces e bolos", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Fotografia", "servico": "O grande dia - Sá Teles Fotografia", "preco": 1780.00, "status": "Contratado", "comentarios": ""},
                {"item": "DJ", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": "Verificando necessidade"},
                {"item": "Noite de núpcias", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Site dos noivos", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Documentos do cartório", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""},
                {"item": "Enfeites pista de dança", "servico": "", "preco": 0.00, "status": "Pendente", "comentarios": ""}
            ]
            
            supabase.table('items').insert(items_data).execute()
            print(f"✅ Inseridos {len(items_data)} itens iniciais.")
    except Exception as e:
        print(f"❌ Erro ao inserir items: {e}")
    
    # Config
    try:
        config_response = supabase.table('config').select('chave').limit(1).execute()
        if config_response.data:
            print("⚠️  Tabela 'config' já contém dados. Pulando inserção de config.")
        else:
            config_data = [
                {"chave": "orcamento_maximo", "valor": 30000.00},
                {"chave": "taxa_juros", "valor": 0.0035},
                {"chave": "numero_meses", "valor": 12},
                {"chave": "valor_inicial", "valor": 30000.00}
            ]
            
            supabase.table('config').insert(config_data).execute()
            print(f"✅ Inseridas {len(config_data)} configurações iniciais.")
    except Exception as e:
        print(f"❌ Erro ao inserir config: {e}")
    
    # Tasks
    try:
        tasks_response = supabase.table('tasks').select('id').limit(1).execute()
        if tasks_response.data:
            print("⚠️  Tabela 'tasks' já contém dados. Pulando inserção de tasks.")
        else:
            tasks_data = [
                {"tarefa": "Definir data do casamento", "concluida": False},
                {"tarefa": "Escolher e reservar igreja", "concluida": True},
                {"tarefa": "Contratar espaço para festa", "concluida": True},
                {"tarefa": "Contratar buffet", "concluida": True},
                {"tarefa": "Contratar fotógrafo", "concluida": True},
                {"tarefa": "Escolher vestido de noiva", "concluida": False},
                {"tarefa": "Escolher roupa do noivo", "concluida": False},
                {"tarefa": "Contratar decoração", "concluida": False},
                {"tarefa": "Escolher doces e bolo", "concluida": False},
                {"tarefa": "Decidir sobre DJ/música", "concluida": False},
                {"tarefa": "Fazer lista de convidados", "concluida": False},
                {"tarefa": "Escolher padrinhos e madrinhas", "concluida": False},
                {"tarefa": "Criar convites", "concluida": False},
                {"tarefa": "Enviar convites", "concluida": False},
                {"tarefa": "Definir cardápio", "concluida": False},
                {"tarefa": "Escolher alianças", "concluida": False},
                {"tarefa": "Reservar lua de mel", "concluida": False},
                {"tarefa": "Providenciar documentos do cartório", "concluida": False},
                {"tarefa": "Fazer lista de presentes", "concluida": False},
                {"tarefa": "Contratar maquiagem e cabelo", "concluida": False},
                {"tarefa": "Definir playlist da festa", "concluida": False},
                {"tarefa": "Fazer prova do vestido", "concluida": False},
                {"tarefa": "Confirmar presença dos convidados", "concluida": False},
                {"tarefa": "Organizar transporte", "concluida": False},
                {"tarefa": "Preparar cronograma do dia", "concluida": False}
            ]
            
            supabase.table('tasks').insert(tasks_data).execute()
            print(f"✅ Inseridas {len(tasks_data)} tarefas iniciais.")
    except Exception as e:
        print(f"❌ Erro ao inserir tasks: {e}")


def main():
    """Função principal"""
    print("=" * 60)
    print("🎉 Inicializador do Banco de Dados - Casamento Streamlit")
    print("=" * 60)
    print()
    
    try:
        create_tables()
        insert_initial_data()
        
        print()
        print("=" * 60)
        print("✅ Processo concluído com sucesso!")
        print("=" * 60)
        print()
        print("📝 Próximos passos:")
        print("1. Verifique se as tabelas foram criadas no Supabase")
        print("2. Execute a aplicação: streamlit run app.py")
        print()
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Erro durante a inicialização: {e}")
        print("=" * 60)
        print()
        print("🔧 Solução de problemas:")
        print("1. Verifique se o arquivo .streamlit/secrets.toml existe")
        print("2. Confirme que as credenciais do Supabase estão corretas")
        print("3. Crie as tabelas manualmente no Supabase SQL Editor")
        print()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
