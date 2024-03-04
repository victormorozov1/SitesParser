from pytest_mock import MockFixture
from sqlalchemy.orm import Session

from app.logic import db_client
from app.models.models import Endpoint, BS4Parser, Parser, RegexpParser, Rule
from app.logic.engine import engine


class TestDbClient:
    def test_create_regexp_parser(self, clear_and_migrate) -> None:
        assert db_client.create_regexp_parser('some_regexp', 'DICT') == 1
        with Session(engine) as session:
            parsers = session.query(RegexpParser)
            assert parsers.count() == 1
            parser = parsers.one()
            assert parser.regexp == 'some_regexp'
            assert parser.type == 'DICT'

    def test_create_bs4_parser(self, clear_and_migrate) -> None:
        assert db_client.create_bs4_parser(
            'h1', {'attr1': 'val1', 'attr2': 'val2'}, ['test', 'keks'],
        ) == 1
        with Session(engine) as session:
            parsers = session.query(BS4Parser)
            assert parsers.count() == 1
            parser = parsers.one()
            assert parser.name == 'h1'
            assert parser.search_by_attrs == {'attr1': 'val1', 'attr2': 'val2'}
            assert parser.output_attrs == ['test', 'keks']

    def test_create_parser(self, clear_and_migrate, mocker: MockFixture) -> None:
        mocker.patch.object(db_client, 'create_bs4_parser', return_value=2)
        assert db_client.create_parser(
            'BS4_PARSER', parser_params={'some': 'param'}, linerize_result=True, list_input=False,
        ) == 1
        db_client.create_bs4_parser.assert_called_once_with(some='param')  # noqa

        mocker.patch.object(db_client, 'create_regexp_parser', return_value=3)
        assert db_client.create_parser(
            'REGEXP_PARSER', parser_params={'kaka': 'some_name'}, linerize_result=False, list_input=True,
        ) == 2
        db_client.create_regexp_parser.assert_called_once_with(kaka='some_name')  # noqa

        with Session(engine) as session:
            actual_parser_1 = session.query(Parser).filter(Parser.id == 1).one()
            assert actual_parser_1.parser_type == 'BS4_PARSER'
            assert actual_parser_1.parser_id == 2
            assert actual_parser_1.linerize_result
            assert not actual_parser_1.list_input

            actual_parser_2 = session.query(Parser).filter(Parser.id == 2).one()
            assert actual_parser_2.parser_type == 'REGEXP_PARSER'
            assert actual_parser_2.parser_id == 3
            assert not actual_parser_2.linerize_result
            assert actual_parser_2.list_input

    def test_create_endpoint(self) -> None:
        assert db_client.create_endpoint(
            'https://abibo.ru', {'header1': 'val1', 'popa': 'popa'}, {'p1': 'v1', 'p2': 'v2'},
        ) == 1
        with Session(engine) as session:
            endpoint = session.query(Endpoint).one()
            assert endpoint.url == 'https://abibo.ru'
            assert endpoint.headers == {'header1': 'val1', 'popa': 'popa'}
            assert endpoint.params == {'p1': 'v1', 'p2': 'v2'}

    def test_create_rule(self) -> None:
        session = Session(engine)
        with session:
            session.add(Endpoint(url='aboba.http'))
            session.add(Parser(parser_type='REGEXP_PARSER', parser_id=1))
            session.add(Parser(parser_type='BS4_PARSER', parser_id=1))
            session.commit()

        assert db_client.create_rule(
            time_delay=9,
            send_result_url='https://pochta.rossii',
            endpoint_id=1,
            parsers_ids=[1, 2],
        ) == 1

        with session:
            rule = session.query(Rule).filter(Rule.id == 1).one()
            assert rule.time_delay == 9
            assert rule.send_result_url == 'https://pochta.rossii'
            assert rule.endpoint.id == 1
            assert [p.id for p in rule.parsers] == [1, 2]