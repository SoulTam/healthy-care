from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
import uuid


class RecipeTagOut(BaseModel):
    dimension: str
    tag_value: str


class RecipeIngredientOut(BaseModel):
    ingredient_name: str
    amount: str | None = None
    note: str | None = None
    sort_order: int = 0


class RecipeOut(BaseModel):
    id: uuid.UUID
    name: str
    category: str
    meal_type: list = []
    ingredients: list = []
    steps: list = []
    efficacy: list = []
    nature_flavor: dict = {}
    nutrition: dict = {}
    contraindications: list = []
    source: str | None = None
    source_detail: str | None = None
    image_url: str | None = None
    status: str = "published"
    created_at: datetime
    updated_at: datetime
    tags: list[RecipeTagOut] = []
    ingredient_list: list[RecipeIngredientOut] = []
