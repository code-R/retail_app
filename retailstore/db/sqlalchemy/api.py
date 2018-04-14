import os

from oslo_config import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CONF = cfg.CONF

def _create_engine():
    try:
        db_connection = CONF.database.database_connect_string
    except cfg.NoSuchOptError:
        db_connection = os.environ.get('STORE_DB_URL', 'invalid_db_url')

    return create_engine(db_connection)

def get_session(engine=None):
    if not engine:
        engine = _create_engine()

    session_klass = sessionmaker(bind=engine)
    return session_klass()
