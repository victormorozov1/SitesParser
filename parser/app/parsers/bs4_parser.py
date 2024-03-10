from app.parsers.base_parser import BaseParser, Type

from bs4 import BeautifulSoup


class BS4Parser(BaseParser):
    def __init__(
            self,
            name: str,
            search_by_attrs: dict[str, any],
            output_attrs: list[str],
            only_values: bool,
            list_input: bool,
            linerize_result: bool,
    ) -> None:
        self.name = name
        self.search_by_attrs = search_by_attrs
        self.output_attrs = output_attrs
        self.only_values = only_values
        super().__init__([Type.STRING], list_input, linerize_result)

    def main(self, input_data: str) -> list[dict[str, any]]:
        soup = BeautifulSoup(input_data)
        l = []
        for i in soup.find_all(self.name, **self.search_by_attrs):
            res = {}
            for output_attr in self.output_attrs:
                res[output_attr] = getattr(i, output_attr) or i.attrs.get(output_attr)
            if self.only_values:
                l.append(list(res.values()))
            else:
                l.append(res)
        return l
