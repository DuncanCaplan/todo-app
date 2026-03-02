from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app
from app.models import Base

TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSession = sessionmaker(bind=test_engine)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create():
    response = client.post(
        "/todos", json={"title": "Test todo", "description": "A test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test todo"
    assert data["description"] == "A test"
    assert not data["completed"]


def test_fetch_all():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_fetch():
    create_response = client.post("/todos", json={"title": "Fetch single todo"})
    todo_id = create_response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Fetch single todo"
    assert not data["completed"]


def test_update():
    create_response = client.post("/todos", json={"title": "Before update"})
    todo_id = create_response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "After update"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "After update"


def test_delete():
    create_response = client.post("/todos", json={"title": "Test delete"})
    todo_id = create_response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    deleted_response = client.get(f"/todos/{todo_id}")
    assert deleted_response.status_code == 404
