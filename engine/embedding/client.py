from __future__ import annotations

import logging
import numpy as np

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingClient:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self._model = None
        self._dimension = 384

    @property
    def dimension(self) -> int:
        return self._dimension

    def _ensure_model(self) -> bool:
        if self._model is not None:
            return True
        try:
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(
                self.model_name, device="cpu"
            )
            self._dimension = self._model.get_sentence_embedding_dimension()
            logger.info(
                f"Embedding model loaded, dimension={self._dimension}"
            )
            return True
        except Exception as e:
            logger.warning(f"Failed to load embedding model: {e}")
            logger.warning("Falling back to numpy random embeddings")
            return False

    def embed(self, text: str) -> list[float]:
        self._ensure_model()
        if self._model is None:
            return self._fallback_embed(text)
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        self._ensure_model()
        if self._model is None:
            return [self._fallback_embed(t) for t in texts]
        embeddings = self._model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False
        )
        return embeddings.tolist()

    def _fallback_embed(self, text: str) -> list[float]:
        rng = np.random.RandomState(hash(text) % (2**31))
        vec = rng.randn(self._dimension).astype(np.float32)
        vec = vec / (np.linalg.norm(vec) + 1e-10)
        return vec.tolist()


embedding_client = EmbeddingClient()
