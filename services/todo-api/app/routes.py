from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Todo, TodoCreate, TodoResponse, TodoUpdate

router = APIRouter()


# Creates new todos
@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


# Lists all todos
@router.get("/todos", response_model=list[TodoResponse])
def fetch_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()


# Gets a specific todo
@router.get("/todos/{id}", response_model=TodoResponse)
def fetch_todo(id: int, db: Session = Depends(get_db)):
    target_todo = db.query(Todo).filter(Todo.id == id).first()
    if not target_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return target_todo


# Updates a specific todo
@router.put("/todos/{id}", response_model=TodoResponse, status_code=200)
def update_todo(id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    target_todo = db.query(Todo).filter(Todo.id == id).first()
    if not target_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(target_todo, key, value)
    db.commit()
    db.refresh(target_todo)
    return target_todo


# Deletes a specific todo
@router.delete("/todos/{id}", status_code=204)
def delete_todo(id: int, db: Session = Depends(get_db)):
    target_todo = db.query(Todo).filter(Todo.id == id).first()
    if not target_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(target_todo)
    db.commit()


@router.get("/health")
def health():
    return {"status": "healthy"}
