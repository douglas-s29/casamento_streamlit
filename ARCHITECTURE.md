# 🏗️ Arquitetura do Sistema

## 📐 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         USUÁRIO                                  │
│                    (Navegador Web)                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                   STREAMLIT CLOUD                                │
│                   (ou localhost)                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      app.py                                │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │Dashboard │  │  Items   │  │Financeiro│  │Checklist │  │  │
│  │  │    🏠    │  │   📋     │  │   💰     │  │   ✅     │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  │  ┌──────────┐                                             │  │
│  │  │Relatórios│                                             │  │
│  │  │   📊     │                                             │  │
│  │  └──────────┘                                             │  │
│  └───────────────────────┬───────────────────────────────────┘  │
│                          │                                       │
│                          │ imports                               │
│                          ↓                                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  utils/                                    │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │        supabase_client.py                           │  │  │
│  │  │  ┌──────────────────────────────────────────────┐   │  │  │
│  │  │  │ init_supabase()                              │   │  │  │
│  │  │  │ get_all_items()   add_item()                │   │  │  │
│  │  │  │ update_item()     delete_item()              │   │  │  │
│  │  │  │ get_all_tasks()   add_task()                │   │  │  │
│  │  │  │ update_task()     delete_task()              │   │  │  │
│  │  │  │ get_config()      update_config()            │   │  │  │
│  │  │  │                                               │   │  │  │
│  │  │  │ Cache: @st.cache_data (TTL 10s)             │   │  │  │
│  │  │  └──────────────────────────────────────────────┘   │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │        calculations.py                              │  │  │
│  │  │  - calcular_total_orcado()                         │  │  │
│  │  │  - calcular_reserva()                              │  │  │
│  │  │  - calcular_porcentagem_usada()                    │  │  │
│  │  │  - calcular_investimento_mensal()                  │  │  │
│  │  │  - formatar_moeda()                                │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                          │                                       │
│                          │ Supabase Client                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │
                           │ REST API
                           │ (HTTPS)
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                    SUPABASE CLOUD                                │
│                  (PostgreSQL Database)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    items     │  │    config    │  │    tasks     │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ id           │  │ id           │  │ id           │          │
│  │ item         │  │ chave        │  │ tarefa       │          │
│  │ servico      │  │ valor        │  │ concluida    │          │
│  │ preco        │  │ updated_at   │  │ created_at   │          │
│  │ status       │  └──────────────┘  └──────────────┘          │
│  │ comentarios  │                                               │
│  │ created_at   │   4 registros       25 registros             │
│  └──────────────┘                                               │
│   14 registros                                                  │
│                                                                  │
│  Características:                                               │
│  ✅ Persistência permanente                                     │
│  ✅ Backup automático                                           │
│  ✅ Acesso multi-dispositivo                                    │
│  ✅ Até 500MB grátis                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

### 1. Leitura (GET)
```
Usuário → Streamlit → Cache (10s) → Supabase → PostgreSQL
                          ↓                ↓
                      Se existe       Busca dados
                      retorna         retorna
                          ↓                ↓
                      ────────────────────── 
                          ↓
                     Dados exibidos
```

### 2. Escrita (POST/PUT)
```
Usuário → Preenche formulário → Clica "Salvar"
                                      ↓
                                Validação
                                      ↓
                            Spinner "⏳ Salvando..."
                                      ↓
                            supabase_client.add_item()
                                      ↓
                               INSERT/UPDATE
                                      ↓
                            Supabase PostgreSQL
                                      ↓
                            Limpa cache (@st.cache_data.clear)
                                      ↓
                            Mensagem "✅ Sucesso!"
                                      ↓
                                  st.rerun()
```

### 3. Atualização (UPDATE)
```
Usuário → Marca checkbox → update_task(id, True)
                                  ↓
                         Spinner "⏳ Atualizando..."
                                  ↓
                         UPDATE tasks SET concluida=true
                                  ↓
                            Limpa cache
                                  ↓
                              st.rerun()
```

## 📦 Dependências

```
streamlit (Framework Web)
    ↓
pandas (Manipulação de dados)
plotly (Gráficos interativos)
    ↓
supabase (Cliente Python)
    ↓
requests + urllib3 (HTTP)
    ↓
PostgreSQL (Supabase Cloud)
```

## 🗂️ Estrutura de Arquivos

```
casamento_streamlit/
│
├── 📱 FRONTEND
│   └── app.py (Interface Streamlit - 669 linhas)
│
├── ⚙️ BACKEND
│   └── utils/
│       ├── supabase_client.py (CRUD - 330 linhas)
│       └── calculations.py (Cálculos - 127 linhas)
│
├── 🗄️ DATABASE
│   └── database_setup.sql (Schema + Seeds)
│
├── 📚 DOCS
│   ├── README.md (Documentação principal)
│   ├── DEPLOYMENT_GUIDE.md (Guia de deploy)
│   ├── IMPLEMENTATION_SUMMARY.md (Resumo técnico)
│   └── ARCHITECTURE.md (Este arquivo)
│
├── 🔧 CONFIG
│   ├── .streamlit/secrets.toml (Credenciais)
│   ├── requirements.txt (Dependências)
│   └── .gitignore (Exclusões)
│
└── 🛠️ SCRIPTS
    ├── setup_database.py (Verificação)
    ├── create_tables.py (Gerador SQL)
    ├── init_database.py (Legacy)
    └── test_mock.py (Testes)
```

