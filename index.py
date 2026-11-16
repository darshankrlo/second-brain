import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from chunker import load_notes, chunk_text

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

records = []
for name, text in load_notes().items():
    for i, chunk in enumerate(chunk_text(text)):
        records.append({"source": name, "chunk_id": i, "text": chunk})

print(f"Embedding {len(records)} chunks...")

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[f"Source: {r['source']}\n{r['text']}" for r in records],
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
)

for record, emb in zip(records, response.embeddings):
    record["embedding"] = emb.values

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(records, f)

print(f"Saved {len(records)} chunks to index.json")