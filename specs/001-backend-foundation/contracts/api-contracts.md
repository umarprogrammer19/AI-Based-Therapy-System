# API Contracts: Backend Foundation

## KnowledgeDoc API Contract

### GET /api/v1/knowledge-docs/
- **Purpose**: Retrieve a list of knowledge documents
- **Authentication**: Required
- **Query Parameters**:
  - limit: int (optional, default: 100) - Maximum number of records to return
  - offset: int (optional, default: 0) - Number of records to skip
  - sort: str (optional) - Sort field and direction (e.g., "upload_date:desc")
- **Responses**:
  - 200: Array of KnowledgeDoc objects
  - 401: Unauthorized
  - 500: Internal server error

### POST /api/v1/knowledge-docs/
- **Purpose**: Create a new knowledge document
- **Authentication**: Required
- **Request Body**: KnowledgeDocCreate object
- **Responses**:
  - 201: Created KnowledgeDoc object
  - 400: Invalid input
  - 401: Unauthorized
  - 409: Conflict (document already exists)
  - 500: Internal server error

### GET /api/v1/knowledge-docs/{id}
- **Purpose**: Retrieve a specific knowledge document
- **Authentication**: Required
- **Path Parameter**:
  - id: UUID - KnowledgeDoc identifier
- **Responses**:
  - 200: KnowledgeDoc object
  - 401: Unauthorized
  - 404: KnowledgeDoc not found
  - 500: Internal server error

### PUT /api/v1/knowledge-docs/{id}
- **Purpose**: Update a knowledge document
- **Authentication**: Required
- **Path Parameter**:
  - id: UUID - KnowledgeDoc identifier
- **Request Body**: KnowledgeDocUpdate object
- **Responses**:
  - 200: Updated KnowledgeDoc object
  - 400: Invalid input
  - 401: Unauthorized
  - 404: KnowledgeDoc not found
  - 500: Internal server error

### DELETE /api/v1/knowledge-docs/{id}
- **Purpose**: Delete a knowledge document
- **Authentication**: Required
- **Path Parameter**:
  - id: UUID - KnowledgeDoc identifier
- **Responses**:
  - 204: Successfully deleted
  - 401: Unauthorized
  - 404: KnowledgeDoc not found
  - 500: Internal server error

## VectorChunk API Contract

### GET /api/v1/vector-chunks/
- **Purpose**: Retrieve a list of vector chunks
- **Authentication**: Required
- **Query Parameters**:
  - knowledge_doc_id: UUID (optional) - Filter by knowledge document
  - limit: int (optional, default: 100) - Maximum number of records to return
  - offset: int (optional, default: 0) - Number of records to skip
- **Responses**:
  - 200: Array of VectorChunk objects
  - 401: Unauthorized
  - 500: Internal server error

### POST /api/v1/vector-chunks/
- **Purpose**: Create a new vector chunk
- **Authentication**: Required
- **Request Body**: VectorChunkCreate object
- **Responses**:
  - 201: Created VectorChunk object
  - 400: Invalid input (embedding dimension mismatch)
  - 401: Unauthorized
  - 500: Internal server error

### POST /api/v1/vector-chunks/search
- **Purpose**: Search for similar vector chunks using cosine similarity
- **Authentication**: Required
- **Request Body**: VectorSearchRequest object
  - query_embedding: Array[float] (384-dimensional vector)
  - limit: int (optional, default: 10) - Number of similar chunks to return
  - knowledge_doc_ids: Array[UUID] (optional) - Restrict search to specific documents
- **Responses**:
  - 200: Array of VectorChunkWithSimilarity objects
  - 400: Invalid input (embedding dimension mismatch)
  - 401: Unauthorized
  - 500: Internal server error

### GET /api/v1/vector-chunks/{id}
- **Purpose**: Retrieve a specific vector chunk
- **Authentication**: Required
- **Path Parameter**:
  - id: UUID - VectorChunk identifier
- **Responses**:
  - 200: VectorChunk object
  - 401: Unauthorized
  - 404: VectorChunk not found
  - 500: Internal server error

## AuditLog API Contract

### GET /api/v1/audit-logs/
- **Purpose**: Retrieve a list of audit logs
- **Authentication**: Required (admin privileges)
- **Query Parameters**:
  - action: str (optional) - Filter by action type
  - resource_type: str (optional) - Filter by resource type
  - start_date: str (optional) - Filter logs after this date
  - end_date: str (optional) - Filter logs before this date
  - limit: int (optional, default: 100) - Maximum number of records to return
  - offset: int (optional, default: 0) - Number of records to skip
- **Responses**:
  - 200: Array of AuditLog objects
  - 401: Unauthorized
  - 403: Forbidden (insufficient privileges)
  - 500: Internal server error

### GET /api/v1/audit-logs/{id}
- **Purpose**: Retrieve a specific audit log
- **Authentication**: Required (admin privileges)
- **Path Parameter**:
  - id: UUID - AuditLog identifier
- **Responses**:
  - 200: AuditLog object
  - 401: Unauthorized
  - 403: Forbidden (insufficient privileges)
  - 404: AuditLog not found
  - 500: Internal server error

## Health Check API Contract

### GET /health
- **Purpose**: Check the health status of the application
- **Authentication**: Not required
- **Responses**:
  - 200: Health status object with database connectivity
  - 503: Service unavailable (database connection issues)