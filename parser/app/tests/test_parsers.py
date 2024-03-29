from contextlib import nullcontext
import pytest
from pytest_mock import MockFixture
from typing import ContextManager

from app.parsers.base_parser import BaseParser, Type, ParserTypeError
from app.parsers.bs4_parser import BS4Parser
from app.parsers.regexp_parsers import DictParser, FindAllParser
from app.parsers.not_empty_parser import NotEmptyParser


class TestBaseParser:
    def test_linerize(self):
        assert list(BaseParser.linerize([1, [2, [3, 4], range(5, 8), 8], (9, 10), 11])) == list(range(1, 12))
        assert list(BaseParser.linerize(1)) == [1]

    @pytest.mark.parametrize(
        'data, expected_type, expectation_context',
        [
            ('s', Type.STRING, nullcontext()),
            (['s', '4'], Type.STRING_LIST, nullcontext()),
            (
                1,
                None,
                pytest.raises(
                    ParserTypeError,
                    match=r'Parsers can only process input types \(list, list\[str\], list\[dict\]\), got 1',
                ),
            ),
            (
                ['1', '2', 1],
                None,
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r"Parsers can only process input types \(list, list\[str\], list\[dict\]\), got \['1', '2', 1\]"
                    )
                ),
            ),
            (
                object,
                None,
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r"Parsers can only process input types "
                        r"\(list, list\[str\], list\[dict\]\), got <class 'object'>"
                    )
                ),
            ),
        ]
    )
    def test_type_from_data(self, data: any, expected_type: Type, expectation_context: ContextManager) -> None:
        with expectation_context:
            assert Type.from_data(data) is expected_type

    @pytest.mark.parametrize(
        'input_types, input_data, expectation_context, list_input, linerize',
        [
            ([Type.STRING], 'ABOBA', nullcontext(), False, False),
            ([Type.STRING_LIST], ['1', 'g', 'fff'], nullcontext(), False, False),
            ([Type.STRING, Type.STRING_LIST], 'some_string', nullcontext(), False, False),
            (
                [Type.STRING],
                ['1', '2', '3'],
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r"Expected that the parser would receive something of \[<str>\] as input, "
                        r"but it received \['1', '2', '3'\]."
                    )
                ),
                False,
                False,
            ),
            (
                [Type.STRING_LIST],
                'keklol',
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r'Expected that the parser would receive something of \[<list\[str\]>\] as input, '
                        r'but it received keklol.'
                    ),
                ),
                False,
                False,
            ),
            (
                [Type.STRING_LIST],
                ['1', 2, 3],
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r"Parsers can only process input types \(list, list\[str\], list\[dict\]\), got \['1', 2, 3\]"
                    )
                ),
                False,
                False,
            ),
            ([Type.STRING], nullcontext(), pytest.raises(ParserTypeError), False, False),
            ([Type.STRING], ['1', '2'], nullcontext(), True, False),
            ([Type.STRING], ['1', '2'], nullcontext(), True, True),
            ([Type.STRING], 'abobus', nullcontext(), False, True),
            (
                [Type.STRING],
                'abobus',
                pytest.raises(
                    ParserTypeError,
                    match=(
                        r'Expected that the parser would receive something of \[<list\[str\]>\] as input, '
                        r'but it received abobus.'
                    )
                ),
                True,
                True,
            ),
        ]
    )
    def test_process(
            self,
            mocker: MockFixture,
            input_types: list[Type],
            input_data: any,
            expectation_context: ContextManager,
            list_input: bool,
            linerize: bool,
    ) -> None:
        main = mocker.patch.object(BaseParser, 'main')
        linerize_mock = mocker.patch.object(BaseParser, 'linerize', return_value=iter([1, 2, 3]))
        parser = BaseParser(input_types, list_input, linerize)
        with expectation_context:
            res = [main.return_value] * 2 if list_input else main.return_value

            if linerize:
                assert parser.process(input_data) == [1, 2, 3]
                linerize_mock.assert_called_once_with(res)
            else:
                assert parser.process(input_data) == res
                linerize_mock.assert_not_called()

            if list_input:
                main.assert_has_calls([mocker.call(i) for i in input_data])
            else:
                main.assert_called_once_with(input_data)


class TestFindAllParser:
    @pytest.mark.parametrize(
        'regexp, input_data, expected_result',
        [
            (
                r'<h1>(?P<header>[\w ]+)</h1>',
                r'aboba ! <h1>Header1</h1><p>\nfndfndsmnf</p><h1>some text</h1>',
                ['Header1', 'some text'],
            ),
            ('\w{1,3}!', 'bebra!', ['bra!']),
            ('amogus', 'Jägermeister', [])
        ]
    )
    def test_findall_parser(self, regexp: str, input_data: str, expected_result: list[str]) -> None:
        parser = FindAllParser(regexp, list_input=False, linerize_result=False)
        assert parser.process(input_data) == expected_result


class TestDictParser:
    @pytest.mark.parametrize(
        'regexp, input_data, expected_result',
        [
            (
                r'<h1>(?P<header1>\w+)<\/h1>\w+<h2>(?P<header2>.*)<\/h2>',
                'курица в перце <h1>trusbl</h1>d<h2>бесплатная</h2>l<h3>Header3</h3>',
                {'header1': 'trusbl', 'header2': 'бесплатная'},
            ),
        ],
    )
    def test_dict_parser(self, regexp: str, input_data: str, expected_result: dict[str, str]) -> None:
        parser = DictParser(regexp, False, False)
        assert parser.process(input_data) == expected_result


class TestBS4Parser:

    @pytest.mark.parametrize(
        'only_values, list_input, linerize_result, expected_result',
        [
            (
                False,
                False,
                False,
                [{'text': 'Какой-то заголовок', 'id': 'first_header'}, {'text': 'Первая секция', 'id': 'super_header'}],
            ),
            (
                True,
                False,
                True,
                ['Какой-то заголовок', 'first_header', 'Первая секция', 'super_header'],
            ),
        ],
    )
    def test_bs4_parser(self, index_html: str, only_values, list_input, linerize_result, expected_result) -> None:
        parser = BS4Parser(
            'h2',
            {'class': 'some_class'},
            ['text', 'id'],
            only_values=only_values,
            list_input=list_input,
            linerize_result=linerize_result,
        )
        assert list(parser.process(index_html)) == expected_result


class TestNotEmptyParser:
    def test_not_empty_parser(self) -> None:
        parser = NotEmptyParser(False, False)
        assert parser.process(['', 's', 'ss']) == ['s', 'ss']
        assert parser.process([{}]) == []
