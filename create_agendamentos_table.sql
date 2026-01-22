-- SQL para criar tabela de agendamentos
CREATE TABLE IF NOT EXISTS agendamentos (
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

-- Índice para busca por data
CREATE INDEX IF NOT EXISTS idx_agendamentos_data ON agendamentos(data);

-- Índice para busca por status
CREATE INDEX IF NOT EXISTS idx_agendamentos_status ON agendamentos(status);
