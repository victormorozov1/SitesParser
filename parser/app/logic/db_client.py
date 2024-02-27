from sqlalchemy.orm import Session

from app.logic.engine import engine
from app.models.models import BS4Parser, RegexpParser


def create_regexp_parser(regexp: str, parser_type: str) -> int:
    with Session(engine) as session:
        r = RegexpParser(regexp=regexp, type=parser_type)
        session.add(r)
        session.commit()
        return r.id


def create_bs4_parser(name: str, search_by_attrs: dict, output_attrs: dict) -> int:
    with Session(engine) as session:
        r = BS4Parser(name=name, search_by_attrs=search_by_attrs, output_attrs=output_attrs)
        session.add(r)
        session.commit()
        return r.id



