from __future__ import annotations
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import app_exception_handler, AppException
from app.user.router import router as auth_router
from app.user.profile_router import router as profile_router
from app.favorite.router import router as favorite_router
from app.constitution.router import router as constitution_router
from app.constitution.chat_router import router as chat_router
from app.constitution.trend_router import router as trend_router
from app.content.router import router as content_router
from app.diet.router import router as diet_router
from app.search.router import router as search_router
from app.feedback.router import router as feedback_router
from engine.llm.client import llm_client
from engine.embedding.client import embedding_client
from engine.retrieval.base import chroma_client

from src.models import SearchRequest, PlanRequest
from src.search_engine import SearchEngine
from src.intent_parser import IntentParser
from src.combiner import Combiner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

logger.info("Initializing search engine...")
search_engine = SearchEngine(data_path="data/recipes.json", index_dir="index")
search_engine.initialize()
intent_parser = IntentParser()
combiner = Combiner()
logger.info(f"Ready: {len(search_engine.recipes)} recipes indexed, embedder={'loaded' if search_engine.embedder else 'not available'}")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppException, app_exception_handler)


@app.on_event("startup")
async def startup():
    app.include_router(auth_router)
    app.include_router(profile_router)
    app.include_router(favorite_router)
    app.include_router(constitution_router)
    app.include_router(chat_router)
    app.include_router(trend_router)
    app.include_router(content_router)
    app.include_router(diet_router)
    app.include_router(search_router)
    app.include_router(feedback_router)
    await llm_client.check_availability()
    logger.info(f"LLM client available: {llm_client.available}")
    await chroma_client.initialize()


@app.get("/")
async def root():
    return {
        "service": "中医食补检索系统",
        "version": "0.2.0",
        "phase": "2 - BM25 + BGE嵌入 + 元数据过滤",
        "recipes_indexed": len(search_engine.recipes),
    }


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.post("/search")
async def search(req: SearchRequest):
    conditions = intent_parser.parse(req.query)
    results = search_engine.search(conditions, top_k=req.top_k)
    return {
        "query": req.query,
        "conditions": conditions.model_dump(),
        "total": len(results),
        "results": [
            {
                "id": r["id"],
                "name": r["name"],
                "category": r["category"],
                "constitutions": r["constitutions"],
                "seasons": r["seasons"],
                "effects": r["effects"],
                "symptoms": r["symptoms"],
                "ingredients": r["ingredients"],
                "contraindications": r["contraindications"],
                "scores": r["scores"],
            }
            for r in results
        ],
    }


@app.post("/plan")
async def plan(req: PlanRequest):
    conditions = intent_parser.parse(req.query)
    results = search_engine.search(conditions, top_k=50)
    meal_plan = combiner.combine(results, days=req.days)
    return {
        "query": req.query,
        "conditions": conditions.model_dump(),
        "plan": meal_plan,
    }


@app.get("/recipes")
async def list_recipes():
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "category": r["category"],
            "constitutions": r["constitutions"],
            "seasons": r["seasons"],
        }
        for r in search_engine.recipes
    ]


@app.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipe = search_engine.recipe_ids.get(recipe_id)
    if not recipe:
        return {"error": "Recipe not found"}
    return recipe


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
