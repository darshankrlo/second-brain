import os
from dotenv import load_dotenv
from google import genai
import numpy as np

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

sentences = [
    "How do I secure my Docker containers?",
    "Ways to lock down containers against attacks",
    "Best street food in Bangalore",
]

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=sentences,
)

for sentence, emb in zip(sentences, response.embeddings):
    print(f"{sentence!r} -> {len(emb.values)} numbers, first 5: {emb.values[:5]}")



def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

vecs = [e.values for e in response.embeddings]

print()
print("A vs B (docker vs lock down):", round(cosine_similarity(vecs[0], vecs[1]), 3))
print("A vs C (docker vs street food):", round(cosine_similarity(vecs[0], vecs[2]), 3))
print("B vs C (lock down vs street food):", round(cosine_similarity(vecs[1], vecs[2]), 3))