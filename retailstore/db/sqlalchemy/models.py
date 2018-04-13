from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship

from retailstore.db.sqlalchemy.base import BaseModel


Base = declarative.declarative_base()

class Location(Base, BaseModel):
    __tablename__ = 'locations'
    name = Column(String(36), unique=True)
    departments = relationship("Department")


class Department(Base, BaseModel):
    __tablename__ = 'departments'

    name = Column(String(36), unique=True)
    location_id = Column(
        Integer,
        ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=False)
