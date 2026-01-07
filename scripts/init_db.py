from sqlalchemy import create_engine
from app.ml.models import Base
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://airflow:airflow@localhost:5432/rag_db"
)

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully")


if __name__ == "__main__":
    init_db()
