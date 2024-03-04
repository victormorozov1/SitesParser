from fastapi import FastAPI, Request, Response, status

from app.logic.db_client import create_bs4_parser, create_endpoint, create_parser, create_regexp_parser, create_rule

app = FastAPI()


@app.get('/ping')
async def ping_endpoint():
    return {'MINE', 'CRAFT'}


@app.post('/create_regexp_parser')
async def create_regexp_parser_endpoint(request: Request, response: Response):
    data = await request.json()
    if 'regexp' not in data:  # TODO добавить нормальную валидацию полей во все ручки
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Required field "regexp" not found'}
    if 'parser_type' not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Required field "parser_type" not found'}
    try:
        return {'created_id': create_regexp_parser(data['regexp'], data['parser_type'])}
    except ValueError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': str(e)}


@app.post('/create_bs4_parser')
async def create_bs4_parser_endpoint(request: Request):
    data = await request.json()
    return {'created_id': create_bs4_parser(data['name'], data['search_by_attrs'], data['output_attrs'])}


@app.post('/create_parser')
async def create_parser_endpoint(request: Request):
    data = await request.json()
    return {
        'created_id': create_parser(
            data['parser_type'], data['list_input'], data['linerize_result'], data['parser_params'],
        ),
    }


@app.post('/create_endpoint')
async def create_endpoint_endpoint(request: Request):
    data = await request.json()
    return {'created_id': create_endpoint(data['url'], data.get('headers', {}), data.get('params', {}))}


@app.post('/create_rule')
async def create_rule_endpoint(request: Request):
    data = await request.json()
    return {
        'created_id': create_rule(
            data['time_delay'],
            data['send_result_url'],
            data.get('endpoint_id'),
            data.get('endpoint_data'),
            data.get('parsers_ids'),
            data.get('parsers_datas'),
        ),
    }
