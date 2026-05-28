from __future__ import annotations
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(title="中医食补检索 API", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "中医食补检索系统",
        "version": "0.2.0",
        "phase": "2 - BM25 + BGE嵌入 + 元数据过滤",
        "recipes_indexed": len(search_engine.recipes),
    }


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
