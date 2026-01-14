# Quickstart: Ingestion Pipeline

## Overview
Quick start guide for implementing and testing the ingestion pipeline with AI classification and vector processing.

## Prerequisites
- Python 3.11+
- FastAPI and SQLModel (from backend foundation)
- Hugging Face API access with appropriate tokens
- Neon PostgreSQL database with pgvector extension
- Required Python packages: `PyMuPDF`, `requests`, `python-multipart`

## Setup Steps

### 1. Install Dependencies
```bash
pip install PyMuPDF python-multipart requests
```

### 2. Configure API Keys
Set the `HUGGING_FACE_API_KEY` in your environment or `.env` file.

### 3. Create the Service Files
Create `backend/src/services/ingestion.py` and `backend/src/services/ai.py` with the planned functionality.

### 4. Update API Endpoint
Add the POST /api/admin/upload endpoint to handle file uploads.

## Testing the Pipeline

### 1. Start the Service
```bash
cd backend
uvicorn src.main:app --reload
```

### 2. Test File Upload
```bash
curl -X POST "http://localhost:8000/api/admin/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_document.pdf"
```

### 3. Verify Processing
- Check that the KnowledgeDoc is created with correct relevance flag
- For relevant documents, verify VectorChunks are created
- For irrelevant documents, verify they're not vectorized

## Key Endpoints
- `POST /api/admin/upload` - Upload and process documents

## Configuration Options
- `FILE_SIZE_LIMIT`: Maximum file size (default: 50MB)
- `CLASSIFICATION_TIMEOUT`: Timeout for AI classification (default: 60 seconds)
- `CHUNK_SIZE`: Target character count for text chunks (default: 500)

## Troubleshooting
- Ensure Hugging Face API key is properly configured
- Check that the database tables exist and are accessible
- Verify file upload path permissions
- Monitor logs for processing errors