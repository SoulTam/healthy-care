from __future__ import annotations

import pytest
from app.constitution.algorithm import (
    calculate_scores,
    determine_constitution,
    get_severity,
    CONSTITUTIONS,
)


class TestConstitutionAlgorithm:
    def test_all_min_answers_gives_peaceful(self):
        answers = {i: 0 for i in range(1, 11)}
        scores = calculate_scores(answers)
        ctype = determine_constitution(scores)
        assert ctype == "平和质"
        assert scores["平和质"] >= 60

    def test_all_max_answers_gives_biased(self):
        answers = {i: 3 for i in range(1, 11)}
        scores = calculate_scores(answers)
        ctype = determine_constitution(scores)
        assert ctype != "平和质"
        assert scores["平和质"] < 60

    def test_scores_sum_to_reasonable_range(self):
        answers = {i: 1 for i in range(1, 11)}
        scores = calculate_scores(answers)
        for c in CONSTITUTIONS:
            assert 0 <= scores[c] <= 100

    def test_cold_people_get_yang_deficiency(self):
        answers = {
            1: 3, 2: 3, 3: 3, 4: 1, 5: 1,
            6: 1, 7: 1, 8: 1, 9: 1, 10: 1,
        }
        scores = calculate_scores(answers)
        ctype = determine_constitution(scores)
        assert ctype == "阳虚质"

    def test_dry_people_get_yin_deficiency(self):
        answers = {
            1: 3, 2: 1, 3: 1, 4: 3, 5: 1,
            6: 1, 7: 1, 8: 1, 9: 1, 10: 3,
        }
        scores = calculate_scores(answers)
        ctype = determine_constitution(scores)
        assert ctype == "阴虚质"

    def test_severity_levels(self):
        assert get_severity(80) == "重度偏颇"
        assert get_severity(60) == "中度偏颇"
        assert get_severity(40) == "轻度偏颇"
        assert get_severity(20) == "基本正常"

    def test_determine_constitution_returns_highest(self):
        scores = {c: 10 for c in CONSTITUTIONS}
        scores["气虚质"] = 90
        assert determine_constitution(scores) == "气虚质"
