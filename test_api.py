import requests
import json

BASE = "http://127.0.0.1:8000"

def test_root():
    r = requests.get(f"{BASE}/")
    print("=== / ===")
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def test_search(query, top_k=5):
    r = requests.post(f"{BASE}/search", json={"query": query, "top_k": top_k})
    d = r.json()
    print(f"\n=== /search: {query} ===")
    print(f"  条件: {json.dumps(d['conditions'], ensure_ascii=False)}")
    print(f"  结果数: {d['total']}")
    for i, x in enumerate(d["results"]):
        print(f"  {i+1}. {x['name']} | 体质:{x['constitutions']} 季节:{x['seasons']} 症状:{x['symptoms']} hybrid={x['scores']['hybrid']}")

def test_plan(query, days=1):
    r = requests.post(f"{BASE}/plan", json={"query": query, "days": days})
    d = r.json()
    print(f"\n=== /plan: {query} ({days}天) ===")
    for day in d["plan"]["days"]:
        print(f"  第{day['day']}天:")
        for meal in day["meals"]:
            if "recipe" in meal:
                print(f"    {meal['meal']}({meal['category']}): {meal['recipe']['name']}")
            elif "recipes" in meal:
                names = [r["name"] for r in meal["recipes"]]
                print(f"    {meal['meal']}({meal['category']}): {', '.join(names)}")

def test_recipes():
    r = requests.get(f"{BASE}/recipes")
    d = r.json()
    print(f"\n=== /recipes: {len(d)} total ===")
    for x in d:
        print(f"  {x['id']:2d}. {x['name']} [{x['category']}] {x['constitutions']} {x['seasons']}")

if __name__ == "__main__":
    test_root()
    test_search("我最近口干，经常失眠，秋天了想调理一下")
    test_search("夏天上火长痘了")
    test_search("冬天怕冷手脚冰凉")
    test_search("最近湿气重，痰多")
    test_search("我是阴虚体质，春天怎么调理")
    test_plan("秋天口干失眠")
    test_recipes()
