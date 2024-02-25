import os

env = {
    'pg_user': os.getenv('pg_user'),
    'pg_password': os.getenv('pg_password'),
    'pg_host': os.getenv('pg_host'),
    'pg_port': os.getenv('pg_port'),
    'pg_db_name': os.getenv('pg_db_name'),
}

if None in env.values():
    from dotenv import load_dotenv
    load_dotenv()
    for key in env:
        if env[key] is None:
            env[key] = os.getenv(key)

connection_string = (
    f'postgresql+psycopg2://{env["pg_user"]}:{env["pg_password"]}@{env["pg_host"]}:{env["pg_port"]}/{env["pg_db_name"]}'
)
