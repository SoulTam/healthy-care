from __future__ import annotations

CONSTITUTIONS = [
    "平和质", "气虚质", "阳虚质", "阴虚质",
    "痰湿质", "湿热质", "血瘀质", "气郁质", "特禀质",
]

QUESTIONS = [
    {
        "id": 1,
        "question": "您是否经常感到精力充沛？",
        "options": [
            {"label": "总是", "score": 1},
            {"label": "经常", "score": 2},
            {"label": "有时", "score": 3},
            {"label": "从不", "score": 4},
        ],
        "dimensions": {"气虚质": 2, "平和质": -1},
    },
    {
        "id": 2,
        "question": "您是否容易感到疲劳乏力？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"气虚质": 3, "平和质": -2},
    },
    {
        "id": 3,
        "question": "您是否怕冷、手脚冰凉？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"阳虚质": 3},
    },
    {
        "id": 4,
        "question": "您是否感到口干咽燥、手脚心发热？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"阴虚质": 3},
    },
    {
        "id": 5,
        "question": "您是否感觉身体沉重、容易水肿？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"痰湿质": 3},
    },
    {
        "id": 6,
        "question": "您是否容易长痘、出油、口苦？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"湿热质": 3},
    },
    {
        "id": 7,
        "question": "您是否皮肤容易出现瘀斑、面色晦暗？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"血瘀质": 3},
    },
    {
        "id": 8,
        "question": "您是否容易情绪低落、多思多虑？",
        "options": [
            {"label": "从不", "score": 1},
            {"label": "有时", "score": 2},
            {"label": "经常", "score": 3},
            {"label": "总是", "score": 4},
        ],
        "dimensions": {"气郁质": 3},
    },
    {
        "id": 9,
        "question": "您是否有过敏史（皮肤/呼吸/食物）？",
        "options": [
            {"label": "无", "score": 1},
            {"label": "轻微", "score": 2},
            {"label": "中度", "score": 3},
            {"label": "严重", "score": 4},
        ],
        "dimensions": {"特禀质": 3},
    },
    {
        "id": 10,
        "question": "您的睡眠质量如何？",
        "options": [
            {"label": "很好", "score": 1},
            {"label": "较好", "score": 2},
            {"label": "较差", "score": 3},
            {"label": "很差", "score": 4},
        ],
        "dimensions": {"气虚质": 1, "阴虚质": 1, "气郁质": 1},
    },
]


def calculate_scores(answers: dict[int, int]) -> dict[str, float]:
    raw_scores: dict[str, float] = {c: 0.0 for c in CONSTITUTIONS}

    for q in QUESTIONS:
        qid = q["id"]
        answer_score = q["options"][answers[qid]]["score"]
        for dim, weight in q["dimensions"].items():
            if weight > 0:
                raw_scores[dim] += answer_score * (weight / 3.0)
            else:
                raw_scores["平和质"] -= answer_score * (abs(weight) / 3.0)

    max_possible = {c: 0.0 for c in CONSTITUTIONS}
    for q in QUESTIONS:
        max_opt = max(o["score"] for o in q["options"])
        for dim, weight in q["dimensions"].items():
            if weight > 0:
                max_possible[dim] += max_opt * (weight / 3.0)

    normalized: dict[str, float] = {}
    for c in CONSTITUTIONS:
        if max_possible[c] > 0:
            normalized[c] = round(
                min(raw_scores[c] / max_possible[c] * 100, 100), 2
            )
        else:
            normalized[c] = 0.0

    normalized["平和质"] = round(
        max(100 - sum(v for k, v in normalized.items() if k != "平和质") / 8, 0),
        2,
    )

    return normalized


def determine_constitution(scores: dict[str, float]) -> str:
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_type, top_score = sorted_types[0]
    if top_type == "平和质" and top_score >= 60:
        return "平和质"
    if top_score >= 40:
        return top_type
    return "平和质"


def get_severity(score: float) -> str:
    if score >= 70:
        return "重度偏颇"
    elif score >= 50:
        return "中度偏颇"
    elif score >= 30:
        return "轻度偏颇"
    return "基本正常"
