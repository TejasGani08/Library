from fastapi import FastAPI
from pydantic import BaseModel
from embeddings.embed import generate_embedding
from db.vector_store import VectorStore
from openai import OpenAI

client = OpenAI()
app = FastAPI()

store = VectorStore()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    query_embedding = generate_embedding(q.question)
    results = store.search(query_embedding, top_k=3)

    context = "\n".join([r["text"] for r in results])
    prompt = f"Answer the question based only on the context below:\n\n{context}\n\nQuestion: {q.question}\nAnswer:"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [r["url"] for r in results]
    }