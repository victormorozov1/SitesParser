from enum import StrEnum
from sqlalchemy import (
    Boolean,
    create_engine,
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.models.fields import Json

DeclarativeBase = declarative_base()


class Endpoint(DeclarativeBase):
    __tablename__ = 'endpoints'

    id = Column(Integer, primary_key=True)
    url = Column('url', String, nullable=False)
    headers = Column(Json, nullable=True)
    params = Column(Json, nullable=True)


class Parser(DeclarativeBase):
    __tablename__ = 'parsers'

    class ParserType(StrEnum):
        REGEXP_PARSER = 'REGEXP_PARSER'
        BS4_PARSER = 'BS4_PARSER'
        NOT_EMPTY_PARSER = 'NOT_EMPTY_PARSER'

    id = Column(Integer, primary_key=True)
    parser_type = Column(postgresql.ENUM(ParserType, name='parser_type'), nullable=False)
    parser_id = Column(Integer, nullable=True)
    rule_id = Column(Integer, ForeignKey('rules.id'))


class Rule(DeclarativeBase):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    endpoint = relationship('Endpoint')
    parsers = relationship('Parser')


class Check(DeclarativeBase):
    __tablename__ = 'checks'

    id = Column(Integer, primary_key=True)
    result = Column(Json, nullable=True)
    rule = Column(Integer, ForeignKey('rules.id'))
    status = Column(postgresql.ENUM('NEW', 'IN_PROGRESS', name='status'), nullable=False)


class BaseParser(DeclarativeBase):
    __abstract__ = True
    list_input = Column(Boolean, default=False)
    linerize_result = Column(Boolean, default=False)


class RegexpParser(BaseParser):
    __tablename__ = 'regexp_parsers'

    class Type(StrEnum):
        DICT = 'DICT'
        FIND_ALL = 'FIND_ALL'

    id = Column(Integer, primary_key=True)
    regexp = Column(String, nullable=False)
    type = Column(postgresql.ENUM(Type, name='type'), nullable=False)


class BS4Parser(BaseParser):
    __tablename__ = 'bs4_parsers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    search_by_attrs = Column(Json, nullable=True)
    output_attrs = Column(postgresql.ARRAY(String), nullable=True)
    only_values = Column(Boolean)


class NotEmptyParser(BaseParser):
    __tablename__ = 'not_empty_parser'

    id = Column(Integer, primary_key=True)
