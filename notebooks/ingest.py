import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This file simulates a full ingestion run
    """)
    return


@app.cell
def _():
    # Ingest files from a directory 

    import os 
    from pathlib import Path 
    from datetime import datetime
    from llama_index.core import SimpleDirectoryReader 

    LAST_INGESTION_TIMESTAMP = 0.0
    DOCS_DIR = "./test/sample_dir/"

    # Pre-filter files, only read files that have been modified 
    # i.e. files that were modified after an ingestion run

    modified_files = [
        str(p) for p in Path(DOCS_DIR).rglob("*.md")
        if p.stat().st_mtime > LAST_INGESTION_TIMESTAMP
    ]

    if not modified_files: 
        print("No files were modified since the last ingestion run")

    else: 
        reader = SimpleDirectoryReader(input_files = modified_files)
        documents = reader.load_data() 
    
        __import__(name="pprint").pprint(documents[0].to_dict())
    return (documents,)


@app.cell
def _(documents):
    from llama_index.core.node_parser import MarkdownNodeParser

    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents(documents) 

    for node in nodes: 

        __import__(name="pprint").pprint(node.to_dict())
    return (nodes,)


@app.cell
def _(nodes):
    from llama_index.core import VectorStoreIndex, Settings, StorageContext
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient

    Settings.embed_model = OllamaEmbedding(model_name="qwen3-embedding:4b", base_url="http://localhost:11434")

    client = QdrantClient(location=":memory:")
    vector_store = QdrantVectorStore(client=client, collection_name="obsidian_vault")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(nodes=nodes, storage_context=storage_context)
    return Settings, index


@app.cell
def _(Settings, index):
    from llama_index.llms.ollama import Ollama

    Settings.llm = Ollama(model="qwen3:4b", base_url="http://localhost:11434")

    query_engine = index.as_query_engine()
    response = query_engine.query("What is the main topic?")
    print(response)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
