from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.ext import declarative

from retailstore.db.sqlalchemy.base import BaseModel


Base = declarative.declarative_base()

class Location(Base, BaseModel):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(36), unique=True)
