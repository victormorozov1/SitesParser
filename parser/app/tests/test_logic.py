from sqlalchemy.orm import Session

from app.logic.db_client import create_regexp_parser
from app.models.models import RegexpParser
from app.logic.engine import engine


class TestDbClient:
    def test_create_regexp_parser(self, mock_connection_string) -> None:
        create_regexp_parser('some_regexp', 'GROUP')
        with Session(engine) as session:
            parsers = session.query(RegexpParser)
            assert parsers.count() == 1
            parser = parsers.one()
            assert parser.regexp == 'some_regexp'
            assert parser.type == 'GROUP'
