import uvicorn as uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/one")
async def one():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.models.connection_string import connection_string
    from app.models.models import Endpoint
    engine = create_engine(connection_string)
    engine.connect()
    session = Session(engine)
    endpoint = Endpoint(url='avito.ru')
    session.add(endpoint)
    session.commit()
    return {"created_id": endpoint.id}


@app.get("/two")
async def two():
    return {"second_root": "two"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
