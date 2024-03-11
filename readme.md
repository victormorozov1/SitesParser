## Run service
With docker:
```commandline
docker-compose -f docker/dev/docker-compose.yml up
```

With docker only for postgres 
```commandline
docker-compose -f docker/dev/docker-compose.yml start postgres
export pg_host=localhost
export pg_port=13000
cd parser
pip3 install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 80
```

You can use the already deployed service at the address 62.84.118.27

## Usage Examples
1) Create parse rule:
POST to http://62.84.118.27/create_rule with body:
```json
{
    "endpoint_data": {
        "url": "https://habr.com/ru/feed/",
        "headers": {},
        "params": {}
    },
    "parsers_datas": [
        {
            "parser_type": "BS4_PARSER",
            "parser_params": {
                "list_input": false,
                "linerize_result": true,
                "name": "h2",
                "search_by_attrs": {"class": "tm-title tm-title_h2"},
                "output_attrs": ["text"],
                "only_values": true
            }
        }
    ]
}
```
you will recive created rule id - remember it for the next step
2)  Parse site with created rule: GET http://62.84.118.27/parse?rule_id=<id_from_previous_step>
Responce:
```json
[
    "Что делать если кончается топливо, а заправки все нет и нет, как на новой трассе Москва-СПб",
    "Как AI помогает побороть монополию в спортивной рекламе и при чем тут GPU и выделенные серверы",
    "Как написать свою маленькую ОС",
    ...
]
```

## Parsers
To create a suitable HTML parsing rule, 
use combinations of parsers 
(they can be found in the folder parser/app/parsers). 
For example, if I want to modify the previous example so that it only returns 
the article about Python, you can add a regexp parser in your rule:
```json
{
    "parser_type": "REGEXP_PARSER",
    "parser_params": {
        "regexp": ".*Py.*",
        "parser_type": "FIND_ALL",
        "list_input": true,
        "linerize_result": true
    }
}
```

Full json:
```json
{
    "endpoint_data": {
        "url": "https://habr.com/ru/feed/",
        "headers": {},
        "params": {}
    },
    "parsers_datas": [
        {
            "parser_type": "BS4_PARSER",
            "parser_params": {
                "list_input": false,
                "linerize_result": true,
                "name": "h2",
                "search_by_attrs": {"class": "tm-title tm-title_h2"},
                "output_attrs": ["text"],
                "only_values": true
            }
        },
        {
            "parser_type": "REGEXP_PARSER",
            "parser_params": {
                "regexp": ".*Py.*",
                "parser_type": "FIND_ALL",
                "list_input": true,
                "linerize_result": true
            }
        }
    ]
}
```

## Run tests

1) Run test database 
```commandline
docker run -e POSTGRES_DB="test_db" -e POSTGRES_USER="test_user" -e POSTGRES_PASSWORD="test_password" -p 2345:5432 -d postgres:15
```
2) Set env vars
```commandline
pg_db_name=test_db;pg_host=localhost;pg_password=test_password;pg_port=2345;pg_user=test_user
```
3) Set workdir: ```parser```
4) Run tests!
