from sqlalchemy import create_engine

from app.logic.connection_string import connection_string

engine = create_engine(connection_string)
engine.connect()
