# Data Model: Chat Endpoint with RAG

## Overview
Data models for the chat endpoint with RAG functionality including query handling, response generation, and interaction tracking.

## ChatQuery (NEW)
**Fields**:
- `id`: UUID (primary key)
- `user_id`: String (required) - ID of the user who submitted the query
- `query_text`: String (required, max 1000 chars) - the user's input query
- `session_id`: String (optional) - identifier for conversation session
- `timestamp`: DateTime (auto-generated) - when the query was submitted
- `query_embedding`: Array[Float] (optional) - vector embedding of the query
- `is_off_topic`: Boolean (optional) - result of guardrail check
- `retrieved_context_ids`: List[UUID] (optional) - IDs of VectorChunks retrieved
- `metadata`: JSON (optional) - additional query metadata

**Validation Rules**:
- `query_text` must be between 1 and 1000 characters
- `user_id` must not be empty
- `query_embedding` must have exactly 384 dimensions if provided

## ChatResponse (NEW)
**Fields**:
- `id`: UUID (primary key)
- `chat_query_id`: UUID (foreign key) - reference to the associated query
- `response_text`: String (required) - the generated response
- `confidence_score`: Float (optional) - confidence in the response
- `used_context_ids`: List[UUID] (optional) - IDs of VectorChunks used in response
- `generation_time_ms`: Integer (optional) - time taken to generate response
- `timestamp`: DateTime (auto-generated) - when the response was generated
- `metadata`: JSON (optional) - additional response metadata

**Validation Rules**:
- `response_text` must not be empty
- `confidence_score` must be between 0.0 and 1.0 if provided
- `generation_time_ms` must be non-negative

## ChatSession (NEW)
**Fields**:
- `id`: UUID (primary key)
- `user_id`: String (required) - ID of the user
- `created_at`: DateTime (auto-generated) - when the session was started
- `last_activity`: DateTime (auto-generated) - when the session was last used
- `conversation_history`: JSON (optional) - truncated conversation history
- `active`: Boolean (default true) - whether the session is still active
- `metadata`: JSON (optional) - additional session metadata

**Validation Rules**:
- `user_id` must not be empty
- `conversation_history` must not exceed reasonable size limits

## Relationships
- `ChatQuery` → `ChatResponse` (one-to-one relationship, optional)
- `ChatQuery` → `VectorChunk` (many-to-many relationship via retrieved_context_ids)
- `ChatQuery` → `ChatSession` (many-to-one relationship, optional)
- `ChatResponse` → `VectorChunk` (many-to-many relationship via used_context_ids)

## Indexes
- Index on `ChatQuery.user_id` for user-specific queries
- Index on `ChatQuery.timestamp` for chronological ordering
- Index on `ChatResponse.chat_query_id` for query-response lookup
- Index on `ChatSession.user_id` for user-specific sessions
- Index on `ChatSession.last_activity` for session cleanup

## State Transitions for Query Processing
- `received` → `guardrail_checked` → `context_retrieved` → `response_generated`
- `received` → `guardrail_checked` → `off_topic_response` (for off-topic queries)
- Any state → `failed` (on error)