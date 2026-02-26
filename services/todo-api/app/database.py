from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

# Database address
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

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


# Creates database table
Base.metadata.create_all(bind=engine)
