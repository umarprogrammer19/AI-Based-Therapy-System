# Quickstart Guide: Backend Foundation

## Prerequisites

- Python 3.11+
- uv package manager
- Access to Neon PostgreSQL database with pgvector extension enabled

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies with uv
```bash
# Install uv if you don't have it
pip install uv

# Navigate to backend directory
cd backend

# Install dependencies
uv pip install fastapi sqlmodel pgvector asyncpg python-multipart python-dotenv
uv pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@neon-host.region.neon.tech/dbname
HUGGING_FACE_API_KEY=your_huggingface_api_key_here
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 4. Initialize Database
```bash
# Run database migrations
cd backend
alembic upgrade head
```

### 5. Run the Application
```bash
# Start the FastAPI server
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Knowledge Docs
- `GET /api/v1/knowledge-docs/` - List all knowledge documents
- `POST /api/v1/knowledge-docs/` - Create a new knowledge document
- `GET /api/v1/knowledge-docs/{id}` - Get a specific knowledge document
- `PUT /api/v1/knowledge-docs/{id}` - Update a knowledge document
- `DELETE /api/v1/knowledge-docs/{id}` - Delete a knowledge document

### Vector Chunks
- `GET /api/v1/vector-chunks/` - List all vector chunks
- `POST /api/v1/vector-chunks/` - Create a new vector chunk
- `GET /api/v1/vector-chunks/{id}` - Get a specific vector chunk
- `PUT /api/v1/vector-chunks/{id}` - Update a vector chunk
- `DELETE /api/v1/vector-chunks/{id}` - Delete a vector chunk
- `POST /api/v1/vector-chunks/search` - Search for similar vector chunks

### Audit Logs
- `GET /api/v1/audit-logs/` - List all audit logs
- `GET /api/v1/audit-logs/{id}` - Get a specific audit log
- `GET /api/v1/audit-logs/actions` - Filter logs by action type

## Development

### Running Tests
```bash
cd backend
pytest tests/
```

### Adding New Dependencies
```bash
cd backend
uv pip install <package-name>
uv pip freeze > requirements.txt
```

### Database Migrations
```bash
# Generate a new migration after changing models
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```