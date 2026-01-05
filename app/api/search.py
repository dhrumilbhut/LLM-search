from fastapi import APIRouter
from app.ml.vector_search import semantic_search

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
