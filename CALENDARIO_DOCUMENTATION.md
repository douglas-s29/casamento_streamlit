# 📅 Calendário de Visitas - Documentação

## 📝 Visão Geral

A seção "📅 Calendário de Visitas" permite aos noivos organizarem visitas a fornecedores e locais do casamento, com interface limpa e calendário interativo.

## ✨ Funcionalidades Implementadas

### 1. 🔔 Próximas Visitas
- Exibe agendamentos dos próximos 7 dias
- Destaca visitas de HOJE em vermelho
- Exibe "Amanhã" e "Em X dias" de forma clara
- Cards expansíveis com detalhes completos
- Botões para editar, deletar e abrir no Google Maps

### 2. 📆 Calendário Interativo
- **Biblioteca**: streamlit-calendar (FullCalendar.js)
- **Feriados brasileiros 2026** destacados em vermelho
- Visualizações: Mês, Semana, Dia
- Navegação entre meses (← →)
- Eventos clicáveis com cores por status
- **Fallback**: date_input caso streamlit-calendar não esteja instalado

### 3. ➕ Agendar Nova Visita
- Formulário completo com validação
- Campos obrigatórios: Data, Hora, Categoria, Local
- Campos opcionais: Contato, Telefone, Endereço, Link, Observações
- Status com cores automáticas
- 16 categorias pré-definidas

### 4. 📋 Todos os Agendamentos
- Lista completa de agendamentos
- Filtros por: Categoria, Status, Mês
- Cards com informações detalhadas
- Edição inline com formulário
- Exclusão com confirmação
- Integração Google Maps

### 5. 📊 Estatísticas
- Total de agendamentos
- Contadores por status:
  - ⏳ Agendados
  - ✅ Confirmados
  - ✔️ Concluídos

## 🗄️ Banco de Dados

### Tabela: `agendamentos`

```sql
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    local VARCHAR(200) NOT NULL,
    endereco TEXT,
    telefone VARCHAR(20),
    contato VARCHAR(100),
    observacao TEXT,
    status VARCHAR(50) DEFAULT '⏳ Agendado',
    link TEXT,
    cor VARCHAR(20) DEFAULT '#FF69B4',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Índices
- `idx_agendamentos_data` - Busca rápida por data
- `idx_agendamentos_status` - Filtro por status

## 📂 Categorias de Agendamento

1. 🍰 Buffet
2. 🏛️ Igreja/Cerimônia
3. 🎪 Espaço para Festa
4. 📸 Fotógrafo
5. 🎥 Videomaker
6. 🎵 DJ/Música
7. 🌸 Decoração
8. 🚗 Transporte
9. 💐 Flores
10. 🎂 Bolo/Doces
11. 👗 Vestido/Roupa
12. 💄 Cabelo e Maquiagem
13. 📄 Cartório/Documentos
14. 🏨 Hospedagem
15. 🎁 Lembrancinhas
16. 📋 Outros

## 📊 Status de Agendamento

| Status | Emoji | Cor | Hex Code |
|--------|-------|-----|----------|
| Agendado | ⏳ | Laranja | #FFA500 |
| Confirmado | ✅ | Verde | #4CAF50 |
| Cancelado | 🚫 | Vermelho | #F44336 |
| Concluído | ✔️ | Cinza | #9E9E9E |
| Reagendar | ⏰ | Azul | #2196F3 |

## 🇧🇷 Feriados Brasileiros 2026

| Data | Feriado |
|------|---------|
| 01/01 | Ano Novo |
| 16/02 | Carnaval |
| 17/02 | Carnaval |
| 03/04 | Sexta-feira Santa |
| 21/04 | Tiradentes |
| 01/05 | Dia do Trabalho |
| 04/06 | Corpus Christi |
| 07/09 | Independência do Brasil |
| 12/10 | Nossa Senhora Aparecida |
| 02/11 | Finados |
| 15/11 | Proclamação da República |
| 20/11 | Dia da Consciência Negra |
| 25/12 | Natal |

## 🔧 Funções CRUD (Supabase)

### `get_all_agendamentos()`
Retorna todos os agendamentos ordenados por data e hora.

### `get_agendamentos_by_data(data: str)`
Retorna agendamentos de uma data específica (YYYY-MM-DD).

### `get_proximos_agendamentos(dias: int = 7)`
Retorna agendamentos dos próximos X dias.

### `add_agendamento(...)`
Adiciona novo agendamento com todos os campos.

### `update_agendamento(id: int, data: dict)`
Atualiza agendamento existente.

### `delete_agendamento(id: int)`
Deleta agendamento por ID.

## 📦 Dependências Adicionadas

```txt
streamlit-calendar>=0.8.0
holidays>=0.35
```

## 🎨 Design e UX

### Princípios Aplicados
- ✅ Minimalista e limpo (sem poluição visual)
- ✅ Cores suaves (rosa/vermelho para destaque)
- ✅ Cards expansíveis em vez de tabelas
- ✅ Ícones intuitivos
- ✅ Feedback visual imediato
- ✅ Mobile-friendly (seguindo padrões existentes)

### Cores Principais
- Rosa primário: #FF69B4
- Vermelho feriado: #F44336
- Fundo: #FFF5F7 (existente)

## 📱 Mobile Optimization

O calendário segue os mesmos padrões de otimização mobile do resto da aplicação:
- Botões touch-friendly (48px)
- Inputs com fonte 16px (sem zoom iOS)
- Layout responsivo
- Cards empilháveis

## 🚀 Como Usar

### 1. Configurar Banco de Dados
Execute o SQL em `create_agendamentos_table.sql` no Supabase:
```bash
# No SQL Editor do Supabase, executar:
CREATE TABLE agendamentos (...);
CREATE INDEX idx_agendamentos_data ON agendamentos(data);
CREATE INDEX idx_agendamentos_status ON agendamentos(status);
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Aplicação
```bash
streamlit run app.py
```

