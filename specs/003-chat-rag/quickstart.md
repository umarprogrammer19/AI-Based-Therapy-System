# Quickstart Guide: Chat Endpoint with RAG

## Overview
Quickstart guide for implementing and testing the chat endpoint with RAG functionality.

## Prerequisites
- Python 3.13+
- FastAPI
- PostgreSQL with pgvector extension
- Hugging Face API access
- Existing vector database with ketamine therapy knowledge base

## Setup
1. Ensure the vector database has been populated with ketamine therapy documents
2. Configure Hugging Face API settings in environment variables
3. Verify database connectivity and vector extensions

## Implementation Steps

### Step 1: Create Chat Service
1. Create `services/chat.py` with RAG logic
2. Implement guardrail functionality to detect off-topic queries
3. Implement vector similarity search against VectorChunk records
4. Integrate with AI service for response generation

### Step 2: Create API Endpoint
1. Create `api/v1/chat.py` with POST /api/chat endpoint
2. Implement request/response validation
3. Connect to chat service for processing
4. Add proper error handling

### Step 3: Integration
1. Register the chat endpoint in the main router
2. Add any necessary middleware
3. Implement logging and monitoring

## Testing
1. Test with on-topic queries about ketamine therapy
2. Test with off-topic queries to verify guardrails
3. Verify context retrieval and response generation
4. Test error handling scenarios

## Example Usage
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the benefits of ketamine therapy for depression?",
    "user_id": "test_user"
  }'
```

## Expected Output
- Successful response with generated answer
- Confidence score and context references
- Proper handling of off-topic queries
- Error responses for invalid inputs

## Troubleshooting
- Verify Hugging Face API key is properly configured
- Check that vector database contains relevant content
- Confirm pgvector extension is properly installed
- Review logs for any processing errors