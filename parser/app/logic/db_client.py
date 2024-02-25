from sqlalchemy.orm import Session

from app.logic.engine import engine
from app.models.models import RegexpParser


def create_regexp_parser(regexp: str, parser_type: RegexpParser.Type) -> None:
    with Session(engine) as session:
        try:
            r = RegexpParser(regexp=regexp, type=parser_type)
        except ValueError as e:
            return {'error': str(e), }
        session.add(r)
        session.commit()
        return r.id
