class UnknownParserType(Exception):
    def __init__(self, parser_type: str) -> None:
        super().__init__(f'Unknown parser type: {parser_type}')
