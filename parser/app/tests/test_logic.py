from itertools import chain
import pytest
from pytest_mock import MockFixture
from sqlalchemy.orm import Session

from app.logic import db_utils, parse
from app.logic.engine import engine
from app.models.models import (
    Endpoint,
    BS4Parser as BS4ParserModel,
    NotEmptyParser as NotEmptyParserModel,
    Parser,
    RegexpParser as RegexpParserModel,
    Rule,
)
from app.parsers.bs4_parser import BS4Parser
from app.parsers.regexp_parsers import DictParser, FindAllParser

pytest_plugins = ('pytest_asyncio',)


class TestDbUtils:
    def test_create_regexp_parser(self, clear_and_migrate) -> None:
        assert db_utils.create_regexp_parser(
            'some_regexp', 'DICT', list_input=True, linerize_result=True,
        ) == 1
        with Session(engine) as session:
            parser = session.query(RegexpParserModel).one()
            assert parser.regexp == 'some_regexp'
            assert parser.type == 'DICT'
            assert parser.list_input
            assert parser.linerize_result

    def test_create_bs4_parser(self, clear_and_migrate) -> None:
        assert db_utils.create_bs4_parser(
            'h1',
            {'attr1': 'val1', 'attr2': 'val2'},
            ['test', 'keks'],
            list_input=True,
            linerize_result=True,
            only_values=False,
        ) == 1
        with Session(engine) as session:
            parser = session.query(BS4ParserModel).one()
            assert parser.name == 'h1'
            assert parser.search_by_attrs == {'attr1': 'val1', 'attr2': 'val2'}
            assert parser.output_attrs == ['test', 'keks']
            assert parser.list_input
            assert parser.linerize_result
            assert not parser.only_values

    def test_create_parser(self, clear_and_migrate, mocker: MockFixture) -> None:
        mocker.patch.object(db_utils, 'create_bs4_parser', return_value=2)
        assert db_utils.create_parser(Parser.ParserType.BS4_PARSER, parser_params={'some': 'param'}) == 1
        db_utils.create_bs4_parser.assert_called_once_with(some='param')  # noqa

        mocker.patch.object(db_utils, 'create_regexp_parser', return_value=3)
        assert db_utils.create_parser(Parser.ParserType.REGEXP_PARSER, parser_params={'kaka': 'some_name'}) == 2
        db_utils.create_regexp_parser.assert_called_once_with(kaka='some_name')  # noqa

        mocker.patch.object(db_utils, 'create_not_empty_parser', return_value=4)
        assert db_utils.create_parser(
            Parser.ParserType.NOT_EMPTY_PARSER, parser_params={'list_input': True, 'linerize_result': False},
        ) == 3
        db_utils.create_not_empty_parser.assert_called_once_with(list_input=True, linerize_result=False)  # noqa

        with Session(engine) as session:
            actual_parser_1 = session.query(Parser).filter(Parser.id == 1).one()
            assert actual_parser_1.parser_type is Parser.ParserType.BS4_PARSER
            assert actual_parser_1.parser_id == 2

            actual_parser_2 = session.query(Parser).filter(Parser.id == 2).one()
            assert actual_parser_2.parser_type is Parser.ParserType.REGEXP_PARSER
            assert actual_parser_2.parser_id == 3

            actual_parser_3 = session.query(Parser).filter(Parser.id == 3).one()
            assert actual_parser_3.parser_type is Parser.ParserType.NOT_EMPTY_PARSER
            assert actual_parser_3.parser_id == 4

    def test_create_endpoint(self) -> None:
        assert db_utils.create_endpoint(
            'https://abibo.ru', {'header1': 'val1', 'popa': 'popa'}, {'p1': 'v1', 'p2': 'v2'},
        ) == 1
        with Session(engine) as session:
            endpoint = session.query(Endpoint).one()
            assert endpoint.url == 'https://abibo.ru'
            assert endpoint.headers == {'header1': 'val1', 'popa': 'popa'}
            assert endpoint.params == {'p1': 'v1', 'p2': 'v2'}

    def test_create_rule(self, mocker: MockFixture) -> None:
        session = Session(engine)

        with session:
            session.add(Endpoint(url='aboba.http'))
            session.add(Parser(parser_type='REGEXP_PARSER', parser_id=1))
            session.add(Parser(parser_type='BS4_PARSER', parser_id=1))
            session.commit()
        assert db_utils.create_rule(endpoint_id=1, parsers_ids=[1, 2]) == 1
        with session:
            rule = session.query(Rule).filter(Rule.id == 1).one()
            assert rule.endpoint.id == 1
            assert [p.id for p in rule.parsers] == [1, 2]

        create_parser = mocker.patch.object(db_utils, 'create_parser', return_value=2)
        create_endpoint = mocker.patch.object(db_utils, 'create_endpoint', return_value=1)
        assert db_utils.create_rule(
            endpoint_data={'url': 'https://something.ru', 'headers': {}, 'params': {}},
            parsers_datas=[{'parser_type': 'BS4_PARSER', 'some_param_1': 'some_value_1'}]
        ) == 2
        create_parser.assert_has_calls(
            [mocker.call(parser_type=Parser.ParserType.BS4_PARSER, some_param_1='some_value_1')]
        )
        create_endpoint.assert_called_once_with(url='https://something.ru', headers={}, params={})
        with session:
            rule = session.query(Rule).filter(Rule.id == 2).one()
            assert rule.endpoint.id == 1
            assert [p.id for p in rule.parsers] == [2]

    def test_load_parsers(self) -> None:
        with Session(engine) as session:
            common_parsers = [
                Parser(parser_type=Parser.ParserType.BS4_PARSER, parser_id=1),
                Parser(parser_type=Parser.ParserType.BS4_PARSER, parser_id=2),
                Parser(parser_type=Parser.ParserType.REGEXP_PARSER, parser_id=1),
                Parser(parser_type=Parser.ParserType.NOT_EMPTY_PARSER, parser_id=1),
            ]
            typed_parsers = [
                BS4ParserModel(name='p', output_attrs=['style']),
                BS4ParserModel(name='a'),
                RegexpParserModel(regexp='/d+./d+', type=RegexpParserModel.Type.FIND_ALL),
                NotEmptyParserModel(list_input=False, linerize_result=True),
            ]
            for p in chain(typed_parsers, common_parsers):
                session.add(p)
            session.commit()

            for expected_parser, actual_parser in zip(typed_parsers, db_utils.load_parsers(common_parsers)):
                if isinstance(expected_parser, BS4ParserModel):
                    assert isinstance(actual_parser, BS4ParserModel)
                    assert actual_parser.name == expected_parser.name
                    assert actual_parser.output_attrs == expected_parser.output_attrs
                    assert actual_parser.search_by_attrs == expected_parser.search_by_attrs
                elif isinstance(expected_parser, RegexpParserModel):
                    assert isinstance(actual_parser, RegexpParserModel)
                    assert actual_parser.type == expected_parser.type
                    assert actual_parser.regexp == expected_parser.regexp
                elif isinstance(expected_parser, NotEmptyParserModel):
                    assert isinstance(actual_parser, NotEmptyParserModel)
                    assert not actual_parser.list_input
                    assert actual_parser.linerize_result

    def test_create_not_empty_parser(self) -> None:
        assert db_utils.create_not_empty_parser(list_input=True, linerize_result=True) == 1
        with Session(engine) as session:
            parser = session.query(NotEmptyParserModel).one()
            assert parser.list_input
            assert parser.linerize_result


