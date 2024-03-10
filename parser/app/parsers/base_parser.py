from enum import Enum
from typing import Any, Callable, Iterable


class ParserTypeError(ValueError):
    pass


class Type(Enum):
    STRING = 'str'
    STRING_LIST = 'list[str]'

    @classmethod
    def from_data(cls, data: any) -> 'Type':
        if isinstance(data, str):
            return cls.STRING
        if isinstance(data, list) and all(isinstance(el, str) for el in data):
            return cls.STRING_LIST
        raise ParserTypeError(f'Parsers can only process types list, list[str], got {data}')

    def __repr__(self):
        return f'<{self.value}>'


class BaseParser:
    def __init__(self, input_types: list[Type], list_input: bool, linerize_result: bool = False) -> None:
        self.input_types = input_types
        if list_input:
            self.main = self.list_decorator(self.main)

            # тут нужно перевести все входные типы в списковые, но пока что только 2 типа так что все просто
            self.input_types = [Type.STRING_LIST]

        self.linerize_result = linerize_result

    @classmethod
    def linerize(cls, a: Any) -> Iterable:
        try:
            for i in a:
                yield from cls.linerize(i)
        except TypeError:
            yield a

    @staticmethod
    def list_decorator(func) -> Callable:
        def _wrapper(input_datas: list) -> list:
            return [func(i) for i in input_datas]

        return _wrapper

    def main(self, input_data: Any) -> Any:
        raise NotImplementedError

    def process(self, input_data: any) -> any:
        actual_input_type = Type.from_data(input_data)
        if all(actual_input_type is not input_type_variant for input_type_variant in self.input_types):
            raise ParserTypeError(
                f'Expected that the parser would receive something of {self.input_types} as input, '
                f'but it received {input_data}.',
            )

        res = self.main(input_data)
        if self.linerize_result:
            return self.linerize(res)
        return res

