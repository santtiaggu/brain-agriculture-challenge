from alembic import context
from logging.config import fileConfig
import os

# Config Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL do banco (use psycopg2 no Alembic)
DATABASE_URL = os.getenv(
    "DATABASE_URL_SYNC",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/brain_agriculture"
)

def run_migrations_offline():
    """Rodar migrations sem conexão (gera SQL)."""
    context.configure(
        url=DATABASE_URL,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Rodar migrations conectando ao banco."""
    from sqlalchemy import create_engine
    connectable = create_engine(DATABASE_URL)
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
