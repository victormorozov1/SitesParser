from fastapi import FastAPI, Request, Response, status

from app.logic.db_client import create_regexp_parser

app = FastAPI()


@app.post('/create_regexp_parser')
async def create_regexp_parser_endpoint(request: Request, response: Response):
    try:
        return {'created_id': create_regexp_parser(request.headers.get('regexp'), request.headers.get('parser_type'))}
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': str(e)}
