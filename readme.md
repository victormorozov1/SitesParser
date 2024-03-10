## Run service
With docker:
```commandline
docker-compose -f docker/dev/docker-compose.yml up
```

With docker only for postgres 
```commandline
docker-compose -f docker/dev/docker-compose.yml start postgres
export pg_host=`ifconfig -u | grep 'inet ' | grep -v 127.0.0.1 | cut -d\  -f2 | head -1`
cd parser
pip3 install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 80
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
