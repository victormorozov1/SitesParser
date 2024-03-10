from app.parsers.base_parser import BaseParser, Type


class NotEmptyParser(BaseParser):
    def __init__(self, list_input: bool, linerize_result: bool) -> None:
        super().__init__([Type.STRING_LIST, Type.LIST_DICT], list_input, linerize_result)

    def main(self, input_data: list[str] | list[dict]) -> list[str] | list[dict]:
        return list(filter(bool, input_data))
