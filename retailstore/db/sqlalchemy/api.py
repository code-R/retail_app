from oslo_config import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CONF = cfg.CONF

def _create_engine():
    return create_engine(CONF.database.database_connect_string)

def get_session(engine=None):
    if not engine:
        engine = _create_engine()

    session_klass = sessionmaker(bind=engine)
    return session_klass()
