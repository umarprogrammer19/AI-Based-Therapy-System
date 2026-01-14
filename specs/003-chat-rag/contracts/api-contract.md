# API Contract: Chat Endpoint with RAG

## Overview
API contract for the chat endpoint with RAG functionality that enables users to interact with the ketamine therapy knowledge base.

## Endpoint: POST /api/chat

### Description
Accepts user queries and returns AI-generated responses based on the ketamine therapy knowledge base. Implements guardrails to detect off-topic queries and retrieves relevant context from vector database before generating responses.

### Request
**Method**: POST
**Path**: `/api/chat`
**Content-Type**: `application/json`

#### Request Body Schema
```json
{
  "query": {
    "type": "string",
    "minLength": 1,
    "maxLength": 1000,
    "description": "User's query text"
  },
  "user_id": {
    "type": "string",
    "optional": true,
    "description": "Unique identifier for the user (optional)"
  },
  "session_id": {
    "type": "string",
    "optional": true,
    "description": "Conversation session identifier (optional)"
  }
}
```

**Example Request**:
```json
{
  "query": "What are the benefits of ketamine therapy for depression?",
  "user_id": "user123",
  "session_id": "sess456"
}
```

### Response
**Success Response (200 OK)**

#### Response Body Schema
```json
{
  "message": {
    "type": "string",
    "description": "Generated response to the user's query"
  },
  "query_id": {
    "type": "string",
    "format": "uuid",
    "description": "Unique identifier for the query"
  },
  "response_id": {
    "type": "string",
    "format": "uuid",
    "description": "Unique identifier for the response"
  },
  "confidence": {
    "type": "number",
    "minimum": 0,
    "maximum": 1,
    "description": "Confidence score for the response (0-1)"
  },
  "context_used": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "chunk_id": {
          "type": "string",
          "format": "uuid",
          "description": "ID of the VectorChunk used"
        },
        "text_preview": {
          "type": "string",
          "description": "Preview of the context text used"
        },
        "similarity_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Similarity score for this context chunk"
        }
      }
    },
    "description": "Array of context chunks used in the response"
  },
  "is_off_topic": {
    "type": "boolean",
    "description": "Whether the query was detected as off-topic"
  },
  "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "ISO 8601 timestamp of the response"
  }
}
```

**Example Success Response**:
```json
{
  "message": "Ketamine therapy has shown promising results for treatment-resistant depression. Studies indicate that ketamine can provide rapid relief of depressive symptoms, often within hours to days, compared to traditional antidepressants which may take weeks to show effects. The therapy typically involves low-dose infusions administered in a controlled clinical setting.",
  "query_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "response_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "confidence": 0.85,
  "context_used": [
    {
      "chunk_id": "c9b8a7d6-e5f4-3210-9876-543210fedcba",
      "text_preview": "Ketamine therapy for treatment-resistant depression...",
      "similarity_score": 0.92
    },
    {
      "chunk_id": "a5b4c3d2-e1f0-9876-5432-10fedcba9876",
      "text_preview": "Clinical studies show rapid antidepressant effects...",
      "similarity_score": 0.88
    }
  ],
  "is_off_topic": false,
  "timestamp": "2026-01-14T10:30:00.000Z"
}
```

**Error Response (400 Bad Request)**
```json
{
  "detail": "Error message describing the issue"
}
```

**Error Response (422 Unprocessable Entity)**
```json
{
  "detail": "Validation error message"
}
```

**Error Response (500 Internal Server Error)**
```json
{
  "detail": "Internal server error occurred"
}
```

### Error Scenarios
- **400 Bad Request**: Invalid query format or empty query
- **422 Unprocessable Entity**: Validation errors in request body
- **500 Internal Server Error**: Internal server errors during processing

## Security Considerations
- Input validation for query length and content
- Rate limiting to prevent abuse
- User identification for tracking and analytics
- Query sanitization to prevent injection attacks

## Performance Requirements
- Response time: <10 seconds under normal load
- Should handle queries up to 1000 characters in length
- Must support concurrent users