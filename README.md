# FastAPI SQLAlchemy CRUD

A modern FastAPI application with SQLAlchemy and SQLite for task management, showcasing best practices for CRUD operations.

## Project Structure

```text
fastapi-sqlalchemy-crud/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── pyproject.toml
└── README.md
```

## Installation and Usage

### 1. Install uv

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone and setup

```bash
git clone <your-repository-url>
cd fastapi-sqlalchemy-crud

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 3. Run the application

```bash
# Run
uvicorn app.main:app --reload
```

#### Note

The application will be available at: `http://localhost:8000`

### 4. Access API documentation

#### Using a browser

After launching the application, you can access the interactive API documentation via browser:

- **Swagger UI**: `http://localhost:8000/docs`
  - Visual representation of all API endpoints
  - Interactive testing functionality for each API
  - Examples of requests and responses
  
- **ReDoc**: `http://localhost:8000/redoc`
  - More readable API documentation format
  - Schema information displayed on the right side
  - Well-organized format suitable for printing

#### Verifying APIs with curl

You can also test each API endpoint directly from the terminal using curl commands:

```bash
# Root endpoint (welcome message)
curl http://localhost:8000/
# Example output: {"message":"Welcome to FastAPI SQLAlchemy CRUD API"}

# Health check
curl http://localhost:8000/health
# Example output: {"status":"healthy"}

# Get task list
curl -X GET "http://localhost:8000/tasks/"
# Example output: [] or [{...task info...}, {...task info...}]

# Get specific task (for ID=1)
curl -X GET "http://localhost:8000/tasks/1"
# Example output: {"title":"Task Title","description":"Task Description","completed":false,"id":1,"created_at":"2023-01-01T00:00:00","updated_at":null}
```

## Testing

To run the tests, follow these steps:

1. **Create and activate the virtual environment**:

    ```bash
    uv venv
    source .venv/bin/activate
    ```

2. **Install project dependencies**:

    ```bash
    uv pip install -e .
    ```

3. **Install testing dependencies (pytest and httpx)**:

    ```bash
    uv pip install pytest httpx
    ```

4. **Run the tests**:

    ```bash
    pytest
    ```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get all tasks (with pagination) |
| GET | `/tasks/{task_id}` | Get task by ID |
| PUT | `/tasks/{task_id}` | Update task by ID |
| DELETE | `/tasks/{task_id}` | Delete task by ID |

## Example Usage

### Create a task

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Study FastAPI documentation and build a sample project",
       "completed": false
     }'
```

### Get all tasks

```bash
curl -X GET "http://localhost:8000/tasks/"
```

### Update a task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "completed": true
     }'
```

### Delete a task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Features

- ✅ Complete CRUD operations for tasks
- ✅ SQLAlchemy ORM with SQLite database
- ✅ Pydantic models for request/response validation
- ✅ Automatic API documentation with Swagger UI
- ✅ Error handling with proper HTTP status codes
- ✅ Database session management
- ✅ Pagination support for listing tasks
- ✅ Partial updates (PATCH-like behavior with PUT)
- ✅ Health check endpoint
- ✅ Modern dependency management with uv

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **SQLite**: Lightweight database engine
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application
- **uv**: Modern, fast Python package manager
