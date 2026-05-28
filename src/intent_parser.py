from __future__ import annotations
import re
import jieba

from src.models import QueryConditions


TCM_DICT_ENTRIES = [
    "阴虚质", "气虚质", "阳虚质", "痰湿质", "湿热质", "血瘀质", "气郁质", "平和质", "特禀质",
    "清热解毒", "滋阴润肺", "清心安神", "补气养血", "健脾祛湿", "温补气血", "活血化瘀",
    "口干舌燥", "四肢冰凉", "腰膝酸软", "食欲不振", "咽喉肿痛",
    "上火", "失眠", "乏力", "口干", "便秘", "腹泻", "胃胀", "头痛", "咳嗽", "痰多",
    "盗汗", "怕冷", "水肿", "长痘", "湿疹", "目涩", "自汗", "气短", "痛经", "胃寒",
    "大便黏腻", "舌苔厚腻", "头晕耳鸣", "面色苍白", "心烦",
    "羊肉", "排骨", "鸡肉", "猪肉", "鸡蛋",
    "红枣", "枸杞", "黄芪", "当归", "陈皮", "茯苓", "桂圆",
]


class IntentParser:
    def __init__(self):
        for word in TCM_DICT_ENTRIES:
            jieba.add_word(word, freq=20, tag="n")

        self.constitution_keywords: dict[str, list[str]] = {
            "气虚": ["气虚质"],
            "阳虚": ["阳虚质"],
            "阴虚": ["阴虚质"],
            "痰湿": ["痰湿质"],
            "湿热": ["湿热质"],
            "血瘀": ["血瘀质"],
            "气郁": ["气郁质"],
            "平和": ["平和质"],
            "特禀": ["特禀质"],
        }

        self.season_keywords: dict[str, list[str]] = {
            "春": ["春季"],
            "夏": ["夏季"],
            "秋": ["秋季"],
            "冬": ["冬季"],
        }

        self.symptom_keywords: dict[str, str] = {
            "口干": "口干", "口渴": "口干", "嘴干": "口干",
            "失眠": "失眠", "睡不着": "失眠", "睡眠不好": "失眠", "多梦": "失眠",
            "乏力": "乏力", "没精神": "乏力", "疲劳": "乏力", "疲倦": "乏力",
            "上火": "上火", "火气大": "上火",
            "便秘": "便秘", "排便困难": "便秘",
            "怕冷": "怕冷", "手脚冰凉": "四肢冰凉", "四肢冰凉": "四肢冰凉",
            "长痘": "长痘", "长痘痘": "长痘",
            "湿疹": "湿疹", "湿气重": "湿疹", "湿气": "湿疹",
            "胃胀": "胃胀", "腹胀": "胃胀",
            "腹泻": "腹泻", "拉肚子": "腹泻",
            "咳嗽": "咳嗽", "干咳": "干咳",
            "痰多": "痰多", "痰": "痰多",
            "头痛": "头痛", "头晕": "头晕耳鸣", "耳鸣": "头晕耳鸣",
            "水肿": "水肿", "浮肿": "水肿",
            "痛经": "痛经",
            "胃寒": "胃寒",
            "自汗": "自汗", "出虚汗": "自汗",
            "气短": "气短", "喘": "气短",
            "目涩": "目涩", "眼睛干": "目涩", "眼干": "目涩",
            "脱发": "脱发", "掉发": "脱发",
            "腰膝酸软": "腰膝酸软",
            "食欲不振": "食欲不振",
            "大便黏腻": "大便黏腻",
            "舌苔厚腻": "舌苔厚腻",
            "心烦": "心烦",
            "面色苍白": "面色苍白",
        }

        self.effect_keywords: dict[str, str] = {
            "滋阴": "滋阴", "润肺": "润肺", "清热": "清热",
            "解毒": "解毒", "补气": "补气", "养血": "养血",
            "安神": "安神", "祛湿": "祛湿", "健脾": "健脾",
            "化痰": "化痰", "活血": "活血", "消肿": "消肿",
            "明目": "明目", "乌发": "乌发",
        }

        self.meal_type_keywords: dict[str, str] = {
            "早餐": "粥", "早饭": "粥", "粥": "粥",
            "午餐": "热菜", "午饭": "热菜",
            "晚餐": "汤羹", "晚饭": "汤羹",
            "汤": "汤羹", "汤羹": "汤羹",
            "甜品": "甜品", "甜点": "甜品",
            "茶": "饮品", "饮品": "饮品",
        }

    def parse(self, text: str) -> QueryConditions:
        tokens = set(jieba.lcut(text))
        text_lower = text.lower()

        constitutions = self._match_constitutions(tokens, text_lower)
        seasons = self._match_seasons(tokens, text_lower)
        symptoms = self._match_symptoms(tokens, text_lower)
        effects = self._match_effects(tokens, text_lower)
        meal_type = self._match_meal_type(tokens, text_lower)

        return QueryConditions(
            constitutions=constitutions,
            seasons=seasons,
            symptoms=symptoms,
            effects=effects,
            meal_type=meal_type,
            raw_text=text,
        )

    def _match_constitutions(self, tokens: set[str], text: str) -> list[str]:
        results = []
        for keyword, constitutions in self.constitution_keywords.items():
            if keyword in text:
                for c in constitutions:
                    if c not in results:
                        results.append(c)
        return results

    def _match_seasons(self, tokens: set[str], text: str) -> list[str]:
        results = []
        season_text_patterns = {
            "春季": ["春", "春天"],
            "夏季": ["夏", "夏天", "暑"],
            "秋季": ["秋", "秋天"],
            "冬季": ["冬", "冬天"],
        }
        for season, patterns in season_text_patterns.items():
            for p in patterns:
                if p in text:
                    if season not in results:
                        results.append(season)
        return results

    def _match_symptoms(self, tokens: set[str], text: str) -> list[str]:
        results = []
        for keyword, symptom in self.symptom_keywords.items():
            if keyword in text:
                if symptom not in results:
                    results.append(symptom)
        return results

    def _match_effects(self, tokens: set[str], text: str) -> list[str]:
        results = []
        for keyword, effect in self.effect_keywords.items():
            if keyword in text:
                if effect not in results:
                    results.append(effect)
        return results

    def _match_meal_type(self, tokens: set[str], text: str) -> str | None:
        for keyword, meal_type in self.meal_type_keywords.items():
            if keyword in text:
                return meal_type
        return None
