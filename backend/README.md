# Backend Foundation

This is the backend foundation for the RAG (Retrieval-Augmented Generation) system, built with FastAPI, SQLModel, and PostgreSQL with pgvector extension.

## Features

- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints
- **SQLModel**: Combines SQLAlchemy and Pydantic for database models
- **PostgreSQL + pgvector**: Vector similarity search capabilities
- **AsyncPG**: Asynchronous PostgreSQL client library
- **Health Checks**: Built-in health check endpoint
- **API Documentation**: Automatic API documentation with Swagger UI and ReDoc

## Architecture

The backend follows a modular architecture:

- **Models**: Data models using SQLModel
- **Services**: Business logic layer
- **API**: API endpoints and routing
- **Utils**: Utility functions
- **Config**: Configuration and database setup

## API Endpoints

### Health Check
- `GET /health` - Check the health status of the application

### Knowledge Documents
- `POST /api/v1/knowledge-docs/` - Create a new knowledge document
- `GET /api/v1/knowledge-docs/{id}` - Get a specific knowledge document
- `GET /api/v1/knowledge-docs/` - Get a list of knowledge documents
- `PUT /api/v1/knowledge-docs/{id}` - Update a knowledge document
- `DELETE /api/v1/knowledge-docs/{id}` - Delete a knowledge document

### Vector Chunks
- `POST /api/v1/vector-chunks/` - Create a new vector chunk
- `GET /api/v1/vector-chunks/{id}` - Get a specific vector chunk
- `GET /api/v1/vector-chunks/` - Get a list of vector chunks
- `PUT /api/v1/vector-chunks/{id}` - Update a vector chunk
- `DELETE /api/v1/vector-chunks/{id}` - Delete a vector chunk
- `POST /api/v1/vector-chunks/search` - Search for similar vector chunks

### Audit Logs
- `GET /api/v1/audit-logs/` - Get a list of audit logs
- `GET /api/v1/audit-logs/{id}` - Get a specific audit log
- `GET /api/v1/audit-logs/actions/{action}` - Get audit logs filtered by action type

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL with pgvector extension
- uv package manager

### Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Set up environment variables (see `.env.example`)
5. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database URL
- `HUGGING_FACE_API_KEY`: Hugging Face API key for embedding generation
- `SECRET_KEY`: Secret key for JWT tokens
- `DEBUG`: Enable/disable debug mode (true/false)

## Development

To run tests:
```bash
pytest tests/
```

To format code:
```bash
black src/
```

To run linting:
```bash
flake8 src/
```

## Docker

To run with Docker:
```bash
docker-compose up
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request