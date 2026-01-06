from fastapi import APIRouter
from app.ml.vector_search import semantic_search
from app.pipelines.rag_pipeline import rag_answer

router = APIRouter()

@router.get("/search")
def search(query: str, limit: int = 5):
    results = semantic_search(query, limit)
    return [
        {
            "id": r.id,
            "title": r.title,
            "content": r.content
        }
        for r in results
    ]

@router.get("/ask")
def ask(query: str):
    answer = rag_answer(query)
    return {"answer": answer}
