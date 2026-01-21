# 🚀 Guia de Deploy - Gerenciador de Casamento

Este guia contém instruções passo a passo para configurar e fazer deploy da aplicação.

## 📋 Pré-requisitos

- [ ] Conta no GitHub
- [ ] Conta no Supabase (gratuita)
- [ ] Conta no Streamlit Cloud (gratuita)
- [ ] Python 3.8+ instalado localmente (para testes)

## 🗄️ PARTE 1: Configurar Supabase

### Passo 1: Criar Projeto

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "Start your project" → "Sign in"
3. Faça login com GitHub
4. Clique em "New Project"
5. Preencha:
   - **Name**: casamento-streamlit
   - **Database Password**: Escolha uma senha forte
   - **Region**: South America (São Paulo) - ou mais próxima
   - **Pricing Plan**: Free
6. Clique em "Create new project"
7. ⏱️ Aguarde ~2 minutos para o projeto ser criado

### Passo 2: Copiar Credenciais

1. No menu lateral, vá em **Settings** (⚙️) → **API**
2. Na seção **Project API keys**, copie:
   - **URL**: `https://xxxxx.supabase.co`
   - **anon public**: Token longo começando com `eyJ...`
3. 📝 Cole essas informações em um local seguro

### Passo 3: Criar Tabelas

1. No menu lateral, clique em **SQL Editor** (ícone de código)
2. Clique no botão **New query**
3. Copie **TODO** o conteúdo do arquivo `database_setup.sql` deste repositório
4. Cole no editor SQL
5. Clique em **Run** (ou Ctrl+Enter)
6. ✅ Aguarde: "Success. No rows returned"

### Passo 4: Verificar Tabelas

1. No menu lateral, clique em **Table Editor** (ícone de tabela)
2. Você deve ver 3 tabelas:
   - ✅ **items** (14 registros)
   - ✅ **config** (4 registros)
   - ✅ **tasks** (25 registros)
3. Clique em cada tabela para ver os dados iniciais

**🎉 Supabase configurado com sucesso!**

---

## 💻 PARTE 2: Testar Localmente

### Passo 1: Clonar Repositório

```bash
git clone https://github.com/douglas-s29/casamento_streamlit.git
cd casamento_streamlit
```

### Passo 2: Criar Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Secrets

1. Criar diretório:
```bash
mkdir .streamlit
```

2. Criar arquivo `.streamlit/secrets.toml`:
```bash
# Windows
type nul > .streamlit\secrets.toml

# Linux/Mac
touch .streamlit/secrets.toml
```

3. Editar `.streamlit/secrets.toml` e adicionar:
```toml
[supabase]
url = "SUA_URL_DO_SUPABASE_AQUI"
key = "SUA_ANON_KEY_DO_SUPABASE_AQUI"
```

### Passo 5: Executar Aplicação

```bash
streamlit run app.py
```

**✅ A aplicação deve abrir em http://localhost:8501**

### Passo 6: Testar Funcionalidades

- [ ] Dashboard carrega com dados do Supabase
- [ ] Adicionar novo item
- [ ] Editar item existente
- [ ] Marcar tarefa como concluída
- [ ] Alterar orçamento
- [ ] Visualizar relatórios
- [ ] Exportar dados em CSV

**🎉 Testes locais concluídos!**

---

## ☁️ PARTE 3: Deploy no Streamlit Cloud

### Passo 1: Push para GitHub

1. Certifique-se de que `.streamlit/secrets.toml` NÃO está commitado:
```bash
git status
# secrets.toml deve aparecer em "Untracked files" e ser ignorado
```

2. Commit e push:
```bash
git add .
git commit -m "Setup completo com Supabase"
git push origin main
```

### Passo 2: Acessar Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em "Sign in" → "Continue with GitHub"
3. Autorize o Streamlit Cloud

### Passo 3: Criar Nova App

1. Clique em "New app"
2. Selecione:
   - **Repository**: douglas-s29/casamento_streamlit
   - **Branch**: main
   - **Main file path**: app.py
3. Clique em "Advanced settings..."

### Passo 4: Configurar Secrets na Cloud

