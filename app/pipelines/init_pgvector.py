from sqlalchemy import create_engine, text
import os


def init_pgvector():
    engine = create_engine(os.environ["DATABASE_URL"])

    # begin() creates a transaction and auto-commits
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    print("pgvector extension ensured")
