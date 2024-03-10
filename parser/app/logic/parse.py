from aiohttp import ClientSession
from sqlalchemy.orm import Session
from typing import Any, Iterable

from app.logic.db_utils import load_parsers
from app.logic.engine import engine
from app.parsers.bs4_parser import BS4Parser
from app.parsers.regexp_parsers import DictParser, FindAllParser
from app.models.models import BS4Parser as BS4ParserModel, Endpoint, Parser, RegexpParser as RegexpParserModel, Rule
from app.parsers.base_parser import BaseParser

ParsersDataType = dict | str | list[dict] | list[str]


def init_parsers_from_db_models(parsers: list[Parser]) -> Iterable[BaseParser]:
    for parser in load_parsers(parsers):
        if isinstance(parser, BS4ParserModel):
            yield BS4Parser(
                parser.name, parser.search_by_attrs, parser.output_attrs, parser.list_input, parser.linerize_result,
            )
        elif isinstance(parser, RegexpParserModel):
            if parser.type is RegexpParserModel.Type.FIND_ALL:
                yield FindAllParser(parser.regexp, parser.list_input, linerize_result=parser.linerize_result)
            elif parser.type is RegexpParserModel.Type.DICT:
                yield DictParser(parser.regexp, parser.list_input, parser.linerize_result)


async def call_endpoint(endpoint_id: int) -> str:
    with Session(engine) as session:
        endpoint = session.query(Endpoint).filter(Endpoint.id == endpoint_id).one()
        async with ClientSession() as http_session:
            response = await http_session.get(endpoint.url, params=endpoint.params, headers={})
            response.raise_for_status()
            return await response.text()


def process_parsers_chain(parsers: Iterable[BaseParser], data: ParsersDataType) -> ParsersDataType:
    for parser in parsers:
        data = parser.process(data)
    return data


async def process_rule(rule_id: int) -> ParsersDataType:
    with Session(engine) as session:
        rule = session.query(Rule).filter(Rule.id == rule_id).one()
        html = await call_endpoint(rule.endpoint_id)
        parsers = init_parsers_from_db_models(rule.parsers)
        return process_parsers_chain(parsers, html)
