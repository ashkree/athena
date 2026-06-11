from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama

from core.clients import Client
from core.config import Config


def query(config: Config, clients: Client, question: str):

    llm = Ollama(
        model=config.llm.model_name,
        base_url=config.llm.url,
        context_window=config.llm.context_window,
        request_timeout=config.llm.request_timeout,
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=clients.vector_store, embed_model=clients.embedding
    )

    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=3,  # only fetch 3 chunks instead of default 2 (adjustable)
        streaming=False,
    )

    return query_engine.query(question)
