from alembic import op

# Revisão (pode ser qualquer string única, mas vamos manter algo simples)
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        CREATE TABLE producers (
            id SERIAL PRIMARY KEY,
            document VARCHAR(18) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL
        );

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

        CREATE TABLE crops (
            id SERIAL PRIMARY KEY,
            farm_id INTEGER NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
            season VARCHAR(20) NOT NULL,
            name VARCHAR(100) NOT NULL
        );
    """)


def downgrade():
    op.execute("""
        DROP TABLE IF EXISTS crops;
        DROP TABLE IF EXISTS farms;
        DROP TABLE IF EXISTS producers;
    """)
