import sys
from pathlib import Path

# Ensure project root is on sys.path when running the script directly
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import SessionLocal
from app.ml.models import Document
from scripts.sample_data import DOCUMENTS

def ingest():
    session = SessionLocal()
    try:
        for doc in DOCUMENTS:
            exists = session.query(Document).filter_by(title=doc["title"]).first()
            if exists:
                exists.content = doc["content"]
            else:
                session.add(Document(**doc))
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    ingest()
    print("Ingestion complete")