### 4. Acessar Calendário
Navegar para **📅 Calendário** no menu lateral.

## 🔍 Exemplo de Uso

### Adicionar Agendamento
1. Clicar em "➕ Agendar Nova Visita"
2. Preencher:
   - Data: 15/03/2026
   - Hora: 14:00
   - Categoria: 🍰 Buffet
   - Local: Chácara Magali
   - Contato: João Silva
   - Telefone: (11) 98765-4321
   - Endereço: Rua ABC, 123
   - Link: https://goo.gl/maps/xyz
3. Clicar em "Agendar Visita"
4. ✅ Confirmação: "Visita agendada para 15/03/2026 às 14:00!"

### Editar Agendamento
1. Clicar em "✏️ Editar" no card do agendamento
2. Alterar campos desejados
3. Clicar em "✅ Salvar"
4. ✅ Confirmação: "Agendamento atualizado!"

### Filtrar Agendamentos
1. Selecionar filtros:
   - Categoria: 🍰 Buffet
   - Status: ✅ Confirmado
   - Mês: Março
2. Ver resultados filtrados instantaneamente

## 🐛 Troubleshooting

### Calendário não aparece
**Causa**: streamlit-calendar não instalado

**Solução**: 
```bash
pip install streamlit-calendar
```
Ou usar o fallback (date_input) automaticamente ativado.

### Feriados não aparecem
**Causa**: Constante FERIADOS_2026 não definida

**Solução**: Verificar se o import está correto em app.py

### Erro ao salvar agendamento
**Causa**: Tabela não criada no Supabase

**Solução**: Executar SQL de criação da tabela

## ✅ Checklist de Verificação

- [x] Tabela `agendamentos` criada no Supabase
- [x] Dependências instaladas (requirements.txt)
- [x] Funções CRUD em utils/supabase_client.py
- [x] Constantes definidas (FERIADOS_2026, CATEGORIAS, STATUS, CORES)
- [x] Menu "📅 Calendário" adicionado
- [x] Seção "Próximas Visitas" implementada
- [x] Calendário interativo com streamlit-calendar
- [x] Formulário "Agendar Nova Visita"
- [x] Lista "Todos os Agendamentos" com filtros
- [x] Edição inline de agendamentos
- [x] Exclusão de agendamentos
- [x] Estatísticas
- [x] Integração Google Maps
- [x] Feriados destacados no calendário
- [x] Mobile-friendly

## 📚 Referências

- [Streamlit Calendar Docs](https://github.com/im-perativa/streamlit-calendar)
- [FullCalendar.js](https://fullcalendar.io/)
- [Supabase Docs](https://supabase.com/docs)
- [Python holidays](https://pypi.org/project/holidays/)

## 🎯 Próximas Melhorias (Futuro)

- [ ] Notificações por email antes das visitas
- [ ] Sincronização com Google Calendar
- [ ] Importar/Exportar agendamentos (.ics)
- [ ] Mapa com todas as visitas
- [ ] Chat com fornecedores
- [ ] Avaliação após visita
- [ ] Lembretes automáticos

---

**Desenvolvido com 💕 para tornar o planejamento do casamento mais fácil!**
