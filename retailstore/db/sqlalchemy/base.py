from oslo_db.sqlalchemy import models
from oslo_utils import timeutils


from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
)

class BaseModel(models.ModelBase, models.TimestampMixin):
    """Base class for Retail Store Models."""

    __table_args__ = {'mysql_engine': 'Postgre', 'mysql_charset': 'utf8'}
    __table_initialized__ = False
    __protected_attributes__ = set([
        "created_at", "updated_at", "deleted_at", "deleted"])

    created_at = Column(DateTime, default=lambda: timeutils.utcnow(),
                        nullable=False)
    updated_at = Column(DateTime, default=lambda: timeutils.utcnow(),
                        nullable=True, onupdate=lambda: timeutils.utcnow())
    deleted_at = Column(DateTime, nullable=True)
    deleted = Column(Boolean, nullable=False, default=False)
