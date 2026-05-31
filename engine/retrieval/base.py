from __future__ import annotations

import logging
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings

logger = logging.getLogger(__name__)


class ChromaClient:
    def __init__(self, persist_dir: str | None = None):
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        self._client: chromadb.ClientAPI | None = None

    async def initialize(self) -> bool:
        try:
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            logger.info(
                f"ChromaDB initialized at {self.persist_dir}"
            )
            return True
        except Exception as e:
            logger.warning(f"Failed to initialize ChromaDB: {e}")
            return False

    @property
    def client(self) -> chromadb.ClientAPI:
        if self._client is None:
            raise RuntimeError("ChromaDB not initialized")
        return self._client

    def get_or_create_collection(
        self, name: str, metadata: dict[str, str] | None = None
    ) -> chromadb.Collection:
        return self.client.get_or_create_collection(
            name=name, metadata=metadata
        )

    def delete_collection(self, name: str) -> None:
        try:
            self.client.delete_collection(name)
        except ValueError:
            pass

    def list_collections(self) -> list[str]:
        return [c.name for c in self.client.list_collections()]

    def add_texts(
        self,
        collection_name: str,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]] | None = None,
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        collection = self.get_or_create_collection(collection_name)
        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def similarity_search(
        self,
        collection_name: str,
        query_embedding: list[float],
        n_results: int = 10,
        filter: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        collection = self.get_or_create_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter,
        )
        output = []
        if results["ids"]:
            for i, doc_id in enumerate(results["ids"][0]):
                output.append({
                    "id": doc_id,
                    "score": results["distances"][0][i]
                    if results.get("distances")
                    else 0,
                    "document": results["documents"][0][i]
                    if results.get("documents")
                    else "",
                    "metadata": results["metadatas"][0][i]
                    if results.get("metadatas")
                    else {},
                })
        return output

    def count(self, collection_name: str) -> int:
        collection = self.get_or_create_collection(collection_name)
        return collection.count()


chroma_client = ChromaClient()
