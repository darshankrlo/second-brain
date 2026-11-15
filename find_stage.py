import json

with open("index.json", encoding="utf-8") as f:
    records = json.load(f)

for label in ["Stage 1", "Stage 3"]:
    print(f"\n{label}:")
    for r in records:
        if label in r["text"]:
            print(f"  {r['source']} chunk {r['chunk_id']}")