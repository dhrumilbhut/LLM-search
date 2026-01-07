from sqlalchemy import create_engine
from app.ml.models import Base
import os


def init_schema():
    engine = create_engine(os.environ["DATABASE_URL"])
    Base.metadata.create_all(engine)
    print("Schema ensured")
