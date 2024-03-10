from sqlalchemy.orm import Session
from typing import Iterable

from app.logic.engine import engine
from app.logic.errors import UnknownParserType
from app.models.models import BS4Parser, Endpoint, NotEmptyParser, Parser, RegexpParser, Rule


def create_regexp_parser(regexp: str, parser_type: str, list_input: bool, linerize_result: bool) -> int:
    with Session(engine) as session:
        parser = RegexpParser(regexp=regexp, type=parser_type, list_input=list_input, linerize_result=linerize_result)
        session.add(parser)
        session.commit()
        return parser.id


def create_bs4_parser(
        name: str,
        search_by_attrs: dict[str: any],
        output_attrs: list[str],
        only_values: bool,
        list_input: bool,
        linerize_result: bool,
) -> int:
    with Session(engine) as session:
        parser = BS4Parser(
            name=name,
            search_by_attrs=search_by_attrs,
            output_attrs=output_attrs,
            only_values=only_values,
            list_input=list_input,
            linerize_result=linerize_result,
        )
        session.add(parser)
        session.commit()
        return parser.id


def create_not_empty_parser(list_input: bool, linerize_result: bool):
    with Session(engine) as session:
        parser = NotEmptyParser(list_input=list_input, linerize_result=linerize_result)
        session.add(parser)
        session.commit()
        return parser.id


def create_parser(parser_type: Parser.ParserType, parser_params: dict) -> int:
    if parser_type is Parser.ParserType.BS4_PARSER:
        parser_id = create_bs4_parser(**parser_params)
    elif parser_type is Parser.ParserType.REGEXP_PARSER:
        parser_id = create_regexp_parser(**parser_params)
    elif parser_type is Parser.ParserType.NOT_EMPTY_PARSER:  # TODO реализовать более по умному
        parser_id = create_not_empty_parser(**parser_params)
    else:
        raise UnknownParserType(parser_type)

    with Session(engine) as session:
        parser = Parser(parser_type=parser_type, parser_id=parser_id)
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
        endpoint_id: int | None = None,
        endpoint_data: dict | None = None,
        parsers_ids: list[int] | None = None,
        parsers_datas: list[dict] | None = None,
) -> int:
    with Session(engine) as session:
        if not parsers_ids:
            parsers_ids = []
            for parser_data in parsers_datas:
                type_str = parser_data.pop('parser_type')
                parsers_ids.append(create_parser(parser_type=Parser.ParserType(type_str), **parser_data))
        parsers = session.query(Parser).filter(Parser.id.in_(parsers_ids)).all()

        if endpoint_data:
            endpoint_id = create_endpoint(**endpoint_data)

        rule = Rule(endpoint_id=endpoint_id, parsers=parsers)

        session.add(rule)
        session.commit()

        return rule.id


def load_parsers(parsers: list[Parser]) -> Iterable[BS4Parser | RegexpParser]:
    with Session(engine) as session:
        for parser in parsers:
            parser_id: int = parser.parser_id
            if Parser.ParserType(parser.parser_type) is Parser.ParserType.REGEXP_PARSER:
                yield session.query(RegexpParser).filter(RegexpParser.id == parser_id).one()
            elif parser.parser_type is Parser.ParserType.BS4_PARSER:
                yield session.query(BS4Parser).filter(BS4Parser.id == parser_id).one()
            elif parser.parser_type is Parser.ParserType.NOT_EMPTY_PARSER:
                yield session.query(NotEmptyParser).filter(NotEmptyParser.id == parser_id).one()
