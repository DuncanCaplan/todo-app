import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database address, with fallback if env is set for CI
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://todo:changeme@localhost/todo-db"
)

# Only adds the argument when using SQLite for tests
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Creates per-request database sessions
SessionLocal = sessionmaker(bind=engine)


# Guarantees db.close() runs
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
