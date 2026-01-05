import sys
from pathlib import Path

# Ensure project root is on sys.path when running the script directly
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import engine, Base
from app.ml.models import Document

Base.metadata.create_all(bind=engine)
print("Tables created")
