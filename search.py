import os
import json
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("index.json", encoding="utf-8") as f:
    records = json.load(f)

def search(question, k=3):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    q = np.array(response.embeddings[0].values)

    scored = []
    for r in records:
        v = np.array(r["embedding"])
        score = float(np.dot(q, v) / (np.linalg.norm(q) * np.linalg.norm(v)))
        scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]

if __name__ == "__main__":
    question = input("Ask your notes: ")
    for score, r in search(question):
        print(f"\n[{score:.3f}] {r['source']} (chunk {r['chunk_id']})")
        print(r["text"][:200], "...")