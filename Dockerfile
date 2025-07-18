# Etapa 1: imagem base com Python
FROM python:3.13-slim

# Etapa 2: instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential curl libpq-dev gcc

# Etapa 3: instalar Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Etapa 4: definir diretório da aplicação
WORKDIR /app

# Etapa 5: copiar arquivos necessários
COPY pyproject.toml poetry.lock ./
COPY . .

# Etapa 6: instalar dependências
RUN poetry install --no-root

# Etapa 7: expor porta
EXPOSE 7000

# Etapa 8: comando de execução
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]
