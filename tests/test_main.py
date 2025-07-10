from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Task

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

import pytest

# Fixture to set up and tear down the database for each test
@pytest.fixture(name="setup_database")
def setup_database(): # 関数名をフィクスチャ名に合わせる
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test for the health check endpoint
def test_health_check(setup_database): # 引数名をフィクスチャ名に合わせる
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_task(setup_database): # 引数名をフィクスチャ名に合わせる
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "This is a test task", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["completed"] == False
    assert "id" in data
    assert "created_at" in data

def test_get_tasks(setup_database): # 引数名をフィクスチャ名に合わせる
    # Create a few tasks
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_get_task(setup_database):
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Single Task", "description": "Description for single task", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Get the task
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["title"] == "Single Task"
    assert data["description"] == "Description for single task"

    # Test non-existent task
    not_found_response = client.get("/tasks/999")
    assert not_found_response.status_code == 404
    assert not_found_response.json() == {"detail": "Task not found"}

def test_update_task(setup_database):
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Task to Update", "description": "Original description", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Update the task
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task Title", "completed": True}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Task Title"
    assert data["completed"] == True
    assert data["description"] == "Original description" # Description should remain unchanged

    # Test partial update
    partial_update_response = client.put(
        f"/tasks/{task_id}",
        json={"description": "New description"}
    )
    assert partial_update_response.status_code == 200
    data = partial_update_response.json()
    assert data["description"] == "New description"
    assert data["title"] == "Updated Task Title" # Title should remain unchanged

    # Test non-existent task update
    not_found_update_response = client.put(
        "/tasks/999",
        json={"title": "Non Existent"}
    )
    assert not_found_update_response.status_code == 404
    assert not_found_update_response.json() == {"detail": "Task not found"}

def test_delete_task(setup_database):
    # Create a task
    create_response = client.post(
        "/tasks/",
        json={"title": "Task to Delete", "description": "Delete me", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204 # No Content

    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Task not found"}

    # Test non-existent task delete
    not_found_delete_response = client.delete("/tasks/999")
    assert not_found_delete_response.status_code == 404
    assert not_found_delete_response.json() == {"detail": "Task not found"}
