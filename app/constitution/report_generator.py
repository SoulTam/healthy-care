from __future__ import annotations

from app.constitution.algorithm import get_severity

CONSTITUTION_INFO = {
    "平和质": {
        "name": "平和质",
        "features": "体形匀称健壮，面色润泽，目光有神，精力充沛，睡眠良好，食欲正常，二便正常。",
        "advice": "保持规律作息，均衡饮食，适度运动，维持良好生活习惯即可。",
        "cautions": "避免过度进补，保持饮食多样化。",
    },
    "气虚质": {
        "name": "气虚质",
        "features": "语声低弱，气短懒言，容易疲乏，精神不振，易出虚汗。",
        "advice": "多食益气健脾食物，如山药、红枣、小米、鸡肉。避免过度劳累。",
        "cautions": "少食生冷油腻，避免熬夜和剧烈运动。",
    },
    "阳虚质": {
        "name": "阳虚质",
        "features": "畏寒怕冷，手足不温，喜热饮食，精神不振，大便稀溏。",
        "advice": "多食温阳食物，如羊肉、韭菜、生姜、桂圆。注意保暖。",
        "cautions": "少食寒凉食物（西瓜、梨、蟹等），冬季特别注意保暖。",
    },
    "阴虚质": {
        "name": "阴虚质",
        "features": "手足心热，口燥咽干，喜冷饮，大便干燥，面色潮红。",
        "advice": "多食滋阴食物，如百合、银耳、鸭肉、黑芝麻。避免熬夜。",
        "cautions": "少食辛辣燥热食物，避免高温环境。",
    },
    "痰湿质": {
        "name": "痰湿质",
        "features": "体形肥胖，腹部肥满，面部油脂多，胸闷痰多，身重不爽。",
        "advice": "多食健脾祛湿食物，如薏米、赤小豆、冬瓜、白萝卜。加强运动。",
        "cautions": "少食甜腻、油炸、高脂食物，控制饮食总量。",
    },
    "湿热质": {
        "name": "湿热质",
        "features": "面垢油光，易生痤疮，口苦口干，身重困倦，大便黏滞。",
        "advice": "多食清热祛湿食物，如绿豆、苦瓜、黄瓜、薏米。保持皮肤清洁。",
        "cautions": "少食辛辣、油腻、烧烤食物，避免烟酒。",
    },
    "血瘀质": {
        "name": "血瘀质",
        "features": "肤色晦暗，色素沉着，易出现瘀斑，唇色紫暗，舌下静脉曲张。",
        "advice": "多食活血化瘀食物，如山楂、黑豆、油菜、醋。适度运动促进循环。",
        "cautions": "少食肥甘厚味，避免久坐不动。",
    },
    "气郁质": {
        "name": "气郁质",
        "features": "神情抑郁，烦闷不乐，胸胁胀满，多思多虑，敏感多疑。",
        "advice": "多食行气解郁食物，如玫瑰花茶、佛手、柑橘、小麦。培养兴趣爱好。",
        "cautions": "避免独处和负面情绪积累，多参与社交活动。",
    },
    "特禀质": {
        "name": "特禀质",
        "features": "易过敏（皮肤/呼吸/食物），打喷嚏、流清涕，皮肤易起荨麻疹。",
        "advice": "明确过敏原并规避，多食富含维生素C的食物，增强免疫力。",
        "cautions": "季节交替时注意防护，随身携带抗过敏药物。",
    },
}


def generate_report(
    constitution_type: str, scores: dict[str, float], trend: str | None = None
) -> str:
    info = CONSTITUTION_INFO.get(
        constitution_type, CONSTITUTION_INFO["平和质"]
    )
    severity = get_severity(scores.get(constitution_type, 0))
    score = scores.get(constitution_type, 0)

    report = f"""## 体质评估报告

### 主体质：{info['name']}（{severity}）
**综合评分：** {score} 分

### 体质特征
{info['features']}

### 调养建议
{info['advice']}

### 注意事项
{info['cautions']}

### 各维度评分
"""
    for c, s in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * max(1, int(s / 10))
        report += f"- {c}: {s} 分 {bar}\n"

    if trend:
        trend_desc = {
            "improving": "较上次评估有所改善",
            "stable": "与上次评估基本持平",
            "declining": "较上次评估有所下降",
        }.get(trend, "")
        report += f"\n### 趋势\n{trend_desc}\n"

    return report
