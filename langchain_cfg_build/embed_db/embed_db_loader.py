from dataclasses import dataclass

from langchain_core.vectorstores import VectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector


@dataclass
class EmbedDbLoader:
    connection: str = None
    collection_name: str = None
    table_name: str = None  # Custom table name
    content_column: str = "text"  # Custom content column name
    _db: VectorStore = None

    def load(self) -> VectorStore:
        if not self._db:
            self._db = self._load()
        return self._db

    def _load(self) -> VectorStore:
        embeddings = OpenAIEmbeddings()
        pgvector_store = PGVector(
            collection_name=self.collection_name,
            connection=self.connection,
            embeddings=embeddings,
            table_name=self.table_name
        )
        return pgvector_store
