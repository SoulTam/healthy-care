from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.models import QueryConditions
from src.search_engine import SearchEngine
from src.intent_parser import IntentParser
from src.combiner import Combiner

router = APIRouter(prefix="/api/v1/diet", tags=["食补方案"])

search_engine = SearchEngine(data_path="data/recipes.json", index_dir="index")
intent_parser = IntentParser()
combiner = Combiner()


class PlanGenerateRequest(BaseModel):
    query: str
    days: int = 1


class PlanReplaceRequest(BaseModel):
    query: str
    current_recipe_id: int
    meal_type: str = ""


@router.get("/health")
async def health():
    search_engine.initialize()
    return {
        "status": "ok",
        "recipes_indexed": len(search_engine.recipes),
    }


@router.post("/plan/generate")
async def generate_plan(req: PlanGenerateRequest):
    search_engine.initialize()
    conditions = intent_parser.parse(req.query)
    results = search_engine.search(conditions, top_k=50)
    plan = combiner.combine(results, days=req.days)
    return {"code": "OK", "data": plan}


@router.post("/plan/replace")
async def replace_recipe(req: PlanReplaceRequest):
    search_engine.initialize()
    conditions = intent_parser.parse(req.query)
    results = search_engine.search(conditions, top_k=50)
    filtered = [r for r in results if r["id"] != req.current_recipe_id]
    if not filtered:
        raise HTTPException(status_code=404, detail="没有可替换的食谱")
    return {"code": "OK", "data": filtered[:5]}
