import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database address
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/todos.db")

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    os.makedirs("data", exist_ok=True)

# Creates the database "todos.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creates per-request database sessions
SessionLocal = sessionmaker(bind=engine)


# Guarantees db.close() runs
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
