import sys
from pathlib import Path

# Ensure project root is on sys.path when running the script directly
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import SessionLocal
from app.ml.models import Document
from app.ml.embedding_service import generate_embedding

def backfill_embeddings():
    session = SessionLocal()
    try:
        docs = session.query(Document).all()
        for doc in docs:
            if doc.embedding is None:
                text = f"{doc.title}\n{doc.content}"
                doc.embedding = generate_embedding(text)
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    backfill_embeddings()
    print("Embeddings generated")