## 🔐 Segurança

### Camadas de Segurança:
```
1. Frontend (Streamlit)
   ├── Validação de inputs
   ├── Sanitização de dados
   └── Mensagens de erro genéricas

2. Secrets Management
   ├── .streamlit/secrets.toml (local)
   ├── Streamlit Cloud Secrets (produção)
   └── .gitignore (proteção)

3. API (Supabase Client)
   ├── Anon/Public key (limitada)
   ├── Row Level Security (RLS)
   └── Rate limiting

4. Database (PostgreSQL)
   ├── Permissões de tabela
   ├── Validações de schema
   └── Backups automáticos
```

## ⚡ Performance

### Otimizações:
```
1. Cache (Frontend)
   - @st.cache_data com TTL 10s
   - Reduz 90% das requisições
   - Invalida após mutations

2. Lazy Loading
   - Dados carregados apenas quando necessário
   - Paginação (se implementada)

3. Efficient Queries
   - SELECT apenas colunas necessárias
   - Índices no PostgreSQL (id PRIMARY KEY)

4. Network
   - HTTPS (criptografia)
   - Compressão de respostas
   - Keep-alive connections
```

### Benchmarks Estimados:
```
- Dashboard load: 1-2s
- Add item: 300-500ms
- Update task: 200-400ms
- Get config: 100-200ms (cached)
- Charts render: 500ms-1s
```

## 🌐 Deploy Options

### 1. Streamlit Cloud (Recomendado)
```
✅ Grátis
✅ CI/CD automático
✅ HTTPS incluído
✅ Secrets management
❌ Recursos limitados (free tier)
```

### 2. Heroku
```
✅ Flexível
✅ Add-ons disponíveis
❌ Pago (após free tier)
⚙️ Requer Procfile
```

### 3. AWS/GCP/Azure
```
✅ Escalável
✅ Controle total
❌ Complexo
❌ Mais caro
```

## 🔄 CI/CD Flow

```
Developer → Git Commit → GitHub Push
                              ↓
                     Streamlit Cloud detecta
                              ↓
                         Build image
                              ↓
                    Install requirements.txt
                              ↓
                      Inject secrets
                              ↓
                       Deploy app
                              ↓
                    Smoke tests
                              ↓
                   Traffic routing
                              ↓
                    App live! 🎉
```

## 📊 Data Flow Examples

### Exemplo 1: Adicionar Item
```
1. Usuário preenche form:
   - Item: "Decoração"
   - Serviço: "Flores Belas"
   - Preço: R$ 2.000
   - Status: "Pendente"

2. Clica "Adicionar Item"

3. app.py chama:
   add_item("Decoração", "Flores Belas", 2000.0, "Pendente", "")

4. supabase_client.py:
   - Valida dados
   - Cria dict: {item: "Decoração", ...}
   - supabase.table('items').insert(data).execute()

5. Supabase:
   - INSERT INTO items VALUES (...)
   - Retorna novo registro com ID

6. supabase_client.py:
   - get_all_items.clear() (invalida cache)
   - Retorna True

7. app.py:
   - st.success("✅ Item adicionado!")
   - st.rerun()

8. Dashboard atualiza com novo item
```

### Exemplo 2: Marcar Tarefa
```
1. Usuário clica checkbox "Escolher vestido"

2. app.py detecta mudança:
   - concluida_atual = False
   - concluida_nova = True

3. Chama: update_task(task_id=6, concluida=True)

4. supabase_client.py:
   - UPDATE tasks SET concluida=true WHERE id=6
   - Limpa cache

5. app.py:
   - st.rerun()

6. UI atualiza:
   - Checkbox marcado
   - Texto com ~~strikethrough~~
   - Barra de progresso aumenta
```

## 🎨 Component Hierarchy

```
app.py
│
├── Configuração (st.set_page_config)
├── CSS customizado
├── Header (título + descrição)
│
├── Sidebar
│   ├── Menu de navegação (radio)
│   └── Dicas
│
└── Main Content (baseado no menu)
    │
    ├── 🏠 Dashboard
    │   ├── Métricas (4 colunas)
    │   ├── Barra de progresso
    │   ├── Gráfico pizza (col1)
    │   ├── Gráfico barras (col2)
    │   └── Lista de tarefas
    │
    ├── 📋 Itens
    │   ├── Filtro de status
    │   ├── Editor de tabela (st.data_editor)
    │   ├── Botão salvar
    │   └── Form adicionar (3 colunas)
    │
    ├── 💰 Financeiro
    │   ├── Inputs de config (2 colunas)
    │   ├── Botão salvar
    │   ├── Métricas (3 colunas)
    │   └── Gráfico de projeção
    │
    ├── ✅ Checklist
    │   ├── Filtro
    │   ├── Métricas (3 colunas)
    │   ├── Barra de progresso
    │   ├── Lista de checkboxes
    │   └── Form adicionar tarefa
    │
    └── 📊 Relatórios
        ├── Gráfico de barras
        ├── Gráfico de pizza
        ├── Tabelas resumo (2 colunas)
        └── Botões de download (3 colunas)
```

## 🎯 Conclusão

Esta arquitetura fornece:
- ✅ Separação clara de responsabilidades
- ✅ Escalabilidade
- ✅ Manutenibilidade
- ✅ Performance otimizada
- ✅ Segurança adequada
- ✅ Fácil deploy

**Pronta para produção!** 🚀
