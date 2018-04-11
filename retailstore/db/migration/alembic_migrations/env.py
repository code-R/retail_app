from alembic import context
from sqlalchemy import create_engine, pool

from retailstore.db.sqlalchemy import models


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

app_config = config

# set the target for 'autogenerate' support
target_metadata = models.BASE.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with either a URL
    or an Engine.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    kwargs = dict()
    if config.database.connection:
        kwargs['url'] = app_config.database.connection
    else:
        kwargs['dialect_name'] = app_config.database.engine
    context.configure(**kwargs)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    import pdb; pdb.set_trace()  # breakpoint bbf1e71a //

    engine = create_engine(
        app_config.database.connection,
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
