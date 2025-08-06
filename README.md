# Brain Agriculture Challenge - API

API REST para cadastro, listagem, edição, exclusão e análise de produtores rurais, suas fazendas e culturas. Desenvolvido com **FastAPI**, utilizando PostgreSQL e arquitetura modular.

## 📦 Tecnologias

- Python 3.13
- FastAPI
- PostgreSQL
- Asyncpg
- Pydantic
- Docker / Docker Compose
- Pytest
- Poetry
- Swagger

---

## 🚀 Como rodar o projeto localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/brain-agriculture-api.git
cd brain-agriculture-api
```

### 2. Criar e ativar ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
poetry install
```

> Caso não tenha o `poetry`, instale com:
> ```bash
> pip install poetry
> ```

---

## 🐘 Como rodar o projeto
```bash
poe start
```

## 🐘 Como rodar com Docker

### 1. Subir o container
```bash
docker-compose up --build
```

### 2. Acessar a API
```bash
http://localhost:7001/api
```

---

## 🧪 Rodando os testes

### Usando Poetry
```bash
poetry run pytest tests/
```

### Usando Pytest diretamente
```bash
pytest tests/
```

---

## 📚 Endpoints principais

| Método | Rota                          | Descrição                    |
|--------|-------------------------------|------------------------------|
| POST   | `/api/producers`              | Cadastrar produtor           |
| POST   | `/api/producers/list`         | Listar produtores paginados  |
| GET    | `/api/producers/{id}`         | Buscar produtor por ID       |
| PUT    | `/api/producers/{id}`         | Atualizar produtor           |
| DELETE | `/api/producers/{id}`         | Remover produtor             |
| GET    | `/api/dashboard`              | Dados para gráficos          |

A documentação Swagger estará disponível em:
```
http://localhost:7001/docs
```

---

## ⚙️ Variáveis de ambiente

Crie um arquivo `.env` na raiz com:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/brain_agriculture
```

> A URL será automaticamente usada tanto em local quanto no container (definido em `docker-compose.yml`).

---

## 🧠 Estrutura do Projeto

```bash
.
├── main.py                 # Entrypoint da aplicação
├── routers/                # Rotas da aplicação
├── services/               # Lógica de negócio
├── repositories/           # Acesso ao banco de dados
├── schemas/                # Schemas Pydantic
├── tests/                  # Testes unitários
├── docker-compose.yml
└── README.md
```

---

## 🧔 Autor

Desenvolvido por **Gustavo Santiago** – contato: gustavoalcantarasantiago@gmail.com

---
