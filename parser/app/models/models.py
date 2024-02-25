from app.models.json_field import Json
from enum import Enum
from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Integer,
    String,
    DateTime,
    Time,
    Enum as EnumType,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class Endpoint(DeclarativeBase):
    __tablename__ = 'endpoints'

    id = Column(Integer, primary_key=True)
    url = Column('url', String, nullable=False)
    headers = Column(Json, nullable=True)
    params = Column(Json, nullable=True)


class Parser(DeclarativeBase):
    __tablename__ = 'parsers'

    class Type(Enum):
        REGEXP = 'REGEXP'
        BS4 = 'BS4'

    id = Column(Integer, primary_key=True)
    parser_type = Column(EnumType(Type))
    parser_id = Column(Integer)
    rule_id = Column(Integer, ForeignKey('rules.id'))


class Rule(DeclarativeBase):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    time_delay = Column(Time, nullable=False)
    last_check_time = Column(DateTime, nullable=True)
    send_result_url = Column(String, nullable=False)
    endpoint = Column(Integer, ForeignKey('endpoints.id'))
    parsers = relationship('Parser')


class Check(DeclarativeBase):
    __tablename__ = 'checks'

    class Status(Enum):
        NEW = 'NEW'
        IN_PROGRESS = 'IN_PROGRESS'  # TODO не забыть что при перезапуске надо поменять IN_PROGRESS на NEW

    id = Column(Integer, primary_key=True)
    result = Column(Json, nullable=True)
    rule = Column(Integer, ForeignKey('rules.id'))
    status = Column(EnumType(Status), nullable=False)


class RegexpParser(DeclarativeBase):
    __tablename__ = 'regexp_parsers'

    class Type(Enum):
        GROUP = 'GROUP'
        FIND_ALL = 'FIND_ALL'

    id = Column(Integer, primary_key=True)
    regexp = Column(String, nullable=False)
    type = Column(EnumType(Type), nullable=False)


class BS4Parser(DeclarativeBase):
    __tablename__ = 'bs4_parsers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    search_by_attrs = Column(Json, nullable=True)
    output_attrs = Column(Json, nullable=True)


if __name__ == '__main__':
    from app.models.connection_string import connection_string
    engine = create_engine(connection_string)
    engine.connect()
    print('Connected!')
    # DeclarativeBase.metadata.create_all(engine)
    # from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    # engine = create_engine('sqlite:///notes/notes.db')
    # engine.connect()
    session = Session(engine)
    from sqlalchemy import text
    print(session.execute(text('SELECT table_name from information_schema.tables')))

    # session.add(BS4Parser(name='a', search_by_attrs={'title': 'home'}, output_attrs={'text': 'aboba'}))
    # session.commit()

    # res = session.query(BS4Parser).one()
    # print(res)