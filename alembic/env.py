from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.core import settings
from app.db import SQLModel

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    # Convert async URL to sync for offline mode
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")

    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Run migrations in 'online' mode.
    """

    # IMPORTANT:
    # Alembic does NOT support async engines.
    # So we convert asyncpg URL to sync PostgreSQL driver.
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")

    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()