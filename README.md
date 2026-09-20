# FastAPI Posts API

A simple REST API built with FastAPI for managing blog posts, backed by PostgreSQL.

## Features

- **Create Posts** - Add new blog posts with title and content
- **Read Posts** - Retrieve all posts or a specific post by ID
- **Update Posts** - Modify existing posts
- **Delete Posts** - Remove posts from the database
- **Database Persistence** - PostgreSQL with SQLAlchemy ORM

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Database Driver**: psycopg2

## Project Structure

```
.
├── main.py          # FastAPI application and route handlers
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── database.py      # Database configuration and session management
├── __init__.py      # Package initialization
└── requirements.txt # Project dependencies
```

## Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Update the database URL in `database.py`:

```python
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:your_password@localhost/fastapi'
```

Ensure PostgreSQL is running and the `fastapi` database exists:
```sql
CREATE DATABASE fastapi;
```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts` | Get all posts |
| POST | `/posts` | Create a new post |
| GET | `/posts/{id}` | Get a specific post |
| PUT | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |

## Request/Response Examples

### Create a Post
```bash
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "This is amazing!", "published": true}'
```

### Get All Posts
```bash
curl "http://localhost:8000/posts"
```

### Get a Specific Post
```bash
curl "http://localhost:8000/posts/1"
```

### Update a Post
```bash
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "content": "Updated content"}'
```

### Delete a Post
```bash
curl -X DELETE "http://localhost:8000/posts/1"
```

## Development Notes

- The application includes automatic database connection retry logic with 2-second intervals
- Tables are created automatically on startup
- All timestamps are stored in UTC via PostgreSQL's `now()` function

## License

MIT
