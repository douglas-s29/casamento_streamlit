"""
Script para executar SQL diretamente no Supabase usando a API REST
"""
import requests
import toml
from pathlib import Path

# Carregar secrets
secrets_path = Path(__file__).parent / '.streamlit' / 'secrets.toml'
secrets = toml.load(secrets_path)

url = secrets["supabase"]["url"]
key = secrets["supabase"]["key"]

# Ler o SQL do arquivo
with open('database_setup.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

print("=" * 80)
print("🎉 EXECUTANDO SQL NO SUPABASE")
print("=" * 80)
print()

# Tentar executar via PostgREST
# Nota: A API pública do Supabase não permite execução direta de SQL
# O SQL deve ser executado manualmente no SQL Editor

print("📋 INSTRUÇÕES PARA EXECUTAR NO SUPABASE:")
print("=" * 80)
print()
print("1. Acesse: https://app.supabase.com/project/jhpzpagkpwolwfbqezwi/sql")
print("2. Faça login se necessário")
print("3. Clique em 'New query'")
print("4. Copie o conteúdo do arquivo 'database_setup.sql'")
print("5. Cole no editor SQL")
print("6. Clique em 'Run' ou pressione Ctrl+Enter")
print()
print("=" * 80)
print()

# Tentar verificar se as tabelas já existem
print("🔍 Verificando se as tabelas já existem...")
print()

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# Verificar tabela items
try:
    response = requests.get(f"{url}/rest/v1/items?limit=1", headers=headers)
    if response.status_code == 200:
        print("✅ Tabela 'items' existe e está acessível")
        data = response.json()
        print(f"   Registros encontrados: {len(data)}")
    else:
        print(f"❌ Tabela 'items' não encontrada (código: {response.status_code})")
        print(f"   Mensagem: {response.text}")
except Exception as e:
    print(f"❌ Erro ao verificar tabela 'items': {e}")

print()

# Verificar tabela config
try:
    response = requests.get(f"{url}/rest/v1/config?limit=1", headers=headers)
    if response.status_code == 200:
        print("✅ Tabela 'config' existe e está acessível")
        data = response.json()
        print(f"   Registros encontrados: {len(data)}")
    else:
        print(f"❌ Tabela 'config' não encontrada (código: {response.status_code})")
        print(f"   Mensagem: {response.text}")
except Exception as e:
    print(f"❌ Erro ao verificar tabela 'config': {e}")

print()

# Verificar tabela tasks
try:
    response = requests.get(f"{url}/rest/v1/tasks?limit=1", headers=headers)
    if response.status_code == 200:
        print("✅ Tabela 'tasks' existe e está acessível")
        data = response.json()
        print(f"   Registros encontrados: {len(data)}")
    else:
        print(f"❌ Tabela 'tasks' não encontrada (código: {response.status_code})")
        print(f"   Mensagem: {response.text}")
except Exception as e:
    print(f"❌ Erro ao verificar tabela 'tasks': {e}")

print()
print("=" * 80)
print("💡 PRÓXIMOS PASSOS:")
print("=" * 80)
print()
print("Se as tabelas NÃO existem:")
print("  1. Execute o SQL manualmente conforme instruções acima")
print("  2. Execute este script novamente para verificar")
print()
print("Se as tabelas EXISTEM:")
print("  1. Execute: streamlit run app.py")
print("  2. Teste todas as funcionalidades")
print()
print("=" * 80)
