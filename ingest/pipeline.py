import json
import time
from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser

from core.clients import Client
from core.config import Config

# public interface


def ingest(config: Config, clients: Client):

    SRC_DIR = config.ingestion.src_dir
    LAST_INGESTION_TIMESTAMP = read_last_ingestion_timestamp(
        config.ingestion.state_file
    )

    modified_files = [
        str(p)
        for p in Path(SRC_DIR).rglob("*.md")
        if p.stat().st_mtime > LAST_INGESTION_TIMESTAMP
    ]

    # early return if no files were modified
    if not modified_files:
        print("No files modified since last ingestion run")
        return

    # log the time here
    write_last_ingestion_timestamp(config.ingestion.state_file, time.time())

    reader = SimpleDirectoryReader(input_files=modified_files)

    pipeline = IngestionPipeline(
        transformations=[MarkdownNodeParser(), clients.embedding],
        vector_store=clients.vector_store,
    )

    _ = pipeline.run(documents=reader.load_data())

    return


# helpers
def read_last_ingestion_timestamp(path: str) -> float:
    if not Path(path).exists():
        write_last_ingestion_timestamp(path, 0.0)
    with open(path, "r") as f:
        return json.load(f).get("last_ingestion_timestamp", 0.0)


def write_last_ingestion_timestamp(path: str, value: float) -> None:
    with open(path, "w") as f:
        json.dump({"last_ingestion_timestamp": value}, f)
