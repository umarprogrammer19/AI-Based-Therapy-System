# Quickstart Guide: Ketamine AI & Learning System

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- PostgreSQL with pgvector extension (or Neon Serverless account)
- Hugging Face API key for Mistral model access
- API key for admin access

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up environment variables:
```bash
# Backend (.env in backend/)
DATABASE_URL="postgresql://username:password@localhost:5432/ketamine_ai"
HF_API_KEY="your_huggingface_api_key_here"
PGVECTOR_EXTENSION_ENABLED="true"
ADMIN_API_KEY="your_admin_api_key_here"
SYSTEM_PROMPT="You are a medical information assistant specializing ONLY in ketamine therapy"
```

```bash
# Frontend (.env in frontend/)
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
NEXT_PUBLIC_ADMIN_API_KEY="your_admin_api_key_here"
```

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
# Make sure PostgreSQL with pgvector is running
python -c "from src.database.init_db import init_db; init_db()"
```

4. Start the backend server:
```bash
uvicorn src.api.main:app --reload --port 8000
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Usage

### For End Users
1. Visit the chat interface at `http://localhost:3000/chat`
2. Ask questions about ketamine therapy
3. Receive responses based on the knowledge base

### For Admin Users
1. Visit the admin panel at `http://localhost:3000/admin`
2. Upload documents using the upload zone
3. View knowledge base with training/non-training status
4. Access audit logs to see who uploaded what

## API Endpoints

### Chat API
- POST `/api/chat` - Submit queries and receive responses

### Upload API
- POST `/api/upload` - Upload documents for classification (requires API key)

### Admin API
- GET `/api/admin/documents` - List all documents with status (requires API key)
- GET `/api/admin/logs` - Get audit logs (requires API key)

## Configuration

The system enforces the following constitutional rules:
- All documents undergo AI classification for ketamine relevance
- Only ketamine-relevant documents are embedded in vector store
- Non-relevant documents are logged for audit but not used for training
- Medical disclaimer is always visible in the UI
- Responses are educational only, no medical diagnoses