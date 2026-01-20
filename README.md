# 💍 Gerenciador de Casamento

## 📝 Descrição do Projeto

Aplicação web completa desenvolvida em Streamlit para gerenciar todo o planejamento do seu casamento. Organize seu orçamento, acompanhe itens contratados, gerencie tarefas e visualize relatórios detalhados - tudo em um só lugar!

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

### ✅ Checklist de Tarefas
- Lista completa de tarefas típicas de casamento (20+ tarefas)
- Adicionar tarefas personalizadas
- Marcar tarefas como concluídas
- Filtrar por status (Todas/Pendentes/Concluídas)
- Barra de progresso mostrando % de conclusão

### 📊 Relatórios
- Gráfico de barras com gastos por item
- Gráfico de pizza com distribuição percentual
- Tabela resumo: itens contratados vs pendentes
- Download de dados em CSV e TXT
- Resumo financeiro completo

## 🔧 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

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

## 🚀 Como Usar

### Executar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`

### Navegação

Use o menu lateral (sidebar) para navegar entre as 5 seções principais:

1. **🏠 Dashboard** - Visão geral e métricas
2. **📋 Itens do Casamento** - Gerenciar itens e fornecedores
3. **💰 Planejamento Financeiro** - Configurações e projeções
4. **✅ Checklist** - Tarefas do casamento
5. **📊 Relatórios** - Análises e downloads

## 📁 Estrutura do Projeto

```
casamento_streamlit/
├── app.py                    # Arquivo principal da aplicação
├── requirements.txt          # Dependências do projeto
├── README.md                # Este arquivo
├── .gitignore               # Arquivos ignorados pelo Git
├── utils/                   # Módulos utilitários
│   ├── __init__.py
│   ├── data_manager.py      # Gerenciamento de dados JSON
│   └── calculations.py      # Funções de cálculo financeiro
└── data/                    # Dados locais (criado automaticamente)
    ├── items.json           # Itens do casamento
    ├── config.json          # Configurações financeiras
    └── tasks.json           # Tarefas/checklist
```

## 💾 Persistência de Dados

Os dados são salvos automaticamente em arquivos JSON na pasta `data/`:

- **items.json**: Armazena todos os itens do casamento (preços, fornecedores, status)
- **config.json**: Configurações financeiras (orçamento, taxa de juros, etc.)
- **tasks.json**: Lista de tarefas e checklist

### Backup dos Dados

Para fazer backup dos seus dados:

1. Copie a pasta `data/` para um local seguro
2. Ou baixe os arquivos CSV através da seção "📊 Relatórios"

### Restaurar Dados

Para restaurar dados de um backup:

1. Substitua os arquivos na pasta `data/` pelos arquivos do backup
2. Reinicie a aplicação

## 🎨 Personalização

### Modificar Dados Iniciais

Os dados iniciais são definidos em `utils/data_manager.py`:

- `get_default_items()` - Itens iniciais do casamento
- `get_default_config()` - Configurações financeiras padrão
- `get_default_tasks()` - Lista inicial de tarefas

### Modificar Valores Padrão

No arquivo `utils/data_manager.py`, você pode alterar:

- Orçamento máximo padrão: R$ 30.000,00
- Taxa de juros: 0,35% ao mês
- Número de meses: 12 meses

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
4. Os dados são salvos automaticamente

### Cenário 2: Marcar uma tarefa como concluída

1. Vá para **✅ Checklist**
2. Clique no checkbox ao lado da tarefa
3. A porcentagem de conclusão é atualizada automaticamente

### Cenário 3: Ajustar orçamento

1. Vá para **💰 Planejamento Financeiro**
2. Altere o valor do "Orçamento Máximo"
3. Clique em "Salvar Configurações"
4. Todos os cálculos são atualizados automaticamente

## ⚠️ Observações Importantes

- Todos os valores monetários são formatados em Reais (R$)
- A aplicação valida valores negativos automaticamente
- Alertas são exibidos quando o orçamento ultrapassar 80%
- Os dados são salvos localmente no seu computador
- A pasta `data/` não é versionada no Git (incluída no .gitignore)

## 🐛 Solução de Problemas

### Erro ao executar a aplicação

Certifique-se de que:
1. O Python 3.8+ está instalado
2. Todas as dependências foram instaladas: `pip install -r requirements.txt`
3. Você está no diretório correto do projeto

### Dados não estão sendo salvos

Verifique se:
1. A pasta `data/` existe e tem permissões de escrita
2. Não há erros no console ao salvar

### Gráficos não aparecem

1. Verifique se o Plotly está instalado: `pip install plotly`
2. Tente atualizar a página (F5)

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

Se tiver dúvidas ou sugestões, abra uma [issue](https://github.com/douglas-s29/casamento_streamlit/issues) no GitHub.