from app.ml.vector_search import semantic_search
from app.ml.prompts import build_rag_prompt
from app.ml.llm_service import generate_answer

def rag_answer(query: str, limit: int = 5):
    results = semantic_search(query, limit)

    docs = [
        {"title": r.title, "content": r.content}
        for r in results
    ]

    prompt = build_rag_prompt(query, docs)
    return generate_answer(prompt)
