import os

def load_notes(folder="notes"):
    notes = {}
    for name in sorted(os.listdir(folder)):
        if name.endswith(".txt"):
            with open(os.path.join(folder, name), encoding="utf-8") as f:
                notes[name] = f.read()
    return notes

def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    step = chunk_size - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_size]))
        if start + chunk_size >= len(words):
            break
    return chunks

if __name__ == "__main__":
    notes = load_notes()
    for name, text in notes.items():
        chunks = chunk_text(text)
        print(f"{name}: {len(text.split())} words -> {len(chunks)} chunks")
        if len(chunks) > 1:
            print("  Last 20 words of chunk 1: ", " ".join(chunks[0].split()[-20:]))
            print("  First 20 words of chunk 2:", " ".join(chunks[1].split()[:20]))