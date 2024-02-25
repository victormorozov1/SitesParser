import pytest

from app.logic.engine import engine
from app.models.models import DeclarativeBase


@pytest.fixture(autouse=True)
def mock_connection_string(monkeypatch) -> None:
    monkeypatch.setenv('pg_user', 'test_user')
    monkeypatch.setenv('pg_password', 'test_password')
    monkeypatch.setenv('pg_host', 'localhost')
    monkeypatch.setenv('pg_port', '2345')
    monkeypatch.setenv('pg_user', 'test_user')
    monkeypatch.setenv('pg_db_name', 'test_name')


@pytest.fixture(autouse=True)
def clear_and_migrate():
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)


