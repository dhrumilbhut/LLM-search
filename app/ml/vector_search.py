from sqlalchemy import text
from app.core.database import engine
from app.ml.embedding_service import generate_embedding

def semantic_search(query: str, limit: int = 5):
    query_embedding = generate_embedding(query)

    sql = text("""
        SELECT id, title, content
        FROM documents
        ORDER BY embedding <-> CAST(:query_embedding AS vector)
        LIMIT :limit;
    """)

    with engine.connect() as conn:
        results = conn.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "limit": limit
            }
        )
        return results.fetchall()
