from oslo_db.sqlalchemy import models
from oslo_utils import timeutils
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    orm,
)

from retailstore.errors import ResourceNotFound
from retailstore.db.sqlalchemy.query_generator import QueryGenerator


class BaseModel(models.ModelBase, models.TimestampMixin):
    """Base class for Retail Store Models."""

    __table_args__ = {'mysql_engine': 'Postgre', 'mysql_charset': 'utf8'}
    __table_initialized__ = False
    __protected_attributes__ = set([
        "created_at", "updated_at", "deleted_at", "deleted"])

    id = Column(Integer, primary_key=True)
    name = Column(String(36), unique=True)
    description = Column(Text())
    created_at = Column(DateTime, default=lambda: timeutils.utcnow(),
                        nullable=False)
    updated_at = Column(DateTime, default=lambda: timeutils.utcnow(),
                        nullable=True, onupdate=lambda: timeutils.utcnow())
    deleted_at = Column(DateTime, nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)

    @classmethod
    def _fetch_resources_query(cls, session, **kwargs):
        qg = QueryGenerator(cls, session, **kwargs)
        return qg.resources_query()

    @classmethod
    def _fetch_resource_query(cls, session, **kwargs):
        qg = QueryGenerator(cls, session, **kwargs)
        return qg.resource_query()

    @classmethod
    def fetch_resources(cls, session, **kwargs):
        query = cls._fetch_resources_query(session, **kwargs)
        return query.all()

    @classmethod
    def fetch_resource(cls, session, **kwargs):
        query = cls._fetch_resource_query(session, **kwargs)

        try:
            return query.one()
        except orm.exc.NoResultFound:
            raise ResourceNotFound(message='this is my message, make it btter')
