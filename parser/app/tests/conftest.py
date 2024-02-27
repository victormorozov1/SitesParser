import pytest

from app.logic.engine import engine
from app.models.models import DeclarativeBase


@pytest.fixture(autouse=True)
def clear_and_migrate():
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)


@pytest.fixture
def index_html():
    with open('app/tests/index.html', 'r') as f:
        return f.read()