1. Na seção **Secrets**, cole:
```toml
[supabase]
url = "SUA_URL_DO_SUPABASE_AQUI"
key = "SUA_ANON_KEY_DO_SUPABASE_AQUI"
```

2. Clique em "Save"
3. Clique em "Deploy!"

### Passo 5: Aguardar Deploy

⏱️ Aguarde ~2-3 minutos para o deploy completar

**✅ Sua aplicação estará disponível em:**
`https://seu-username-casamento-streamlit.streamlit.app`

### Passo 6: Testar App em Produção

- [ ] Acesse a URL pública
- [ ] Teste todas as funcionalidades
- [ ] Verifique se dados persistem após refresh
- [ ] Compartilhe o link com outras pessoas para testar

**🎉 Deploy concluído com sucesso!**

---

## 🔧 Troubleshooting

### Erro: "Erro ao conectar ao Supabase"

**Possíveis causas:**
- Secrets não configurados
- URL ou key incorretos
- Projeto Supabase desativado

**Solução:**
1. Verifique se os secrets estão corretos
2. Verifique se o projeto Supabase está ativo
3. Teste a conexão localmente primeiro

### Erro: "Tabela não existe"

**Causa:** Tabelas não foram criadas no Supabase

**Solução:**
1. Execute o SQL do arquivo `database_setup.sql`
2. Verifique no Table Editor se as tabelas existem

### App está lento

**Causa:** Cache desabilitado ou muitas requisições

**Solução:**
1. Verifique se o cache está funcionando (TTL=10s)
2. Reduza a frequência de reloads
3. Upgrade para plano pago do Supabase se necessário

### Dados não aparecem

**Causa:** Tabelas vazias

**Solução:**
1. Verifique no Supabase Table Editor
2. Execute novamente os INSERTs do `database_setup.sql`

---

## 📊 Monitoramento

### No Supabase:
- **Database** → **Usage**: Veja uso de armazenamento
- **API** → **Logs**: Veja logs de requisições

### No Streamlit Cloud:
- **Logs**: Veja logs da aplicação
- **Analytics**: Veja número de visitantes

---

## 🔒 Segurança

### ✅ Boas Práticas Implementadas:
- Secrets em arquivo separado
- `.gitignore` configurado
- Uso de anon key (não service role)
- Validação de inputs

### ⚠️ NUNCA:
- Commitar `secrets.toml`
- Compartilhar service role key
- Expor credenciais em código

---

## 📈 Próximos Passos (Opcional)

### Melhorias Futuras:
- [ ] Adicionar autenticação de usuários
- [ ] Permitir upload de imagens
- [ ] Criar app mobile com Flutter
- [ ] Adicionar notificações por email
- [ ] Integração com Google Calendar
- [ ] Modo dark theme
- [ ] Exportar relatórios em PDF

### Customização:
- Alterar cores no CSS
- Adicionar logo personalizado
- Modificar dados iniciais
- Adicionar novos campos

---

## 📞 Suporte

**Problemas com Supabase:**
- [Documentação Supabase](https://supabase.com/docs)
- [Discord Supabase](https://discord.supabase.com)

**Problemas com Streamlit:**
- [Documentação Streamlit](https://docs.streamlit.io)
- [Fórum Streamlit](https://discuss.streamlit.io)

**Problemas com este projeto:**
- Abra uma [issue no GitHub](https://github.com/douglas-s29/casamento_streamlit/issues)

---

## ✅ Checklist Final

- [ ] Projeto Supabase criado
- [ ] Credenciais copiadas
- [ ] Tabelas criadas no Supabase
- [ ] Dados iniciais inseridos
- [ ] App testado localmente
- [ ] Secrets configurados localmente
- [ ] Código commitado no GitHub
- [ ] App deployado no Streamlit Cloud
- [ ] Secrets configurados na cloud
- [ ] App em produção testado
- [ ] URL compartilhada

**🎊 Parabéns! Seu sistema de gerenciamento de casamento está no ar!**

---

**Desenvolvido com 💕 para casais organizarem o casamento dos sonhos!**
