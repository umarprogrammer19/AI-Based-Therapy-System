# Feature Specification: Ingestion Pipeline

**Feature Branch**: `002-ingestion-pipeline`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "@.claude/agents/rag-engineer.md I want to build the Ingestion Pipeline.

**Requirements**:
1. **Endpoint**: `POST /api/admin/upload`.
2. **Logic Flow**:
   - [cite_start]Receive file (PDF/TXT)[cite: 31].
   - **Step A (Classification)**: Send first 500 chars to Mistral. Ask: "Is this about Ketamine Therapy?".
   - **Step B (Branching)**:
     - [cite_start]If NO: Save to `KnowledgeDoc(relevant=False)` and STOP[cite: 49].
     - If YES: Save to `KnowledgeDoc(relevant=True)`.
   - **Step C (Processing)**:
     - Extract full text.
     - Split into 500-char chunks.
     - Embed using Hugging Face (MiniLM).
     - Save to `VectorChunk`. (branch name starts with 002)"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - File Upload and Classification (Priority: P1)

Admin users need to upload documents (PDF/TXT) to the system. The system automatically classifies whether the document is about Ketamine Therapy using AI classification. Documents classified as irrelevant are stored with a flag but not processed further, while relevant documents proceed to full processing.

**Why this priority**: This is the core functionality that enables the RAG system to selectively process relevant documents and avoid cluttering the knowledge base with irrelevant content.

**Independent Test**: Can be fully tested by uploading various documents (both ketamine therapy related and unrelated) and verifying that relevant documents are marked as such while irrelevant ones are flagged as not relevant and not processed further.

**Acceptance Scenarios**:

1. **Given** admin user has access to the system, **When** they upload a PDF document about ketamine therapy, **Then** the document is classified as relevant and marked for full processing
2. **Given** admin user uploads a document unrelated to ketamine therapy, **When** classification occurs, **Then** the document is saved as irrelevant and processing stops

---

### User Story 2 - Text Extraction and Chunking (Priority: P2)

For documents classified as relevant, the system extracts the full text content and splits it into manageable chunks of approximately 500 characters each for vector storage and retrieval.

**Why this priority**: This enables proper indexing of document content for semantic search, which is essential for the RAG system's effectiveness.

**Independent Test**: Can be tested by uploading a relevant document and verifying that it gets split into appropriately sized chunks without losing content integrity.

**Acceptance Scenarios**:

1. **Given** a relevant document has been classified, **When** text extraction occurs, **Then** the full text is successfully extracted without corruption
2. **Given** extracted text exists, **When** chunking occurs, **Then** text is split into approximately 500-character chunks with logical breaks between sentences/paragraphs

---

### User Story 3 - Vector Embedding and Storage (Priority: P3)

Processed document chunks are converted to vector embeddings using Hugging Face MiniLM model and stored in the vector database for similarity search capabilities.

**Why this priority**: This enables the core semantic search functionality that powers the RAG system's ability to retrieve relevant information.

**Independent Test**: Can be tested by uploading a document and verifying that vector embeddings are created and stored properly for later retrieval.

**Acceptance Scenarios**:

1. **Given** document chunks exist, **When** embedding process occurs, **Then** vector embeddings are generated using Hugging Face MiniLM
2. **Given** vector embeddings exist, **When** storage occurs, **Then** embeddings are saved to VectorChunk records with proper associations to source documents

---

### Edge Cases

- What happens when the uploaded file is corrupted or unreadable?
- How does system handle files exceeding maximum size limits?
- What occurs if the AI classification service is unavailable?
- How does the system handle documents with non-standard encodings or mixed languages?
- What happens if the Hugging Face embedding service fails during processing?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST accept file uploads via POST /api/admin/upload endpoint with PDF and TXT file formats
- **FR-002**: System MUST classify document relevance by sending first 500 characters to Mistral AI with query "Is this about Ketamine Therapy?"
- **FR-003**: System MUST save documents classified as irrelevant to KnowledgeDoc with relevant=False flag and halt further processing
- **FR-004**: System MUST save documents classified as relevant to KnowledgeDoc with relevant=True flag and continue processing
- **FR-005**: System MUST extract full text content from uploaded PDF and TXT files
- **FR-006**: System MUST split extracted text into approximately 500-character chunks with intelligent boundary detection
- **FR-007**: System MUST generate vector embeddings using Hugging Face MiniLM model for each text chunk
- **FR-008**: System MUST store vector embeddings in VectorChunk records linked to the source KnowledgeDoc
- **FR-009**: System MUST handle file upload errors gracefully with appropriate error responses
- **FR-010**: System MUST maintain associations between KnowledgeDoc and its related VectorChunk records

*Example of marking unclear requirements:*

- **FR-011**: System MUST handle file size limits of 50MB maximum per document
- **FR-012**: System MUST maintain processing timeouts of 60 seconds before failing gracefully
- **FR-013**: System MUST preserve text formatting during extraction for PDF documents to maintain structural information

### Key Entities *(include if feature involves data)*

- **KnowledgeDoc**: Represents an uploaded knowledge document with metadata including file information, relevance classification, and processing status
- **VectorChunk**: Contains text content chunks and their vector embeddings for similarity search operations, linked to source KnowledgeDoc
- **UploadSession**: Represents a file upload and processing session with status tracking and error handling

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Admin users can successfully upload PDF and TXT documents through the API endpoint with 95% success rate
- **SC-002**: Document classification accuracy for ketamine therapy relevance achieves 90% precision based on manual verification samples
- **SC-003**: System processes and stores document vectors within 30 seconds per average-sized document (10 pages/5000 words)
- **SC-004**: 99% of uploaded documents are properly categorized as relevant or irrelevant without system errors
- **SC-005**: Text extraction preserves 98% of original content without corruption across PDF and TXT formats
- **SC-006**: Semantic search returns relevant results within 500ms response time for 95% of queries