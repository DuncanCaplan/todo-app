from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Parent class that provides ability to map to database tables
class Base(DeclarativeBase):
    pass


# The database schema
class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(500), default=None)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


# The todo creation schema
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False


# The todo update schema
class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


# The API response schema
class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
