from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.engine import create_engine


dsn = "sqlite:///notes.db"

# `echo=True` - будут выводиться все действия с базой
engine = create_engine(dsn, echo=True)
# `autoflush=False` - убираем автоматическое подтверждение действий.
session = sessionmaker(bind=engine, autoflush=False)


# Декларативная основа для будущего класса
class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # primary_key - первичный ключ таблицы
    # default - автоматическое создание uuid
    # lambda - т.к. uuid - не строка, а объект uuid, а lambda: str вернет строку со значением uuid
    title = Column(String(200), unique=True, nullable=False)
    # unique - уникальность, nullable=False - not null
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


def drop_tables():
    Base.metadata.drop_all(engine)


def create_tables():
    Base.metadata.create_all(engine)
