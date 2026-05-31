from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.search_engine import SearchEngine
from src.intent_parser import IntentParser

router = APIRouter(prefix="/api/v1/search", tags=["搜索"])

search_engine = SearchEngine(data_path="data/recipes.json", index_dir="index")
intent_parser = IntentParser()


@router.get("/recipes")
async def search_recipes(
    q: str = Query("", description="搜索关键词"),
    top_k: int = Query(20, ge=1, le=100),
):
    search_engine.initialize()
    conditions = intent_parser.parse(q)
    results = search_engine.search(conditions, top_k=top_k)
    return {
        "code": "OK",
        "data": [
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
        "total": len(results),
    }


@router.get("/global")
async def search_global(
    q: str = Query("", description="全局搜索"),
    top_k: int = Query(20, ge=1, le=100),
):
    search_engine.initialize()
    from src.models import QueryConditions

    conditions = intent_parser.parse(q)
    results = search_engine.search(conditions, top_k=top_k)

    return {
        "code": "OK",
        "data": {
            "recipes": [
                {
                    "id": r["id"],
                    "name": r["name"],
                    "category": r["category"],
                    "type": "recipe",
                }
                for r in results[:10]
            ]
        },
    }


@router.get("/hot")
async def hot_searches():
    return {
        "code": "OK",
        "data": [
            "阴虚质调理", "春季养生", "失眠食疗",
            "健脾祛湿", "补气血", "润肺止咳",
        ],
    }
