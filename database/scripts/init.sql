DROP TABLE IF EXISTS crops;
DROP TABLE IF EXISTS farms;
DROP TABLE IF EXISTS producers;

-- ========================
-- Tabela: producers
-- ========================
-- Armazena CPF ou CNPJ formatados
-- Exemplo CPF: 123.456.789-09
-- Exemplo CNPJ: 12.345.678/0001-99
CREATE TABLE producers (
    id SERIAL PRIMARY KEY,
    document VARCHAR(18) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL
);

-- ========================
-- Tabela: farms
-- ========================
-- Cada fazenda pertence a um produtor
CREATE TABLE farms (
    id SERIAL PRIMARY KEY,
    producer_id INTEGER NOT NULL REFERENCES producers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    total_area FLOAT NOT NULL CHECK (total_area > 0),
    agricultural_area FLOAT NOT NULL CHECK (agricultural_area >= 0),
    vegetation_area FLOAT NOT NULL CHECK (vegetation_area >= 0),
    CHECK (agricultural_area + vegetation_area <= total_area)
);

-- ========================
-- Tabela: crops
-- ========================
-- Representa culturas plantadas em uma fazenda em determinada safra
CREATE TABLE crops (
    id SERIAL PRIMARY KEY,
    farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    season VARCHAR(20) NOT NULL,   -- Ex: '2022/2023'
    name VARCHAR(100) NOT NULL     -- Ex: 'Soja'
);
