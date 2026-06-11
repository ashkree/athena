import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo 

    return


app._unparsable_cell(
    r"""
    from qdrant_client import QdrantClient
    from llama_index.core import VectorStoreIndex 
    from llama_index.vector_stores.qdrant import QdrantVectorStore

    client = QdrantClient(host="localhost", port=6333)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="test_store",
    )

    loaded_index = 
    """,
    name="_"
)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
