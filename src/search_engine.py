from __future__ import annotations
import json
import os
import shutil
import logging
import numpy as np
import jieba
from whoosh.index import create_in, open_dir, exists_in
from whoosh.fields import Schema, TEXT, KEYWORD, STORED, ID
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.analysis import SpaceSeparatedTokenizer, LowercaseFilter

jieba_analyzer = SpaceSeparatedTokenizer() | LowercaseFilter()

def _tokenize(text: str) -> str:
    return " ".join(jieba.cut(text))

from src.models import QueryConditions

logger = logging.getLogger(__name__)


BM25_WEIGHT = 0.35
METADATA_WEIGHT = 0.35
EMBEDDING_WEIGHT = 0.30

CONSTITUTION_MATCH_WEIGHT = 0.40
SEASON_MATCH_WEIGHT = 0.30
SYMPTOM_MATCH_WEIGHT = 0.20
EFFECT_MATCH_WEIGHT = 0.10


class SearchEngine:
    def __init__(self, data_path: str, index_dir: str = "index"):
        self.data_path = data_path
        self.index_dir = index_dir
        self.recipes: list[dict] = []
        self.recipe_ids: dict[int, dict] = {}
        self.ix = None
        self.embedder = None
        self.embeddings: np.ndarray | None = None
        self.embedding_texts: list[str] = []

    def initialize(self) -> None:
        self._load_data()
        self._build_index()
        self._init_embedder()

    def _load_data(self) -> None:
        with open(self.data_path, encoding="utf-8") as f:
            self.recipes = json.load(f)
        self.recipe_ids = {r["id"]: r for r in self.recipes}
        logger.info(f"Loaded {len(self.recipes)} recipes")

    def _build_index(self) -> None:
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)
        os.makedirs(self.index_dir, exist_ok=True)

        schema = Schema(
            id=ID(stored=True, unique=True),
            name=TEXT(stored=True, analyzer=jieba_analyzer),
            category=KEYWORD(stored=True),
            constitutions=KEYWORD(stored=True),
            seasons=KEYWORD(stored=True),
            constitutions_text=TEXT(analyzer=jieba_analyzer),
            seasons_text=TEXT(analyzer=jieba_analyzer),
            ingredients=TEXT(stored=True, analyzer=jieba_analyzer),
            effects=TEXT(stored=True, analyzer=jieba_analyzer),
            symptoms=TEXT(stored=True, analyzer=jieba_analyzer),
            contraindications=TEXT(stored=True, analyzer=jieba_analyzer),
        )

        self.ix = create_in(self.index_dir, schema)
        writer = self.ix.writer()

        for r in self.recipes:
            writer.add_document(
                id=str(r["id"]),
                name=_tokenize(r["name"]),
                category=r["category"],
                constitutions=",".join(r["constitutions"]),
                seasons=",".join(r["seasons"]),
                constitutions_text=_tokenize(" ".join(r["constitutions"])),
                seasons_text=_tokenize(" ".join(r["seasons"])),
                ingredients=_tokenize(" ".join(r["ingredients"])),
                effects=_tokenize(" ".join(r["effects"])),
                symptoms=_tokenize(" ".join(r["symptoms"])),
                contraindications=_tokenize(" ".join(r["contraindications"])),
            )

        writer.commit()
        logger.info(f"Built Whoosh index with {len(self.recipes)} documents")

    def _init_embedder(self) -> None:
        try:
            from fastembed import TextEmbedding
            models = TextEmbedding.list_supported_models()
            bge_models = [m for m in models if "bge" in m.get("model", "").lower() and "zh" in m.get("model", "").lower()]
            model_name = bge_models[0]["model"] if bge_models else None

            if not model_name:
                logger.warning("No suitable BGE model found in fastembed, skipping embedding")
                self.embedder = None
                return

            self.embedder = TextEmbedding(model_name=model_name)
            self._compute_embeddings()
            logger.info(f"Embedder initialized with {model_name}")
        except Exception as e:
            logger.warning(f"Failed to initialize embedder: {e}")
            logger.warning("Falling back to BM25 + metadata only search")
            self.embedder = None

    def _compute_embeddings(self) -> None:
        if not self.embedder:
            return
        for r in self.recipes:
            text = " ".join([
                r["name"],
                " ".join(r["effects"]),
                " ".join(r["ingredients"]),
                " ".join(r["symptoms"]),
            ])
            self.embedding_texts.append(text)

        embeddings_list = list(self.embedder.passage_embed(self.embedding_texts))
        self.embeddings = np.array(embeddings_list)
        logger.info(f"Computed embeddings with shape {self.embeddings.shape}")

    def search(self, conditions: QueryConditions, top_k: int = 20) -> list[dict]:
        if not self.ix:
            return []

        bm25_results = self._bm25_search(conditions, top_k=top_k * 2)
        bm25_ids = {recipe_id for recipe_id, _ in bm25_results}
        bm25_scores = {recipe_id: score for recipe_id, score in bm25_results}
        scored = []

        for recipe in self.recipes:
            rid = str(recipe["id"])
            bm25_score = bm25_scores.get(rid)
            meta_score = self._compute_metadata_score(recipe, conditions)
            emb_score = self._compute_embedding_score(recipe, conditions)

            if bm25_score is None and meta_score == 0:
                continue

            bm25_norm = self._normalize_bm25(bm25_score) if bm25_score is not None else 0.0

            hybrid = BM25_WEIGHT * bm25_norm + METADATA_WEIGHT * meta_score + EMBEDDING_WEIGHT * emb_score

            scored.append({
                **recipe,
                "scores": {
                    "hybrid": round(hybrid, 4),
                    "bm25": round(bm25_norm, 4) if bm25_score is not None else 0,
                    "metadata": round(meta_score, 4),
                    "embedding": round(emb_score, 4),
                },
            })

        scored.sort(key=lambda x: x["scores"]["hybrid"], reverse=True)
        return scored[:top_k]

    def _normalize_bm25(self, score: float | None) -> float:
        if score is None:
            return 0.0
        if score <= 0:
            return 0.0
        return min(score / 3.0, 1.0)

    def _bm25_search(self, conditions: QueryConditions, top_k: int) -> list[tuple[str, float | None]]:
        search_fields = [
            "name", "ingredients", "effects", "symptoms",
            "constitutions_text", "seasons_text",
        ]
        qp = MultifieldParser(search_fields, schema=self.ix.schema, group=OrGroup)

        query_parts = []
        query_parts.extend(conditions.symptoms)
        query_parts.extend(conditions.effects)
        if conditions.seasons:
            query_parts.extend(conditions.seasons)
        if conditions.constitutions:
            query_parts.extend(conditions.constitutions)

        if not query_parts:
            query_parts.extend(conditions.raw_text.split())

        query_text = _tokenize(" ".join(query_parts))

        if not query_text.strip():
            return [(str(r["id"]), None) for r in self.recipes]

        with self.ix.searcher() as searcher:
            query = qp.parse(query_text)
            results = searcher.search(query, limit=top_k)
            return [(r["id"], r.score) for r in results]

    def _compute_metadata_score(self, recipe: dict, conditions: QueryConditions) -> float:
        score = 0.0
        total_weight = 0.0

        if conditions.constitutions:
            c_match = any(c in recipe["constitutions"] for c in conditions.constitutions)
            if c_match:
                score += CONSTITUTION_MATCH_WEIGHT
            total_weight += CONSTITUTION_MATCH_WEIGHT

        if conditions.seasons:
            s_match = any(s in recipe["seasons"] for s in conditions.seasons)
            if s_match:
                score += SEASON_MATCH_WEIGHT
            total_weight += SEASON_MATCH_WEIGHT

        if conditions.symptoms:
            matched_symptoms = sum(1 for s in conditions.symptoms if s in recipe["symptoms"])
            symptom_ratio = matched_symptoms / len(conditions.symptoms)
            score += SYMPTOM_MATCH_WEIGHT * symptom_ratio
            total_weight += SYMPTOM_MATCH_WEIGHT

        if conditions.effects:
            matched_effects = sum(1 for e in conditions.effects if e in recipe["effects"])
            effect_ratio = matched_effects / len(conditions.effects)
            score += EFFECT_MATCH_WEIGHT * effect_ratio
            total_weight += EFFECT_MATCH_WEIGHT

        return score / total_weight if total_weight > 0 else 0.0

    def _compute_embedding_score(self, recipe: dict, conditions: QueryConditions) -> float:
        if self.embeddings is None or self.embedder is None:
            return 0.0

        recipe_idx = self.recipe_ids[recipe["id"]]["id"] - 1
        if recipe_idx < 0 or recipe_idx >= len(self.embeddings):
            return 0.0

        query_text = " ".join([
            *conditions.symptoms,
            *conditions.effects,
            *conditions.seasons,
            *conditions.constitutions,
        ])

        if not query_text.strip():
            return 0.0

        try:
            query_emb_list = list(self.embedder.query_embed([query_text]))
            if not query_emb_list:
                return 0.0
            query_emb = np.array(query_emb_list[0])
            recipe_emb = self.embeddings[recipe_idx]
            sim = float(np.dot(query_emb, recipe_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(recipe_emb) + 1e-10))
            return max(0.0, sim)
        except Exception as e:
            logger.warning(f"Embedding score error: {e}")
            return 0.0
