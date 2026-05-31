from __future__ import annotations

import pytest
from src.combiner import Combiner
from src.models import QueryConditions


class TestCombiner:
    @pytest.fixture
    def combiner(self):
        return Combiner()

    @pytest.fixture
    def sample_results(self):
        return [
            {"id": i, "name": f"食谱{i}", "category": cat,
             "ingredients": [f"食材{i}"], "effects": ["滋阴"],
             "natures": {"主料": "平"}, "symptoms": [],
             "steps": "", "nutrition": {}, "source": "",
             "scores": {"hybrid": 0.9 - i * 0.1}}
            for i, cat in enumerate(
                ["粥"] * 3 + ["热菜"] * 3 + ["汤羹"] * 3
                + ["甜品"] * 3 + ["饮品"] * 3, 1
            )
        ]

    def test_empty_results_returns_empty_plan(self, combiner):
        plan = combiner.combine([], days=1)
        assert "note" in plan
        assert plan.get("note") == "未找到匹配食谱"

    def test_plan_has_correct_day_count(self, combiner, sample_results):
        plan = combiner.combine(sample_results, days=3)
        assert len(plan["days"]) == 3

    def test_plan_has_meals(self, combiner, sample_results):
        plan = combiner.combine(sample_results, days=1)
        day = plan["days"][0]
        assert len(day["meals"]) > 0
        meal_names = [m["meal"] for m in day["meals"]]
        assert "早餐" in meal_names or "午餐" in meal_names

    def test_recipes_have_required_fields(self, combiner, sample_results):
        plan = combiner.combine(sample_results, days=1)
        for day in plan["days"]:
            for meal in day["meals"]:
                if "recipe" in meal:
                    r = meal["recipe"]
                    assert "id" in r
                    assert "name" in r
                elif "recipes" in meal:
                    for r in meal["recipes"]:
                        assert "id" in r
                        assert "name" in r
