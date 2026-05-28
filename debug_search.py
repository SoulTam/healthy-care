import jieba
from src.search_engine import SearchEngine, _tokenize
from src.intent_parser import IntentParser
from src.models import QueryConditions

e = SearchEngine("data/recipes.json", "index")
e.initialize()
p = IntentParser()

# Test 1: Tokenize
print("=== Tokenize Test ===")
print("阴虚质 春季 ->", _tokenize("阴虚质 春季"))
print("口干 失眠 秋季 ->", _tokenize("口干 失眠 秋季"))

# Test 2: Intent parse
conds = p.parse("阴虚体质春天怎么调理")
print("\n=== Parse Result ===")
print(f"  constitutions: {conds.constitutions}")
print(f"  seasons: {conds.seasons}")
print(f"  symptoms: {conds.symptoms}")

# Test 3: Direct Whoosh search
from whoosh.qparser import MultifieldParser, OrGroup
search_fields = ["name", "ingredients", "effects", "symptoms", "constitutions_text", "seasons_text"]
qp = MultifieldParser(search_fields, schema=e.ix.schema, group=OrGroup)
query_text = _tokenize(" ".join(conds.constitutions + conds.seasons + conds.symptoms + conds.effects))
print(f"\n=== Whoosh Query: '{query_text}' ===")
with e.ix.searcher() as searcher:
    query = qp.parse(query_text)
    print(f"  Parsed query: {query}")
    results = searcher.search(query, limit=10)
    print(f"  BM25 results: {len(results)}")
    for r in results:
        print(f"    id={r['id']} name={r['name']} score={r.score}")

# Test 4: metadata-only search (simulate with all recipes)
print("\n=== Metadata-only Search ===")
for recipe in e.recipes:
    meta = e._compute_metadata_score(recipe, conds)
    if meta > 0:
        print(f"  {recipe['id']:2d}. {recipe['name']} meta={meta:.4f} constitutions={recipe['constitutions']} seasons={recipe['seasons']}")

# Test 5: Full hybrid search
print("\n=== Full Search ===")
results = e.search(conds, top_k=5)
for r in results:
    print(f"  {r['id']:2d}. {r['name']} hybrid={r['scores']['hybrid']:.4f}")
