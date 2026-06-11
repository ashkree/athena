from fastapi import Depends, FastAPI
from pydantic import BaseModel

from core.clients import Client
from core.config import Config
from ingest.pipeline import ingest
from retrieval.pipeline import query

app = FastAPI()


def get_config():
    return Config.load("~/.config/athena/config.toml")


def get_clients(config: Config = Depends(get_config)):
    return Client(config)


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
async def root():
    return {"status": "ok"}


@app.post("/ingest")
async def ingest_directory(
    config: Config = Depends(get_config), clients: Client = Depends(get_clients)
):
    return ingest(config=config, clients=clients)


@app.post("/query")
async def query_directory(
    req: QueryRequest,
    config: Config = Depends(get_config),
    clients: Client = Depends(get_clients),
):

    return query(config=config, clients=clients, question=req.question)
