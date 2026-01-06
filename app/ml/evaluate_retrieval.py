from app.ml.vector_search import semantic_search

def evaluate_retrieval(query: str, expected_keywords: list[str]) -> float:
    results = semantic_search(query, limit=3)

    text = " ".join(r.content.lower() for r in results)
    hits = sum(1 for kw in expected_keywords if kw in text)

    return hits / len(expected_keywords)
