# Data Model: Chat Interface (Home Page)

## Overview
Data models for the frontend chat interface including message structures and session management.

## ChatMessage (Frontend Model)
**Fields**:
- `id`: string (required) - Unique identifier for the message
- `content`: string (required) - The text content of the message
- `role`: "user" | "assistant" (required) - The sender of the message
- `createdAt`: Date (required) - Timestamp when the message was created
- `status`: "sent" | "delivered" | "error" (optional) - Status of the message delivery

**Validation Rules**:
- `content` must not be empty
- `role` must be either "user" or "assistant"
- `createdAt` must be a valid timestamp

## ChatSession (Frontend Model)
**Fields**:
- `id`: string (required) - Unique identifier for the session
- `messages`: ChatMessage[] (required) - Array of messages in the session
- `createdAt`: Date (required) - When the session started
- `updatedAt`: Date (required) - When the session was last updated
- `isActive`: boolean (optional) - Whether the session is currently active

**Validation Rules**:
- `messages` must be an array of valid ChatMessage objects
- `isActive` defaults to true when not specified

## UserInput (Frontend Model)
**Fields**:
- `text`: string (required) - The text entered by the user
- `attachments`: File[] (optional) - Any files attached to the message
- `timestamp`: Date (required) - When the input was submitted

**Validation Rules**:
- `text` must not be empty
- `text` must be less than 1000 characters
- `attachments` size must be less than 10MB total

## APIResponse (Frontend Model)
**Fields**:
- `message`: string (required) - The generated response message
- `query_id`: string (required) - ID of the original query
- `response_id`: string (required) - ID of the response
- `confidence`: number (optional) - Confidence score between 0 and 1
- `context_used`: Array<Object> (optional) - Context chunks used in the response
- `is_off_topic`: boolean (optional) - Whether the query was off-topic
- `timestamp`: string (required) - ISO timestamp of the response

**Validation Rules**:
- `confidence` must be between 0 and 1 if provided
- `message` must not be empty
- `query_id` and `response_id` must be valid UUIDs

## State Management Models
- `isLoading`: boolean - Indicates if the system is processing a request
- `error`: string | null - Error message if any error occurs
- `inputValue`: string - Current value in the input field

## Relationships
- `ChatSession` contains multiple `ChatMessage` objects
- `UserInput` triggers creation of a `ChatMessage` with role "user"
- `APIResponse` creates a `ChatMessage` with role "assistant"