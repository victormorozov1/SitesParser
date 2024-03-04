from sqlalchemy.orm import Session
from typing import Literal

from app.logic.engine import engine
from app.logic.errors import UnknownParserType
from app.models.models import BS4Parser, Endpoint, Parser, RegexpParser, Rule


def create_regexp_parser(regexp: str, parser_type: str) -> int:
    with Session(engine) as session:
        parser = RegexpParser(regexp=regexp, type=parser_type)
        session.add(parser)
        session.commit()
        return parser.id


def create_bs4_parser(name: str, search_by_attrs: dict[str: any], output_attrs: list[str]) -> int:
    with Session(engine) as session:
        parser = BS4Parser(name=name, search_by_attrs=search_by_attrs, output_attrs=output_attrs)
        session.add(parser)
        session.commit()
        return parser.id


def create_parser(
        parser_type: Literal['BS4_PARSER', 'REGEXP_PARSER'],
        list_input: bool,
        linerize_result: bool,
        parser_params: dict,
) -> int:
    if parser_type == 'BS4_PARSER':  # TODO избавиться от хардкода
        parser_id = create_bs4_parser(**parser_params)
    elif parser_type == 'REGEXP_PARSER':
        parser_id = create_regexp_parser(**parser_params)
    else:
        raise UnknownParserType(parser_type)

    with Session(engine) as session:
        parser = Parser(
            parser_type=parser_type, parser_id=parser_id, list_input=list_input, linerize_result=linerize_result,
        )
        session.add(parser)
        session.commit()

        return parser.id


def create_endpoint(url: str, headers: dict, params: dict) -> int:
    with Session(engine) as session:
        e = Endpoint(url=url, headers=headers, params=params)
        session.add(e)
        session.commit()
        return e.id


def create_rule(
        time_delay: int,
        send_result_url: str,
        endpoint_id: int | None = None,
        endpoint_data: dict | None = None,
        parsers_ids: list[int] | None = None,
        parsers_datas: list[dict] | None = None,
) -> int:
    with Session(engine) as session:
        if not parsers_ids:
            parsers_ids = [create_parser(**parser_data) for parser_data in parsers_datas]
        parsers = session.query(Parser).filter(Parser.id.in_(parsers_ids)).all()

        if endpoint_data:
            endpoint_id = create_endpoint(**endpoint_data)

        rule = Rule(time_delay=time_delay, send_result_url=send_result_url, endpoint_id=endpoint_id, parsers=parsers)

        session.add(rule)
        session.commit()

        return rule.id

