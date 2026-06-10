import tomllib
from typing import Any

from pydantic import BaseModel, ConfigDict


class IngestionConfig(BaseModel):
    src_dir: str
    state_file: str


class EmbeddingConfig(BaseModel):
    model_name: str
    base_url: str


class QdrantConfig(BaseModel):
    url: str
    collection_name: str


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)  # type: ignore[misc]

    ingestion: IngestionConfig
    embedding: EmbeddingConfig
    qdrant: QdrantConfig

    @classmethod
    def load(cls, path: str = "config.toml") -> "Config":
        with open(file=path, mode="rb") as f:
            raw: dict[str, Any] = tomllib.load(f)  # type: ignore[assignment]
        return cls.model_validate(obj=raw)
