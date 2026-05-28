from __future__ import annotations
import random

NATURE_ORDER = {"寒": 0, "凉": 1, "微寒": 1.5, "平": 2, "温": 3, "热": 4}


def _recipe_dominant_nature(recipe: dict) -> str:
    natures = [NATURE_ORDER.get(n, 2) for n in recipe.get("natures", {}).values()]
    if not natures:
        return "平"
    avg = sum(natures) / len(natures)
    if avg <= 0.5:
        return "寒"
    elif avg <= 1.5:
        return "凉"
    elif avg <= 2.5:
        return "平"
    elif avg <= 3.5:
        return "温"
    else:
        return "热"


def _has_ingredient_overlap(recipe_a: dict, recipe_b: dict) -> bool:
    ingredients_a = set(recipe_a.get("ingredients", []))
    ingredients_b = set(recipe_b.get("ingredients", []))
    common = ingredients_a & ingredients_b
    return len(common) >= 2


def _is_nature_balanced(selected: list[dict], candidate: dict) -> bool:
    if not selected:
        return True
    dom_candidate = NATURE_ORDER.get(_recipe_dominant_nature(candidate), 2)
    extremes = 0
    for r in selected:
        n = NATURE_ORDER.get(_recipe_dominant_nature(r), 2)
        if n <= 1 or n >= 3.5:
            extremes += 1
    if (dom_candidate <= 1 or dom_candidate >= 3.5) and extremes >= 2:
        return False
    return True


class Combiner:
    def combine(self, results: list[dict], days: int = 1) -> dict:
        if not results:
            return {"meals": [], "note": "未找到匹配食谱"}

        meal_plan = {"days": []}
        for day in range(days):
            day_meals = self._build_day_plan(results, day)
            meal_plan["days"].append({"day": day + 1, "meals": day_meals})

        return meal_plan

    def _build_day_plan(self, results: list[dict], day: int) -> list[dict]:
        breakfast_pool = self._filter_by_category(results, ["粥"])
        lunch_pool = self._filter_by_category(results, ["热菜", "汤羹"])
        dinner_pool = self._filter_by_category(results, ["汤羹", "粥"])
        snack_pool = self._filter_by_category(results, ["甜品", "饮品"])

        seed = day * 100

        breakfast = self._pick_one(breakfast_pool, seed)
        lunch_main = self._pick_one(lunch_pool, seed + 1)
        lunch_soup = self._pick_one(
            [r for r in lunch_pool if r["id"] != (lunch_main["id"] if lunch_main else -1)],
            seed + 2,
        )
        dinner = self._pick_one(dinner_pool, seed + 3)
        snack = self._pick_one(snack_pool, seed + 4)

        meals = []

        if breakfast:
            meals.append({
                "meal": "早餐",
                "category": "粥品",
                "recipe": self._format_recipe(breakfast),
            })

        lunch_recipes = []
        if lunch_main:
            lunch_recipes.append(lunch_main)
        if lunch_soup and lunch_soup["id"] != (lunch_main["id"] if lunch_main else -1):
            lunch_recipes.append(lunch_soup)

        if lunch_recipes:
            meals.append({
                "meal": "午餐",
                "category": "主食+菜品",
                "recipes": [self._format_recipe(r) for r in lunch_recipes],
            })

        if dinner:
            meals.append({
                "meal": "晚餐",
                "category": "汤羹/轻食",
                "recipe": self._format_recipe(dinner),
            })

        if snack:
            meals.append({
                "meal": "加餐/茶饮",
                "category": "甜品/饮品",
                "recipe": self._format_recipe(snack),
            })

        return meals

    def _filter_by_category(self, results: list[dict], categories: list[str]) -> list[dict]:
        return [r for r in results if r.get("category", "") in categories]

    def _pick_one(self, pool: list[dict], seed: int) -> dict | None:
        if not pool:
            return None
        rng = random.Random(seed)
        return pool[0] if len(pool) == 1 else rng.choice(pool[:5])

    def _format_recipe(self, recipe: dict) -> dict:
        return {
            "id": recipe["id"],
            "name": recipe["name"],
            "category": recipe.get("category", ""),
            "ingredients": recipe.get("ingredients", []),
            "effects": recipe.get("effects", []),
            "natures": recipe.get("natures", {}),
            "symptoms": recipe.get("symptoms", []),
            "steps": recipe.get("steps", ""),
            "nutrition": recipe.get("nutrition", {}),
            "source": recipe.get("source", ""),
            "score": recipe.get("scores", {}).get("hybrid", 0),
        }
