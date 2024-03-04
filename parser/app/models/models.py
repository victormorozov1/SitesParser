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

    id = Column(Integer, primary_key=True)
    parser_type = Column(postgresql.ENUM('REGEXP_PARSER', 'BS4_PARSER', name='parser_type'), nullable=False)
    parser_id = Column(Integer)
    rule_id = Column(Integer, ForeignKey('rules.id'))
    list_input = Column(Boolean, default=False)
    linerize_result = Column(Boolean, default=False)


class Rule(DeclarativeBase):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    time_delay = Column(Integer, nullable=False)
    last_check_time = Column(DateTime, nullable=True)
    send_result_url = Column(String, nullable=False)
    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    endpoint = relationship('Endpoint')
    parsers = relationship('Parser')


class Check(DeclarativeBase):
    __tablename__ = 'checks'

    id = Column(Integer, primary_key=True)
    result = Column(Json, nullable=True)
    rule = Column(Integer, ForeignKey('rules.id'))
    status = Column(postgresql.ENUM('NEW', 'IN_PROGRESS', name='status'), nullable=False)


class RegexpParser(DeclarativeBase):
    __tablename__ = 'regexp_parsers'

    id = Column(Integer, primary_key=True)
    regexp = Column(String, nullable=False)
    type = Column(postgresql.ENUM('DICT', 'FIND_ALL', name='type'), nullable=False)


class BS4Parser(DeclarativeBase):
    __tablename__ = 'bs4_parsers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    search_by_attrs = Column(Json, nullable=True)
    output_attrs = Column(postgresql.ARRAY(String), nullable=True)


if __name__ == '__main__':
    from app.logic.connection_string import connection_string
    engine = create_engine(connection_string)
    engine.connect()
    print('Connected!')
    DeclarativeBase.metadata.create_all(engine)
    # from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    # engine = create_engine('sqlite:///notes/notes.db')
    # engine.connect()
    session = Session(engine)
    session.add(BS4Parser(name='a', output_attrs=['1', '2']))
    session.commit()
    from sqlalchemy import text
    print(session.execute(text('SELECT table_name from information_schema.tables')))

    # session.add(BS4Parser(name='a', search_by_attrs={'title': 'home'}, output_attrs={'text': 'aboba'}))
    # session.commit()

    # res = session.query(BS4Parser).one()
    # print(res)