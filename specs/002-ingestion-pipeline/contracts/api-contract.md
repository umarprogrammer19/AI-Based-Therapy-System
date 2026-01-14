# API Contract: Document Ingestion

## Endpoint: POST /api/admin/upload

### Description
Uploads a document for processing through the AI classification and vectorization pipeline.

### Request
**Method**: POST
**Path**: `/api/admin/upload`
**Content-Type**: `multipart/form-data`

#### Parameters
- `file`: (Required) File upload - PDF or TXT format
  - Type: binary file
  - Size limit: 50MB maximum
  - Supported formats: PDF, TXT

### Response Codes
- `200 OK`: Document processed successfully
- `400 Bad Request`: Invalid file format or malformed request
- `413 Payload Too Large`: File exceeds size limits
- `422 Unprocessable Entity`: File type not supported
- `500 Internal Server Error`: Processing error

### Successful Response (200)
```json
{
  "id": "uuid-string",
  "filename": "original_filename.pdf",
  "file_size": 123456,
  "content_type": "application/pdf",
  "relevant": true,
  "processing_status": "completed",
  "chunks_created": 23,
  "message": "Document processed successfully"
}
```

### Failed Response (400, 413, 422, 500)
```json
{
  "detail": "Error description"
}
```

### Processing Flow
1. Receive file upload
2. Validate file format and size
3. Extract first 500 characters
4. Send to AI classifier with query "Is this about Ketamine Therapy?"
5. Based on classification result:
   - If NO: Save as KnowledgeDoc(relevant=False), stop processing
   - If YES: Continue to full processing
6. Extract full text content
7. Split into 500-character chunks
8. Generate embeddings using Hugging Face MiniLM
9. Save chunks to VectorChunk records
10. Return processing results

### Security
- Admin authentication required
- Rate limiting applied
- File type validation enforced
- Size validation enforced

### Examples

#### Successful Upload
```
POST /api/admin/upload
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="ketamine_research.pdf"
Content-Type: application/pdf

[file binary data]
------WebKitFormBoundary--
```

#### Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "filename": "ketamine_research.pdf",
  "file_size": 245760,
  "content_type": "application/pdf",
  "relevant": true,
  "processing_status": "completed",
  "chunks_created": 15,
  "message": "Document processed successfully and vectorized"
}
```