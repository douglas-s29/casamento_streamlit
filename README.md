# 💍 Gerenciador de Casamento

## 📝 Descrição do Projeto

Aplicação web completa desenvolvida em Streamlit para gerenciar todo o planejamento do seu casamento. Organize seu orçamento, acompanhe itens contratados, gerencie tarefas e visualize relatórios detalhados - tudo em um só lugar!

**⚠️ IMPORTANTE: Todos os dados são persistidos no Supabase (PostgreSQL na nuvem) para garantir segurança e disponibilidade permanente!**

**📱 NOVO: Totalmente otimizado para mobile! Use em qualquer dispositivo - celular, tablet ou desktop.**

**Desenvolvido com amor para tornar seu grande dia ainda mais especial! 💕**

## ✨ Funcionalidades

### 🏠 Dashboard
- Visão geral do orçamento com métricas em tempo real
- Gráficos visuais (pizza/barras) mostrando distribuição dos gastos
- Indicador de progresso do orçamento
- Lista das próximas tarefas pendentes
- Alertas quando o orçamento ultrapassar 80%

### 📋 Itens do Casamento
- Tabela interativa e editável com todos os itens do casamento
- Adicionar, editar e remover itens facilmente
- Marcar itens como "Contratado" ou "Pendente"
- Filtrar por status
- Cálculo automático do total orçado
- **Dados salvos permanentemente no Supabase**

### 💰 Planejamento Financeiro
- Configurações personalizáveis:
  - Orçamento máximo
  - Taxa de juros mensal
  - Número de meses até o casamento
  - Valor inicial disponível
- Cálculos automáticos:
  - Total orçado
  - Reserva disponível
  - Investimento mensal recomendado
- Gráfico de projeção de investimento ao longo do tempo
- Alertas visuais de orçamento
- **Configurações persistidas no Supabase**

### ✅ Checklist de Tarefas
- Lista completa de tarefas típicas de casamento (25+ tarefas)
- Adicionar tarefas personalizadas
- **Editar e deletar tarefas**
- Marcar tarefas como concluídas em tempo real
- Filtrar por status (Todas/Pendentes/Concluídas)
- Barra de progresso mostrando % de conclusão
- **Progresso salvo instantaneamente no Supabase**

### 💸 Orçamentos
- Gerenciar categorias de serviços (Buffet, Igreja, Fotografia, etc.)
- Adicionar, editar e deletar categorias
- Cadastrar múltiplos orçamentos por categoria
- Incluir informações de fornecedor, valor, telefone e observações
- Filtrar orçamentos por categoria
- Visualizar totais por categoria e total geral
- **Organização completa de todos os orçamentos recebidos**

### 📊 Relatórios
- Gráfico de barras com gastos por item
- Gráfico de pizza com distribuição percentual
- Tabela resumo: itens contratados vs pendentes
- Download de dados em CSV e TXT
- Resumo financeiro completo

### 📅 Calendário de Visitas (NEW!)
- **Calendário interativo** com visualizações mensais, semanais e diárias
- **Feriados brasileiros 2026** destacados automaticamente
- **Próximas visitas** - resumo dos próximos 7 dias com destaque para hoje
- **16 categorias** de agendamento (Buffet, Igreja, Fotógrafo, etc.)
- **5 status** com cores (Agendado, Confirmado, Cancelado, Concluído, Reagendar)
- Formulário completo para agendar visitas
- **Filtros** por categoria, status e mês
- **Edição inline** de agendamentos
- **Integração Google Maps** para localização
- **Estatísticas** de agendamentos
- **Fallback** para date picker caso biblioteca não esteja instalada

## 📱 Otimização Mobile (NEW!)

**O aplicativo agora está totalmente otimizado para dispositivos móveis!**

### ✨ Recursos Mobile-First:
- 📱 **Sidebar Colapsável**: Começa fechada em mobile, economizando espaço
- 🎯 **Botões Touch-Friendly**: Mínimo 48x48px (Apple HIG compliance)
- 📊 **Dashboard Responsivo**: Layout 2x2 em vez de 4 colunas
- 💳 **Cards Mobile**: Orçamentos exibidos em cards em vez de tabelas
- 🔤 **Tipografia Otimizada**: Fonte mínima 16px (sem zoom automático iOS)
- 📏 **Inputs Maiores**: Campos de formulário com 48px de altura
- 🎨 **CSS Responsivo**: Breakpoints mobile (768px) e tablet (1024px)

