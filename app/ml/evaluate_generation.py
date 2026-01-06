from app.pipelines.rag_pipeline import rag_answer

def evaluate_generation(query: str, expected_keywords: list[str]) -> float:
    answer = rag_answer(query).lower()
    hits = sum(1 for kw in expected_keywords if kw in answer)
    return hits / len(expected_keywords)
