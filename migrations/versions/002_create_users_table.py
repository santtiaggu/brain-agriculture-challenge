from alembic import op
import bcrypt

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            admin BOOLEAN DEFAULT FALSE NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
            is_deleted BOOLEAN DEFAULT FALSE NOT NULL
        );
    """)

    # Gera hash seguro para a senha
    password = "santiago"
    hash_str = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    op.execute(f"""
        INSERT INTO users (
            id, email, password, first_name, last_name, phone, admin, created_at, updated_at, is_deleted
        ) VALUES (
            1,
            'gustavo.santiago@gmail.com',
            '{hash_str}',
            'Gustavo',
            'Santiago',
            '+5527992033083',
            TRUE,
            CURRENT_TIMESTAMP,
            CURRENT_TIMESTAMP,
            FALSE
        );
    """)


def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS users;
    """)
