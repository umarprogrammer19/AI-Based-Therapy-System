# Data Model: Ketamine AI & Learning System

## Entity: KnowledgeDoc
**Description**: Represents an uploaded document with attributes for identification, filename, ketamine relevance status, and upload timestamp

**Fields**:
- id: UUID (Primary Key)
- filename: String (max 255 characters)
- is_ketamine_relevant: Boolean (indicates if document is related to ketamine therapy)
- uploaded_at: DateTime (timestamp of upload)
- uploader_id: String (identifier of the user who uploaded)
- file_size: Integer (size of the file in bytes)
- content_hash: String (hash of the content for deduplication)

**Validation Rules**:
- filename must not be empty
- uploaded_at must be in the past
- is_ketamine_relevant must be boolean

## Entity: VectorChunk
**Description**: Represents a processed segment of a document with associated embedding vector and content for retrieval

**Fields**:
- id: UUID (Primary Key)
- doc_id: UUID (Foreign Key to KnowledgeDoc)
- content: Text (the actual text content of the chunk)
- embedding: Vector (pgvector compatible embedding)
- chunk_index: Integer (position of chunk in original document)
- created_at: DateTime (timestamp of creation)

**Validation Rules**:
- doc_id must reference existing KnowledgeDoc
- content must not be empty
- embedding must be valid vector format
- chunk_index must be non-negative

## Entity: ChatSession
**Description**: Represents a user's chat session with a unique identifier and user information

**Fields**:
- id: UUID (Primary Key)
- user_identifier: String (identifier of the user)
- created_at: DateTime (timestamp of session creation)
- last_activity_at: DateTime (timestamp of last activity)
- is_active: Boolean (indicates if session is currently active)

**Validation Rules**:
- user_identifier must not be empty
- created_at must be in the past
- last_activity_at must be >= created_at

## Entity: ChatMessage
**Description**: Represents individual messages within a chat session with role (user/system) and content

**Fields**:
- id: UUID (Primary Key)
- session_id: UUID (Foreign Key to ChatSession)
- role: String (either "user" or "assistant")
- content: Text (the message content)
- timestamp: DateTime (when the message was sent)
- source_chunks: Array<String> (IDs of vector chunks referenced in response)

**Validation Rules**:
- session_id must reference existing ChatSession
- role must be either "user" or "assistant"
- content must not be empty
- timestamp must be in the past

## Relationships
- KnowledgeDoc (1) ←→ (0..*) VectorChunk
- ChatSession (1) ←→ (0..*) ChatMessage

## State Transitions
- KnowledgeDoc: Unprocessed → Classified (is_ketamine_relevant determined)
- ChatSession: Active → Inactive (after period of inactivity)