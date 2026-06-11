from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from core.config import Config


class Client:
    def __init__(self, config: Config):
        self.config: Config = config
        self.embedding: OllamaEmbedding = self.embedding_model()
        self.client: QdrantClient = self.qdrant_client()
        self.vector_store: QdrantVectorStore = self.qdrant_vector_store()

    def embedding_model(self) -> OllamaEmbedding:

        return OllamaEmbedding(
            model_name=self.config.embedding.model_name,
            base_url=self.config.embedding.base_url,
        )

    def qdrant_client(self) -> QdrantClient:
        return QdrantClient(url=self.config.qdrant.url)

    def qdrant_vector_store(self) -> QdrantVectorStore:
        return QdrantVectorStore(
            client=self.client, collection_name=self.config.qdrant.collection_name
        )