class TestParse:
    def test_init_parsers_from_db_models(self, mocker: MockFixture) -> None:
        load_parsers = mocker.patch(
            'app.logic.parse.load_parsers',
            return_value=[
                BS4ParserModel(
                    name='h1',
                    search_by_attrs={'class': 'kaka'},
                    output_attrs=['text'],
                    list_input=True,
                    linerize_result=False,
                ),
                RegexpParserModel(
                    regexp='kek',
                    type=RegexpParserModel.Type.FIND_ALL,
                    list_input=False,
                    linerize_result=True,
                ),
                RegexpParserModel(
                    regexp='lol',
                    type=RegexpParserModel.Type.DICT,
                    list_input=False,
                    linerize_result=False,
                ),
            ],
        )
        list_decorator = mocker.patch('app.parsers.base_parser.BaseParser.list_decorator')

        start_parsers = [
            Parser(parser_type=Parser.ParserType.BS4_PARSER),
            Parser(parser_type=Parser.ParserType.REGEXP_PARSER),
            Parser(parser_type=Parser.ParserType.REGEXP_PARSER),
        ]
        parsers = list(parse.init_parsers_from_db_models(start_parsers))
        load_parsers.assert_called_once_with(start_parsers)

        assert isinstance(parsers[0], BS4Parser)
        assert parsers[0].name == 'h1'
        assert parsers[0].search_by_attrs == {'class': 'kaka'}
        assert parsers[0].output_attrs == ['text']
        assert not parsers[0].linerize_result
        list_decorator.assert_called_once()

        assert isinstance(parsers[1], FindAllParser)
        assert parsers[1].regexp.pattern == 'kek'
        assert parsers[1].linerize_result

        assert isinstance(parsers[2], DictParser)
        assert parsers[2].regexp.pattern == 'lol'
        assert not parsers[2].linerize_result

    def test_process_parsers_chain(self, mocker: MockFixture) -> None:
        p1 = BS4Parser('p', {}, [], False, False, False)
        p1_process = mocker.patch.object(p1, 'process')
        p2 = DictParser('somereg', False, False)
        p2_process = mocker.patch.object(p2, 'process')

        assert parse.process_parsers_chain([p1, p2], {}) == p2_process.return_value
        p1_process.assert_called_once_with({})
        p2_process.assert_called_once_with(p1_process.return_value)

    @pytest.mark.asyncio
    async def test_process_rule(self, mocker: MockFixture) -> None:
        with Session(engine) as session:
            endpoint = Endpoint(url='https://aaaoooouuuuu', headers={'h1': 'v1'}, params={'p1': 'v1'})
            session.add(endpoint)
            p1, p2 = (
                Parser(parser_type=Parser.ParserType.BS4_PARSER, parser_id=1),
                Parser(parser_type=Parser.ParserType.REGEXP_PARSER, parser_id=2),
            )
            session.add(p1)
            session.add(p2)
            session.commit()
            session.add(Rule(endpoint=endpoint, parsers=[p1, p2]))
            session.commit()

            process_rule = mocker.patch('app.logic.parse.process_rule')

            assert await parse.process_rule(1) == process_rule.return_value
