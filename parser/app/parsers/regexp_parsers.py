import re

from app.parsers.base_parser import BaseParser, Type


class FindAllParser(BaseParser):
    def __init__(self, regexp: str, list_input: bool, linerize_result: bool = False) -> None:
        self.regexp = re.compile(regexp)
        super().__init__([Type.STRING], list_input, linerize_result=linerize_result)

    def main(self, input_data: str) -> list[str]:
        return self.regexp.findall(input_data)


class DictParser(BaseParser):
    def __init__(self, regexp: str, list_input: bool, linerize_result: bool = False) -> None:
        self.regexp = re.compile(regexp)
        super().__init__([Type.STRING], list_input, linerize_result)

    def main(self, input_data: str) -> dict[str, str]:
        return self.regexp.search(input_data).groupdict()