### 📐 Dispositivos Suportados:
- ✅ iPhone SE (375px)
- ✅ iPhone 12/13 (390px)
- ✅ Samsung Galaxy (360px)
- ✅ iPad Mini (768px)
- ✅ iPad Pro (1024px+)

### 📚 Documentação Mobile:
- **[MOBILE_OPTIMIZATION_SUMMARY.md](MOBILE_OPTIMIZATION_SUMMARY.md)** - Detalhes técnicos completos
- **[MOBILE_OPTIMIZATION_VISUAL_GUIDE.md](MOBILE_OPTIMIZATION_VISUAL_GUIDE.md)** - Guia visual com comparações

## 🔧 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Conta no Supabase (gratuita)

## 📥 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/douglas-s29/casamento_streamlit.git
cd casamento_streamlit
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ☁️ Configuração do Supabase

### Passo 1: Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com) e crie uma conta gratuita
2. Clique em "New Project"
3. Preencha os dados do projeto:
   - Nome: `casamento-streamlit` (ou o nome que preferir)
   - Database Password: Escolha uma senha segura
   - Region: Escolha a região mais próxima
4. Aguarde a criação do projeto (leva ~2 minutos)

### Passo 2: Obter Credenciais

1. No dashboard do projeto, vá em **Settings** → **API**
2. Copie:
   - **Project URL** (formato: `https://xxx.supabase.co`)
   - **anon/public key** (token longo começando com `eyJ...`)

### Passo 3: Configurar Secrets Localmente

1. Crie o diretório `.streamlit` na raiz do projeto:
```bash
mkdir .streamlit
```

2. Crie o arquivo `.streamlit/secrets.toml`:
```bash
# Windows
type nul > .streamlit\secrets.toml

# Linux/Mac
touch .streamlit/secrets.toml
```

3. Edite o arquivo `.streamlit/secrets.toml` e adicione suas credenciais:
```toml
[supabase]
url = "SUA_PROJECT_URL_AQUI"
key = "SUA_ANON_KEY_AQUI"
```

**⚠️ IMPORTANTE: Nunca commite este arquivo! Ele já está no .gitignore**

### Passo 4: Criar Tabelas no Banco de Dados

1. No dashboard do Supabase, vá em **SQL Editor**
2. Clique em **New query**
3. Copie todo o conteúdo do arquivo `database_setup.sql` deste repositório
4. Cole no editor SQL do Supabase
5. Clique em **Run** (ou pressione Ctrl+Enter)
6. Aguarde a confirmação: "Success. No rows returned"

Isso criará:
- ✅ Tabela `items` (itens do casamento)
- ✅ Tabela `config` (configurações financeiras)
- ✅ Tabela `tasks` (checklist de tarefas)
- ✅ Dados iniciais populados

### Passo 5: Verificar Tabelas

1. No dashboard do Supabase, vá em **Table Editor**
2. Você deve ver as 5 tabelas: `items`, `config`, `tasks`, `categorias`, `orcamentos`
3. Cada tabela deve ter dados iniciais

## 🚀 Como Usar

### Executar a aplicação localmente

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`

### Navegação

Use o menu lateral (sidebar) para navegar entre as 7 seções principais:

1. **🏠 Dashboard** - Visão geral e métricas
2. **📋 Itens do Casamento** - Gerenciar itens e fornecedores
3. **💰 Planejamento Financeiro** - Configurações e projeções
4. **✅ Checklist** - Tarefas do casamento (com edição e exclusão)
5. **📊 Relatórios** - Análises e downloads
6. **💸 Orçamentos** - Gerenciar orçamentos por categoria
7. **📅 Calendário** - Organizar visitas a fornecedores (NOVO!)

## 📁 Estrutura do Projeto

```
casamento_streamlit/
├── app.py                          # Arquivo principal da aplicação
├── requirements.txt                # Dependências do projeto
├── README.md                       # Este arquivo
├── .gitignore                      # Arquivos ignorados pelo Git
├── database_setup.sql              # SQL para criar tabelas no Supabase
├── create_agendamentos_table.sql   # SQL para tabela de agendamentos (NOVO!)
├── create_tables.py                # Script auxiliar para gerar SQL
├── init_database.py                # Script de inicialização (legacy)
├── CALENDARIO_DOCUMENTATION.md     # Documentação completa do Calendário (NOVO!)
├── CALENDAR_VISUAL_GUIDE.md        # Guia visual do Calendário (NOVO!)
├── .streamlit/
│   └── secrets.toml               # Credenciais Supabase (NÃO commitar!)
└── utils/                          # Módulos utilitários
    ├── __init__.py
    ├── supabase_client.py         # Cliente e operações Supabase (+ funções de agendamentos)
    ├── calculations.py            # Funções de cálculo financeiro
    └── data_manager.py            # Gerenciamento de dados (legacy)
