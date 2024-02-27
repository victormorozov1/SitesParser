from fastapi.testclient import TestClient
from pytest_mock import MockFixture

from app.api import app


client = TestClient(app)


def test_create_regexp_parser_endpoint(mocker: MockFixture) -> None:
    create_regexp_parser = mocker.patch('app.api.create_regexp_parser', return_value=4)
    response = client.post('/create_regexp_parser', headers={'regexp': 'some_regexp', 'parser_type': 'GROUP'})
    assert response.status_code == 200
    assert response.json() == {'created_id': 4}
    create_regexp_parser.assert_called_once_with('some_regexp', 'GROUP')

    create_regexp_parser.side_effect = ValueError('Ужасная ошибка!')
    response = client.post('/create_regexp_parser', headers={'regexp': 'some_regexp', 'parser_type': 'pipi'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Ужасная ошибка!'}
