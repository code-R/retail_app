from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship

from retailstore.db.sqlalchemy.base import BaseModel


Base = declarative.declarative_base()

class Location(Base, BaseModel):
    __tablename__ = 'locations'
    name = Column(String(36), unique=True)
    description = Column(Text())
    departments = relationship("Department")


class Department(Base, BaseModel):
    __tablename__ = 'departments'

    name = Column(String(36), unique=True)
    description = Column(Text())
    location_id = Column(
        Integer,
        ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=False)
    categories = relationship("Category")


class Category(Base, BaseModel):
    __tablename__ = 'categories'

    name = Column(String(36), unique=True)
    description = Column(Text())
    department_id = Column(
        Integer,
        ForeignKey('departments.id', ondelete='CASCADE'),
        nullable=False)
    sub_categories = relationship("SubCategory")


class SubCategory(Base, BaseModel):
    __tablename__ = 'sub_categories'

    name = Column(String(36), unique=True)
    description = Column(Text())
    category_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE'),
        nullable=False)
