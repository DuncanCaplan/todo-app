from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes import router

app = FastAPI(title="Todo API", version="0.1.0")


app.include_router(router)

# Creates database table
Base.metadata.create_all(bind=engine)