```

## 💾 Persistência de Dados

### ☁️ Supabase (PostgreSQL na Nuvem)

Todos os dados são salvos automaticamente no Supabase:

- **items**: Todos os itens do casamento (preços, fornecedores, status)
- **config**: Configurações financeiras (orçamento, taxa de juros, etc.)
- **tasks**: Lista de tarefas e checklist
- **categorias**: Categorias de serviços para orçamentos
- **orcamentos**: Orçamentos recebidos de fornecedores
- **agendamentos**: Visitas agendadas com fornecedores (NOVO!)

### ✅ Vantagens do Supabase:
- ✅ Dados persistem permanentemente na nuvem
- ✅ Acesso de qualquer dispositivo
- ✅ Backup automático
- ✅ Sem perda de dados em reinicializações
- ✅ Escalável e seguro
- ✅ Gratuito até 500MB de dados

### 🔄 Como os Dados São Salvos:

1. **Adicionar Item**: INSERT instantâneo no Supabase
2. **Editar Item**: UPDATE em tempo real
3. **Marcar Tarefa**: Atualização automática no banco
4. **Alterar Orçamento**: Salvo imediatamente no Supabase

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Push para GitHub

```bash
git add .
git commit -m "Setup completo com Supabase"
git push origin main
```

### Passo 2: Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione:
   - Repository: `douglas-s29/casamento_streamlit`
   - Branch: `main`
   - Main file path: `app.py`

### Passo 3: Configurar Secrets na Cloud

1. Na página de deploy, clique em "Advanced settings"
2. Em "Secrets", cole:
```toml
[supabase]
url = "SUA_PROJECT_URL_AQUI"
key = "SUA_ANON_KEY_AQUI"
```
3. Clique em "Deploy!"

Pronto! Seu app estará disponível em uma URL pública tipo:
`https://seu-app.streamlit.app`

## 📊 Cálculos Financeiros

### Investimento Mensal

O cálculo do investimento mensal recomendado usa a fórmula de valor futuro com aportes mensais:

```
VF = VP * (1 + i)^n + PMT * [((1 + i)^n - 1) / i]
```

Onde:
- VF = Valor Final desejado (orçamento máximo)
- VP = Valor Presente (valor inicial disponível)
- PMT = Pagamento mensal (calculado)
- i = Taxa de juros mensal
- n = Número de meses

### Reserva Disponível

```
Reserva = Orçamento Máximo - Total Orçado
```

### Porcentagem Utilizada

```
Porcentagem = (Total Orçado / Orçamento Máximo) × 100
```

## 🎯 Casos de Uso

### Cenário 1: Adicionar um novo fornecedor

1. Vá para **📋 Itens do Casamento**
2. Preencha o formulário "Adicionar Novo Item"
3. Clique em "Adicionar Item"
4. Os dados são salvos **instantaneamente no Supabase**

### Cenário 2: Marcar uma tarefa como concluída

1. Vá para **✅ Checklist**
2. Clique no checkbox ao lado da tarefa
3. A atualização é salva **automaticamente no Supabase**
4. A porcentagem de conclusão é atualizada em tempo real

### Cenário 3: Ajustar orçamento

1. Vá para **💰 Planejamento Financeiro**
2. Altere o valor do "Orçamento Máximo"
3. Clique em "Salvar Configurações"
4. Todos os cálculos são atualizados e **salvos no Supabase**

## ⚠️ Observações Importantes

- Todos os valores monetários são formatados em Reais (R$)
- A aplicação valida valores negativos automaticamente
- Alertas são exibidos quando o orçamento ultrapassar 80%
- Os dados são salvos **permanentemente no Supabase**
- Conexão com internet é necessária para acessar os dados
- Credenciais do Supabase devem ser mantidas em segredo

## 🐛 Solução de Problemas

### Erro: "Erro ao conectar ao Supabase"

**Causas possíveis:**
1. Arquivo `.streamlit/secrets.toml` não existe ou está mal configurado
2. Credenciais incorretas
3. Sem conexão com internet

