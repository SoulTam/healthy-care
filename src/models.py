from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    name: str
    category: str
    constitutions: list[str]
    seasons: list[str]
    ingredients: list[str]
    effects: list[str]
    natures: dict[str, str]
    symptoms: list[str]
    contraindications: list[str]
    steps: str
    nutrition: dict[str, float]
    source: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 20


class PlanRequest(BaseModel):
    query: str
    days: int = 1


class QueryConditions(BaseModel):
    constitutions: list[str] = []
    seasons: list[str] = []
    symptoms: list[str] = []
    effects: list[str] = []
    meal_type: Optional[str] = None
    ingredients: list[str] = []
    raw_text: str = ""
