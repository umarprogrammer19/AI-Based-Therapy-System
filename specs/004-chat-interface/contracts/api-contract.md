# API Contract: Chat Interface (Frontend-Backend Communication)

## Overview
API contract defining the communication between the frontend chat interface and the backend API for streaming chat responses.

## Endpoint: POST /api/chat (Frontend API Route)
### Description
Frontend API route that proxies requests to the backend chat API. Handles CORS and provides a clean interface between the frontend and backend services.

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
  "user_id": "web_user"
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
  "message": "Ketamine therapy has shown promising results for treatment-resistant depression...",
  "query_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "response_id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "confidence": 0.85,
  "context_used": [
    {
      "chunk_id": "c9b8a7d6-e5f4-3210-9876-543210fedcba",
      "text_preview": "Ketamine therapy for treatment-resistant depression...",
      "similarity_score": 0.92
    }
  ],
  "is_off_topic": false,
  "timestamp": "2026-01-14T10:30:00.000Z"
}
```

**Error Response (500 Internal Server Error)**
```json
{
  "error": "Proxy error"
}
```

## Client-Side Streaming Implementation

### useChat Hook Configuration
The frontend uses the Vercel AI SDK's `useChat` hook to handle streaming responses:

```typescript
const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
  api: '/api/chat',
  headers: {
    'Content-Type': 'application/json',
  },
  body: {
    user_id: 'web_user',
  },
});
```

### Message Object Structure
Each message returned by the hook follows this structure:
```typescript
{
  id: string,           // Unique message identifier
  content: string,      // Message text content
  role: 'user' | 'assistant',  // Sender role
  createdAt: Date,      // Timestamp of message creation
}
```

## Error Handling
- Network errors during API requests
- Backend service unavailability
- Malformed responses from backend
- Timeout scenarios
- CORS-related issues (handled by proxy route)

## Headers
- `Content-Type: application/json` for all requests
- Additional headers forwarded from frontend to backend as needed

## Security Considerations
- Input validation for query length and content
- Sanitization of user inputs
- Proper error handling to avoid exposing system details
- Authentication handling if required (future enhancement)