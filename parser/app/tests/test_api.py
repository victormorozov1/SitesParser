from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from app.api import app


client = TestClient(app)


def test_create_regexp_parser_endpoint(mocker: MockFixture) -> None:
    create_regexp_parser = mocker.patch('app.api.create_regexp_parser', return_value=4)
    response = client.post('/create_regexp_parser', json={'regexp': 'some_regexp', 'parser_type': 'GROUP'})
    assert response.status_code == 200
    assert response.json() == {'created_id': 4}
    create_regexp_parser.assert_called_once_with('some_regexp', 'GROUP')

    create_regexp_parser.side_effect = ValueError('Ужасная ошибка!')
    response = client.post('/create_regexp_parser', json={'regexp': 'some_regexp', 'parser_type': 'pipi'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Ужасная ошибка!'}


def test_create_bs4_parser_endpoint(mocker: MockFixture) -> None:
    create_bs4_parser = mocker.patch('app.api.create_bs4_parser', return_value=8)
    response = client.post(
        '/create_bs4_parser',
        json={'name': 'tag', 'search_by_attrs': {'style': 'red', 'title': 'kaka'}, 'output_attrs': ['text', 'bebra']},
    )
    assert response.status_code == 200
    assert response.json() == {'created_id': 8}
    create_bs4_parser.assert_called_once_with('tag', {'style': 'red', 'title': 'kaka'}, ['text', 'bebra'])


def test_create_parser_endpoint(mocker: MockFixture) -> None:
    create_parser = mocker.patch('app.api.create_parser', return_value=9)
    response = client.post(
        '/create_parser',
        json={
            'parser_type': 'RegexpParser',
            'list_input': False,
            'linerize_result': True,
            'parser_params': {'a': 1, 'b': '2'},
        },
    )
    assert response.status_code == 200
    assert response.json() == {'created_id': 9}
    create_parser.assert_called_once_with('RegexpParser', False, True, {'a': 1, 'b': '2'})


def test_create_endpoint_endpoint(mocker: MockFixture) -> None:
    create_endpoint = mocker.patch('app.api.create_endpoint', return_value=10)
    response = client.post(
        '/create_endpoint', json={'url': 'https://aboba.com', 'params': {'page': 2, 'kek': 'lol'}},
    )
    assert response.status_code == 200
    assert response.json() == {'created_id': 10}
    create_endpoint.assert_called_once_with('https://aboba.com', {}, {'page': 2, 'kek': 'lol'})


def test_create_rule_endpoint(mocker: MockFixture) -> None:
    create_rule = mocker.patch('app.api.create_rule', return_value=11)
    response = client.post('/create_rule', json={'endpoint_id': 3, 'parsers_datas': {'some': 'data'}})
    assert response.status_code == 200
    assert response.json() == {'created_id': 11}
    create_rule.assert_called_once_with(3, None, None, {'some': 'data'})


def test_parse_endpoint(mocker: MockFixture) -> None:
    process_rule = mocker.patch('app.api.process_rule', return_value={'some': 'data'})
    response = client.get('/parse', params={'rule_id': 69})
    assert response.json() == {'some': 'data'}
    process_rule.assert_called_once_with(69)
