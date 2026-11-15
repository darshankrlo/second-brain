# Second Brain

A small RAG (retrieval-augmented generation) app that answers questions from my own text notes, in Python with the Gemini API. If the notes don't contain the answer, it says so instead of making one up.

## How it works

**Indexing (run once per set of notes)**
1. `chunker.py` loads every `.txt` file in `notes/` and splits it into overlapping chunks of 100 words (20 words of overlap, so ideas on a boundary aren't cut in half)
2. `index.py` turns each chunk into an embedding (a list of 3072 numbers that captures its meaning) and saves chunks and embeddings to `index.json`

**Querying (every question)**
1. `search.py` embeds the question and ranks all chunks by cosine similarity, keeping the top k
2. `answer.py` pastes those chunks into a prompt and asks the model to answer using only them. A system instruction tells it to reply "I couldn't find that in your notes" when the context doesn't contain the answer
3. The sources (file, chunk and score) are printed under every answer so it can be checked

## Setup

```bash
git clone https://github.com/darshankrlo/second-brain.git
cd second-brain
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file with a free key from Google AI Studio:

```
GEMINI_API_KEY=your_key_here
```

Create a `notes/` folder and add your own `.txt` files. Then:

```bash
python index.py     # build the index
python answer.py    # ask questions
```

Note: on the free tier, content you send may be used by Google to improve its products, so don't index anything private.

## What I learned

- Why RAG exists: sending 200 pages in every prompt wastes tokens, hits limits and hurts accuracy
- Embeddings capture meaning, so a question can match a chunk that uses different words
- Cosine similarity scores for unrelated text are not near zero, so I rank by top-k and read the chunks instead of trusting a fixed cutoff
- A grounding rule in the system instruction made the model refuse when my notes had no answer
- Retrieval can only be as complete as the source text: when an answer looked incomplete, I checked the raw notes first, then the index, then the retrieved chunks

## Limitations

- Chunks are cut by word count, so they can start or end mid-sentence or mid-code-block
- Retrieval always returns k chunks, even when none are relevant, so the Sources list can look misleading on a refusal
- The index is a JSON file that is rebuilt from scratch, not a real vector database

## Next

- Turn search into a tool for an agent loop
- Chunk by paragraphs or headings
- Index new notes without rebuilding everything