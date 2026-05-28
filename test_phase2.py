import json
from src.search_engine import SearchEngine
from src.intent_parser import IntentParser
from src.combiner import Combiner

e = SearchEngine("data/recipes.json", "index")
e.initialize()
p = IntentParser()
c = Combiner()

query = "我最近口干，经常失眠，秋天了想调理一下"
conds = p.parse(query)
print("=== 解析结果 ===")
print(json.dumps(conds.model_dump(), ensure_ascii=False, indent=2))

print()
print("=== 搜索 Top-8 ===")
results = e.search(conds, top_k=8)
for r in results:
    print(f'  {r["id"]:2d}. {r["name"]:10s} | 体质: {str(r["constitutions"]):15s} | 季节: {str(r["seasons"]):10s} | 症状: {str(r["symptoms"]):25s} | 评分: {r["scores"]["hybrid"]:.4f}')

print()
print("=== 方案组合 (1日) ===")
plan = c.combine(results, days=1)
print(json.dumps(plan, ensure_ascii=False, indent=2, default=str))

print()
print("=== 更多测试 ===")

queries = [
    "夏天上火长痘了",
    "冬天怕冷手脚冰凉",
    "最近湿气重，痰多",
    "我是阴虚体质，春天怎么调理",
]
for q in queries:
    conds = p.parse(q)
    results = e.search(conds, top_k=3)
    names = [r["name"] for r in results]
    print(f'  "{q}" -> {names}')
