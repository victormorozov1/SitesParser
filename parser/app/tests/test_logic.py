from fastapi.testclient import TestClient
from requests_mock import Mocker
from sqlalchemy.orm import Session

from app.api import app
from app.logic.db_client import create_regexp_parser
from app.models.models import RegexpParser
from app.logic.engine import engine


class TestDbClient:
    def test_create_regexp_parser(self) -> None:
        create_regexp_parser('some_regexp', 'GROUP')
        with Session(engine) as session:
            parsers = session.query(RegexpParser)
            assert parsers.count() == 1
            parser = parsers.one()
            assert parser.regexp == 'some_regexp'
            assert parser.type == 'GROUP'
