# Data Model: Ingestion Pipeline

## Overview
Data models for the ingestion pipeline including document metadata, processing status, and upload session tracking.

## KnowledgeDoc Updates
**Fields**:
- `id`: UUID (primary key)
- `filename`: String (required) - name of the uploaded file
- `file_size`: Integer (required, positive) - size of the file in bytes
- `source`: String (required) - source location of the document
- `content_type`: String (optional) - MIME type of the document
- `checksum`: String (optional) - hash of the file for integrity checking
- `doc_metadata`: JSON (optional) - additional document-specific metadata
- `upload_date`: DateTime (auto-generated) - timestamp when document was uploaded
- `created_at`: DateTime (auto-generated) - record creation timestamp
- `updated_at`: DateTime (auto-generated) - record update timestamp
- `relevant`: Boolean (required) - whether document is relevant to ketamine therapy (classification result)
- `classification_reason`: String (optional) - reason for classification decision
- `processing_status`: String (required) - current status (uploaded, classified, processing, completed, failed)
- `error_message`: String (optional) - error details if processing failed

**Validation Rules**:
- `file_size` must be greater than 0
- `filename` must not be empty
- `source` must not be empty
- `relevant` must be set after classification

## VectorChunk Updates
**Fields**:
- `id`: UUID (primary key)
- `knowledge_doc_id`: UUID (foreign key) - reference to parent KnowledgeDoc
- `text_content`: String (required) - the actual text content of the chunk
- `embedding`: Array[Float] (required) - 384-dimensional vector embedding
- `chunk_index`: Integer (required) - order of the chunk within the original document
- `chunk_metadata`: JSON (optional) - metadata about the specific chunk
- `similarity_score`: Float (optional) - cached similarity scores when applicable
- `created_at`: DateTime (auto-generated) - record creation timestamp
- `updated_at`: DateTime (auto-generated) - record update timestamp

**Validation Rules**:
- `chunk_index` must be non-negative
- `text_content` must not be empty
- `embedding` must have exactly 384 dimensions
- `knowledge_doc_id` must reference an existing KnowledgeDoc

## New: UploadSession Model
**Fields**:
- `id`: UUID (primary key)
- `user_id`: String (required) - ID of the user who initiated the upload
- `knowledge_doc_id`: UUID (foreign key) - reference to associated KnowledgeDoc
- `original_filename`: String (required) - original name of uploaded file
- `file_path`: String (optional) - temporary storage path
- `file_size`: Integer (required) - size of uploaded file
- `status`: String (required) - current status (uploading, uploaded, processing, completed, failed)
- `progress`: Float (optional) - processing progress percentage (0.0 to 1.0)
- `started_at`: DateTime (auto-generated) - when upload started
- `completed_at`: DateTime (optional) - when processing completed
- `error_details`: String (optional) - error details if upload failed

**Validation Rules**:
- `status` must be one of the predefined values
- `progress` must be between 0.0 and 1.0
- `file_size` must be greater than 0

## Relationships
- `UploadSession` → `KnowledgeDoc` (one-to-one relationship)
- `KnowledgeDoc` → `VectorChunk` (one-to-many relationship)

## State Transitions for Processing Status
- `uploaded` → `classified` → `processing` → `completed`
- `uploaded` → `classified` → `skipped` (for irrelevant documents)
- Any status → `failed` (on error)

## Indexes
- Index on `KnowledgeDoc.relevant` for efficient filtering
- Index on `KnowledgeDoc.processing_status` for processing queue management
- Index on `KnowledgeDoc.upload_date` for chronological ordering
- Index on `VectorChunk.knowledge_doc_id` for document-chunk lookup