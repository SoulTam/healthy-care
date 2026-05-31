from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.content.models import KnowledgeChunk, ChunkTag
from app.diet.models import Recipe, RecipeTag
from engine.embedding.client import embedding_client
from engine.retrieval.base import chroma_client

router = APIRouter(prefix="/api/v1/retrieval", tags=["资料入库"])


class IngestRecipeRequest(BaseModel):
    id: str | None = None
    name: str
    category: str
    meal_type: list[str] = []
    ingredients: list[dict] = []
    steps: list[dict] = []
    efficacy: list[str] = []
    nature_flavor: dict = {}
    nutrition: dict = {}
    contraindications: list[str] = []
    source: str | None = None
    source_detail: str | None = None
    tags: list[dict] = []


class IngestKnowledgeRequest(BaseModel):
    content: str
    source: str | None = None
    source_chapter: str | None = None
    chunk_index: int | None = None
    tags: list[dict] = []


class BatchIngestRequest(BaseModel):
    recipes: list[IngestRecipeRequest] = []
    knowledge_chunks: list[IngestKnowledgeRequest] = []


@router.post("/ingest-recipe")
async def ingest_recipe(
    req: IngestRecipeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    recipe_id = uuid.UUID(req.id) if req.id else uuid.uuid4()
    recipe = Recipe(
        id=recipe_id,
        name=req.name,
        category=req.category,
        meal_type=req.meal_type,
        ingredients=req.ingredients,
        steps=req.steps,
        efficacy=req.efficacy,
        nature_flavor=req.nature_flavor,
        nutrition=req.nutrition,
        contraindications=req.contraindications,
        source=req.source,
        source_detail=req.source_detail,
    )
    db.add(recipe)
    for t in req.tags:
        db.add(RecipeTag(
            recipe_id=recipe_id,
            dimension=t.get("dimension", ""),
            tag_value=t.get("tag_value", ""),
        ))

    embedding_text = f"{req.name} {' '.join(req.efficacy)}"
    emb = embedding_client.embed(embedding_text)
    try:
        chroma_client.add_texts(
            "recipes",
            ids=[str(recipe_id)],
            texts=[embedding_text],
            embeddings=[emb],
            metadatas=[{"name": req.name, "category": req.category}],
        )
    except Exception as e:
        pass

    return {"code": "OK", "data": {"id": str(recipe_id)}}


@router.post("/ingest-knowledge")
async def ingest_knowledge(
    req: IngestKnowledgeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    chunk_id = uuid.uuid4()
    chunk = KnowledgeChunk(
        id=chunk_id,
        content=req.content,
        source=req.source,
        source_chapter=req.source_chapter,
        chunk_index=req.chunk_index,
    )
    db.add(chunk)
    for t in req.tags:
        db.add(ChunkTag(
            chunk_id=chunk_id,
            dimension=t.get("dimension", ""),
            tag_value=t.get("tag_value", ""),
        ))

    emb = embedding_client.embed(req.content)
    try:
        chroma_client.add_texts(
            "knowledge",
            ids=[str(chunk_id)],
            texts=[req.content],
            embeddings=[emb],
            metadatas=[{"source": req.source or ""}],
        )
    except Exception as e:
        pass

    return {"code": "OK", "data": {"id": str(chunk_id)}}


@router.post("/ingest/batch")
async def batch_ingest(
    req: BatchIngestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    results = {"recipes": [], "knowledge_chunks": []}
    for r in req.recipes:
        res = await ingest_recipe(r, db, current_user)
        results["recipes"].append(res["data"])
    for k in req.knowledge_chunks:
        res = await ingest_knowledge(k, db, current_user)
        results["knowledge_chunks"].append(res["data"])
    return {"code": "OK", "data": results}


@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
):
    recipe_count = await db.execute(sa_func.count(Recipe.id).select())
    chunk_count = await db.execute(sa_func.count(KnowledgeChunk.id).select())

    tag_query = await db.execute(
        select(RecipeTag.dimension, sa_func.count(RecipeTag.id))
        .group_by(RecipeTag.dimension)
    )

    return {
        "code": "OK",
        "data": {
            "recipes": recipe_count.scalar() or 0,
            "knowledge_chunks": chunk_count.scalar() or 0,
            "chroma_collections": chroma_client.list_collections(),
            "tag_coverage": {
                row[0]: row[1] for row in tag_query.all()
            },
        },
    }
