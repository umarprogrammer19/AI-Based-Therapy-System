# Data Model: Backend Foundation

## Entity Definitions

### KnowledgeDoc
- **Purpose**: Stores document metadata and information
- **Fields**:
  - id: UUID (primary key)
  - filename: str (name of the uploaded file)
  - file_size: int (size of the file in bytes)
  - upload_date: datetime (timestamp when document was uploaded)
  - source: str (where the document originated from)
  - content_type: str (MIME type of the document)
  - checksum: str (hash of the file for integrity checking)
  - metadata: JSON (additional document-specific metadata)
  - created_at: datetime (record creation timestamp)
  - updated_at: datetime (record update timestamp)

### VectorChunk
- **Purpose**: Stores text content with vector embeddings for similarity search
- **Fields**:
  - id: UUID (primary key)
  - knowledge_doc_id: UUID (foreign key to KnowledgeDoc)
  - text_content: str (the actual text content of the chunk)
  - embedding: Vector(384) (384-dimensional vector embedding)
  - chunk_index: int (order of the chunk within the original document)
  - chunk_metadata: JSON (metadata about the specific chunk)
  - similarity_score: float (cached similarity scores when applicable)
  - created_at: datetime (record creation timestamp)
  - updated_at: datetime (record update timestamp)

### AuditLog
- **Purpose**: Tracks system actions and events for monitoring and debugging
- **Fields**:
  - id: UUID (primary key)
  - action: str (type of action performed)
  - actor_id: str (identifier of who performed the action)
  - actor_type: str (type of actor - user, system, api)
  - resource_type: str (type of resource affected)
  - resource_id: str (identifier of the specific resource)
  - timestamp: datetime (when the action occurred)
  - details: JSON (additional information about the action)
  - severity: str (log level: info, warning, error, critical)
  - ip_address: str (IP address of the request, if applicable)
  - user_agent: str (user agent string, if applicable)

## Relationships
- KnowledgeDoc 1---* VectorChunk (one-to-many: one document to many chunks)
- Each VectorChunk belongs to exactly one KnowledgeDoc
- AuditLog references other entities through resource_type/resource_id

## Validation Rules
- KnowledgeDoc.filename must not be empty
- KnowledgeDoc.file_size must be non-negative
- VectorChunk.text_content must not be empty
- VectorChunk.embedding must have exactly 384 dimensions
- AuditLog.action must be one of predefined actions
- AuditLog.timestamp must be current or past (not future)

## Indexing Strategy
- KnowledgeDoc.id: Primary key index
- KnowledgeDoc.upload_date: Date-based query optimization
- VectorChunk.knowledge_doc_id: Foreign key index for joins
- VectorChunk.embedding: Vector index for similarity search (using pgvector)
- AuditLog.timestamp: Time-based query optimization
- AuditLog.action: Action-based filtering