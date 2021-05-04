from app.db.base import Base
from app.core.config import settings
from logging.config import fileConfig
import logging
import os

from sqlalchemy import engine_from_config, create_engine, pool
from psycopg2 import DatabaseError

from alembic import context


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError(
            "Running testing migrations offline currently not permitted.")
    context.configure(url=str(settings.SQLALCHEMY_DATABASE_URI),
                      target_metadata=target_metadata,
                      literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    DB_URL = f"{settings.SQLALCHEMY_DATABASE_URI}_test" if os.environ.get(
        "TESTING") else str(settings.SQLALCHEMY_DATABASE_URI)
    # handle testing config for migrations
    if os.environ.get("TESTING"):
        # connect to primary db
        default_engine = create_engine(
            str(settings.SQLALCHEMY_DATABASE_URI), isolation_level="AUTOCOMMIT")
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {settings.POSTGRES_DB}_test")
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
