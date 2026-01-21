"""
Script de teste - Simula dados do Supabase para verificar a UI
Este script modifica temporariamente o supabase_client.py para retornar dados mock
"""

# Dados mock para testes
MOCK_ITEMS = [
    {"id": 1, "item": "Vestido de noiva", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
    {"id": 2, "item": "Cabelo e maquiagem", "servico": "", "preco": 0.0, "status": "Pendente", "comentarios": ""},
    {"id": 3, "item": "Igreja", "servico": "Igreja Bom Jesus", "preco": 800.0, "status": "Contratado", "comentarios": ""},
    {"id": 4, "item": "Espaço para a festa", "servico": "Chacara Da Maria", "preco": 1600.0, "status": "Contratado", "comentarios": ""},
    {"id": 5, "item": "Buffet", "servico": "Marquinhos", "preco": 8400.0, "status": "Contratado", "comentarios": ""},
    {"id": 6, "item": "Fotografia", "servico": "O grande dia - Sá Teles Fotografia", "preco": 1780.0, "status": "Contratado", "comentarios": ""}
]

MOCK_CONFIG = {
    'orcamento_maximo': 30000.0,
    'taxa_juros': 0.0035,
    'numero_meses': 12.0,
    'valor_inicial': 30000.0
}

MOCK_TASKS = [
    {"id": 1, "tarefa": "Definir data do casamento", "concluida": False},
    {"id": 2, "tarefa": "Escolher e reservar igreja", "concluida": True},
    {"id": 3, "tarefa": "Contratar espaço para festa", "concluida": True},
    {"id": 4, "tarefa": "Contratar buffet", "concluida": True},
    {"id": 5, "tarefa": "Contratar fotógrafo", "concluida": True},
    {"id": 6, "tarefa": "Escolher vestido de noiva", "concluida": False}
]

print("=" * 80)
print("🧪 MODO DE TESTE - DADOS MOCK")
print("=" * 80)
print()
print("Este script fornece dados simulados para testar a interface da aplicação")
print("sem necessidade de conexão com o Supabase.")
print()
print("📊 Dados Mock Disponíveis:")
print(f"  - Items: {len(MOCK_ITEMS)} itens")
print(f"  - Config: {len(MOCK_CONFIG)} configurações")
print(f"  - Tasks: {len(MOCK_TASKS)} tarefas")
print()
print("💡 Para usar dados mock:")
print("  1. Descomente as funções mock em utils/supabase_client.py")
print("  2. Execute: streamlit run app.py")
print()
print("⚠️  ATENÇÃO: Dados mock NÃO são persistidos!")
print()
print("=" * 80)