**Solução:**
1. Verifique se o arquivo `.streamlit/secrets.toml` existe
2. Confirme que as credenciais estão corretas (URL e key)
3. Teste sua conexão com internet

### Erro: "Tabela não existe"

**Causa:** As tabelas não foram criadas no Supabase

**Solução:**
1. Acesse o SQL Editor do Supabase
2. Execute todo o conteúdo de `database_setup.sql`
3. Verifique no Table Editor se as tabelas foram criadas

### Dados não aparecem

**Causa:** Tabelas vazias ou erro na query

**Solução:**
1. Verifique no Supabase Table Editor se há dados nas tabelas
2. Execute novamente o SQL de inserção de dados iniciais
3. Limpe o cache do Streamlit: `streamlit cache clear`

### Aplicação muito lenta

**Causa:** Muitas requisições ao Supabase

**Solução:**
- O app usa cache automático (`@st.cache_data`) com TTL de 10 segundos
- Se necessário, aumente o TTL em `utils/supabase_client.py`

## 🔒 Segurança

### Boas Práticas Implementadas:

- ✅ Credenciais em arquivo separado (`.streamlit/secrets.toml`)
- ✅ Arquivo de secrets no `.gitignore`
- ✅ Uso de variáveis de ambiente
- ✅ Tratamento de erros em todas operações
- ✅ Validação de dados antes de inserir
- ✅ Uso da API key pública (anon) do Supabase

### **NUNCA**:
- ❌ Commitar o arquivo `secrets.toml`
- ❌ Compartilhar suas credenciais
- ❌ Usar a Service Role Key em produção

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal.

## 👰🤵 Sobre

Desenvolvido com 💕 para ajudar casais a organizarem o casamento dos seus sonhos!

**Bom planejamento e felicidades! 🎉💍**

---

## 📞 Suporte

Se tiver dúvidas ou sugestões:
- Abra uma [issue](https://github.com/douglas-s29/casamento_streamlit/issues) no GitHub
- Consulte a [documentação do Supabase](https://supabase.com/docs)
- Consulte a [documentação do Streamlit](https://docs.streamlit.io)

## 🆕 Changelog

### v2.2.0 - Calendário de Visitas (NEW!)
- ✅ Nova seção "📅 Calendário" para organizar visitas a fornecedores
- ✅ **Calendário interativo** com streamlit-calendar (FullCalendar.js)
- ✅ **13 feriados brasileiros 2026** destacados no calendário
- ✅ Seção "Próximas Visitas" com agendamentos dos próximos 7 dias
- ✅ **16 categorias** de agendamento (Buffet, Igreja, Fotógrafo, etc.)
- ✅ **5 status** com cores personalizadas (Agendado, Confirmado, Cancelado, etc.)
- ✅ Formulário completo para agendar visitas
- ✅ Filtros por categoria, status e mês
- ✅ Edição inline de agendamentos
- ✅ Integração com Google Maps
- ✅ Estatísticas de agendamentos
- ✅ Tabela `agendamentos` no Supabase
- ✅ Funções helper para parsing de data/hora
- ✅ Fallback para date picker caso biblioteca não instalada
- ✅ Documentação completa (CALENDARIO_DOCUMENTATION.md)
- ✅ Guia visual (CALENDAR_VISUAL_GUIDE.md)

### v2.1.0 - Novas Funcionalidades e Melhorias
- ✅ Nova seção "💸 Orçamentos" para gerenciar orçamentos por categoria
- ✅ CRUD completo de categorias (Buffet, Igreja, Fotografia, etc.)
- ✅ CRUD completo de orçamentos com fornecedor, valor, telefone e observações
- ✅ Filtros por categoria e totais automáticos
- ✅ Checklist melhorado com opções de editar e deletar tarefas
- ✅ Correção do campo taxa de juros (agora aceita valores até 100%)
- ✅ Interface aprimorada com melhor experiência do usuário

### v2.0.0 - Migração para Supabase
- ✅ Migração completa de JSON para Supabase
- ✅ Persistência permanente na nuvem
- ✅ CRUD completo para items, tasks e config
- ✅ Cache otimizado para performance
- ✅ Mensagens de feedback ao usuário
- ✅ Tratamento de erros robusto

### v1.0.0 - Versão Inicial
- ✅ Sistema básico com arquivos JSON locais
- ✅ Dashboard com métricas
- ✅ Gerenciamento de itens
- ✅ Planejamento financeiro
- ✅ Checklist de tarefas
- ✅ Relatórios e exports