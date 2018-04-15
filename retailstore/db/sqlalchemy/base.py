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

    DataMapper = {
        'locations': 'location_id',
        'departments': 'department_id',
        'categories': 'category_id',
        'sub_categories': 'sub_category_id',
    }

    @classmethod
    def _fetch_resources_query(cls, session, **kwargs):
        query = session.query(cls)

        for join_model in cls.join_models:
            query = query.join(join_model)

        condition = []
        for model in cls.join_models:
            key = cls.DataMapper[model.__tablename__]
            condition.append(getattr(model, 'id') == kwargs[key])

        return query.filter(*condition)

    @classmethod
    def fetch_resources(cls, session, **kwargs):
        query = cls._fetch_resources_query(session, **kwargs)
        return query.all()

    @classmethod
    def fetch_resource(cls, session, **kwargs):
        query = cls._fetch_resources_query(session, **kwargs)

        try:
            return query.filter(cls.id == kwargs['id']).one()
        except orm.exc.NoResultFound:
            raise ResourceNotFound(message='this is my message, make it btter')
