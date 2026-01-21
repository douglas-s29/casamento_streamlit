-- Tabela items
CREATE TABLE IF NOT EXISTS items (
  id SERIAL PRIMARY KEY,
  item TEXT NOT NULL,
  servico TEXT DEFAULT '',
  preco DECIMAL(10,2) DEFAULT 0.00,
  status TEXT DEFAULT 'Pendente',
  comentarios TEXT DEFAULT '',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela config
CREATE TABLE IF NOT EXISTS config (
  id SERIAL PRIMARY KEY,
  chave TEXT UNIQUE NOT NULL,
  valor DECIMAL(10,2) NOT NULL,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela tasks
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  tarefa TEXT NOT NULL,
  concluida BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Inserir items iniciais (se não existirem)
INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Vestido de noiva', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Vestido de noiva');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Cabelo e maquiagem', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Cabelo e maquiagem');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Roupa do noivo', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Roupa do noivo');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Igreja', 'Igreja Bom Jesus', 800.00, 'Contratado', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Igreja');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Espaço para a festa', 'Chacara Da Maria', 1600.00, 'Contratado', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Espaço para a festa');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Decoração (flores e móveis)', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Decoração (flores e móveis)');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Buffet', 'Marquinhos', 8400.00, 'Contratado', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Buffet');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Doces e bolos', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Doces e bolos');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Fotografia', 'O grande dia - Sá Teles Fotografia', 1780.00, 'Contratado', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Fotografia');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'DJ', '', 0.00, 'Pendente', 'Verificando necessidade'
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'DJ');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Noite de núpcias', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Noite de núpcias');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Site dos noivos', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Site dos noivos');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Documentos do cartório', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Documentos do cartório');

INSERT INTO items (item, servico, preco, status, comentarios) 
SELECT 'Enfeites pista de dança', '', 0.00, 'Pendente', ''
WHERE NOT EXISTS (SELECT 1 FROM items WHERE item = 'Enfeites pista de dança');

-- Inserir config inicial (se não existir)
INSERT INTO config (chave, valor) 
SELECT 'orcamento_maximo', 30000.00
WHERE NOT EXISTS (SELECT 1 FROM config WHERE chave = 'orcamento_maximo');

INSERT INTO config (chave, valor) 
SELECT 'taxa_juros', 0.0035
WHERE NOT EXISTS (SELECT 1 FROM config WHERE chave = 'taxa_juros');

INSERT INTO config (chave, valor) 
SELECT 'numero_meses', 12
WHERE NOT EXISTS (SELECT 1 FROM config WHERE chave = 'numero_meses');

INSERT INTO config (chave, valor) 
SELECT 'valor_inicial', 30000.00
WHERE NOT EXISTS (SELECT 1 FROM config WHERE chave = 'valor_inicial');

-- Inserir tasks iniciais (se não existirem)
INSERT INTO tasks (tarefa, concluida) 
SELECT 'Definir data do casamento', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Definir data do casamento');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher e reservar igreja', true
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher e reservar igreja');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Contratar espaço para festa', true
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Contratar espaço para festa');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Contratar buffet', true
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Contratar buffet');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Contratar fotógrafo', true
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Contratar fotógrafo');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher vestido de noiva', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher vestido de noiva');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher roupa do noivo', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher roupa do noivo');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Contratar decoração', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Contratar decoração');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher doces e bolo', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher doces e bolo');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Decidir sobre DJ/música', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Decidir sobre DJ/música');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Fazer lista de convidados', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Fazer lista de convidados');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher padrinhos e madrinhas', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher padrinhos e madrinhas');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Criar convites', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Criar convites');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Enviar convites', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Enviar convites');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Definir cardápio', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Definir cardápio');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Escolher alianças', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Escolher alianças');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Reservar lua de mel', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Reservar lua de mel');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Providenciar documentos do cartório', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Providenciar documentos do cartório');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Fazer lista de presentes', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Fazer lista de presentes');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Contratar maquiagem e cabelo', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Contratar maquiagem e cabelo');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Definir playlist da festa', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Definir playlist da festa');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Fazer prova do vestido', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Fazer prova do vestido');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Confirmar presença dos convidados', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Confirmar presença dos convidados');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Organizar transporte', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Organizar transporte');

INSERT INTO tasks (tarefa, concluida) 
SELECT 'Preparar cronograma do dia', false
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE tarefa = 'Preparar cronograma do dia');

-- Tabela de categorias
CREATE TABLE IF NOT EXISTS categorias (
  id SERIAL PRIMARY KEY,
  nome TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de orçamentos
CREATE TABLE IF NOT EXISTS orcamentos (
  id SERIAL PRIMARY KEY,
  categoria_id INTEGER REFERENCES categorias(id) ON DELETE CASCADE,
  fornecedor TEXT NOT NULL,
  valor DECIMAL(10,2) NOT NULL,
  telefone TEXT,
  observacao TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Dados iniciais de categorias
INSERT INTO categorias (nome) VALUES
('Buffet'),
('Igreja'),
('Chácara'),
('Decoração'),
('Fotografia'),
('DJ/Música'),
('Vestido de Noiva'),
('Roupa do Noivo'),
('Doces e Bolos'),
('Cabelo e Maquiagem'),
('Convites'),
('Lembrancinhas'),
('Transporte'),
('Lua de Mel'),
('Documentação')
ON CONFLICT (nome) DO NOTHING;
