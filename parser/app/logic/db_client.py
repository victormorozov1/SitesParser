from sqlalchemy.orm import Session

from app.logic.engine import engine
from app.models.models import RegexpParser


def create_regexp_parser(regexp: str, parser_type: str) -> int:
    with Session(engine) as session:
        r = RegexpParser(regexp=regexp, type=parser_type)
        session.add(r)
        session.commit()
        return r.id
