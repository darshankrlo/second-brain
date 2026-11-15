from google.genai import types
from search import search, client

SYSTEM = (
    "You answer questions using ONLY the provided notes. "
    "If the notes do not contain the answer, reply exactly: "
    "I couldn't find that in your notes. "
    "Do not use outside knowledge."
)

def answer(question, k=4):
    hits = search(question, k)
    context = "\n\n".join(
        f"[{i}] ({r['source']}, chunk {r['chunk_id']})\n{r['text']}"
        for i, (score, r) in enumerate(hits, 1)
    )
    prompt = f"Notes:\n{context}\n\nQuestion: {question}"
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=SYSTEM),
    )
    return response.text, hits

if __name__ == "__main__":
    question = input("Ask your notes: ")
    text, hits = answer(question)
    print("\n" + text)
    print("\nSources:")
    for score, r in hits:
        print(f"  [{score:.3f}] {r['source']} chunk {r['chunk_id']}")