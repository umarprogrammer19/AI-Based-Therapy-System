# Feature Specification: Ketamine AI & Learning System

**Feature Branch**: `005-ketamine-ai-system`
**Created**: 2026-01-15
**Status**: Draft
**Input**: User description: "I want to define the Master Spec for the \"Ketamine AI & Learning System\".

**1. System Architecture**
- **Monorepo**: \`frontend/\` (Next.js) and \`backend/\` (FastAPI).
- **Dual Storage Strategy**[cite: 52]:
  - **Store A (Ketamine Knowledge)**: Stores vector embeddings of approved PDFs/Docs. Used for RAG.
  - **Store B (General Storage)**: Stores raw Chat History, User Logs, and \"Non-Training\" files.

**2. Backend Features (FastAPI)**
- **Auth**: API Key protection for Admin routes.
- **Ingestion Pipeline** [cite: 36-50]:
  - \`POST /api/upload\`: Accepts PDF/DOCX/TXT/MD.
  - **Step 1 (Classify)**: Ask Mistral \"Is this regarding Ketamine Therapy?\".
  - **Step 2 (Route)**:
    - *If Yes*: Extract Text -> Chunk -> Embed -> Store in \`vectors_ketamine\`.
    - *If No*: Save Metadata to \`admin_logs\` -> Mark \"NON-TRAINING\" -> Do NOT Embed.
- **Chat API**[cite: 10]:
  - \`POST /api/chat\`:
  - **Step 1**: Check if query is off-topic[cite: 17].
  - **Step 2**: Retrieve top 3 relevant chunks from \`vectors_ketamine\`.
  - **Step 3**: Generate response using Mistral with System Prompt[cite: 88].

**3. Frontend Features (Next.js)**
- **User Interface**[cite: 11]:
  - Chat Window (Streaming responses).
  - \"Medical Disclaimer\" footer visible at all times[cite: 95].
- **Admin Panel**[cite: 100]:
  - File Upload Zone.
  - \"Knowledge Base\" View: List all files with status (Training / Non-Training).
  - \"Audit Log\": View who uploaded what[cite: 96].

**4. Data Models (SQLModel)**
- \`KnowledgeDoc\`: id, filename, is_ketamine_relevant (bool), uploaded_at.
- \`VectorChunk\`: id, doc_id, embedding (vector), content.
- \`ChatSession\`: id, user_identifier.
- \`ChatMessage\`: id, session_id, role, content."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ketamine Therapy Information Query (Priority: P1)

As a user seeking information about ketamine therapy, I want to be able to ask questions and receive accurate, relevant responses based on approved ketamine therapy knowledge, so that I can learn about ketamine therapy safely and effectively.

**Why this priority**: This is the core value proposition of the system - providing reliable ketamine therapy information to users.

**Independent Test**: Can be fully tested by submitting various ketamine therapy-related queries and verifying that responses are accurate, relevant, and come from the knowledge base, delivering educational value.

**Acceptance Scenarios**:

1. **Given** a user has a question about ketamine therapy, **When** they submit the query through the chat interface, **Then** they receive a relevant, accurate response based on the knowledge base within 5 seconds.
2. **Given** a user submits an off-topic query, **When** they submit the query, **Then** the system recognizes it as off-topic and responds appropriately without providing unrelated medical advice.

---

### User Story 2 - Document Upload and Classification (Priority: P2)

As an admin user, I want to upload documents and have them automatically classified as ketamine-related or non-related, so that only relevant information enters the knowledge base while maintaining an audit trail of all uploads.

**Why this priority**: Critical for maintaining the integrity of the knowledge base and ensuring the system operates within its intended scope.

**Independent Test**: Can be fully tested by uploading various documents (ketamine-related and non-related) and verifying they are correctly classified and routed to appropriate storage, delivering data quality assurance.

**Acceptance Scenarios**:

1. **Given** an admin user uploads a ketamine therapy document, **When** the system processes it, **Then** the document is classified as ketamine-related, extracted, chunked, embedded, and stored in the ketamine knowledge store.
2. **Given** an admin user uploads a non-ketamine therapy document, **When** the system processes it, **Then** the document is classified as non-related, metadata is saved to admin logs, marked as "NON-TRAINING", and not embedded.

---

### User Story 3 - Admin Knowledge Management (Priority: P3)

As an admin user, I want to view the knowledge base with document status and audit logs, so that I can monitor what content is being used for training and maintain oversight of the system.

**Why this priority**: Essential for administrative control and compliance monitoring of the system's content.

**Independent Test**: Can be fully tested by accessing the admin panel and viewing the knowledge base and audit logs, delivering administrative oversight capability.

**Acceptance Scenarios**:

1. **Given** an admin user accesses the admin panel, **When** they view the knowledge base, **Then** they see a list of all files with their status (Training/Non-Training).
2. **Given** an admin user accesses the admin panel, **When** they view the audit log, **Then** they can see who uploaded what documents with timestamps.

---

### Edge Cases

- What happens when a user submits a query that appears to seek medical diagnosis rather than education?
- How does the system handle very large documents during the upload process?
- What occurs when the AI classification is uncertain about whether content is ketamine-related?
- How does the system handle concurrent users during peak usage periods?
- What happens when a user uploads a document in an unsupported format?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept PDF, DOCX, and TXT file uploads through the admin interface
- **FR-002**: System MUST classify uploaded documents using AI to determine if they are related to ketamine therapy
- **FR-003**: System MUST route ketamine-related documents to the knowledge store with text extraction, chunking, and embedding
- **FR-004**: System MUST route non-ketamine-related documents to admin logs with "NON-TRAINING" designation without embedding
- **FR-005**: System MUST provide a chat interface that retrieves relevant information from the ketamine knowledge store
- **FR-006**: System MUST use a RAG (Retrieval Augmented Generation) approach to answer user queries
- **FR-007**: System MUST apply the system prompt "You are a medical information assistant specializing ONLY in ketamine therapy" when generating responses
- **FR-008**: System MUST include a medical disclaimer visible at all times in the user interface
- **FR-009**: System MUST provide streaming responses in the chat window
- **FR-010**: System MUST protect admin routes with API key authentication
- **FR-011**: System MUST store user chat history and logs separately from the knowledge base
- **FR-012**: System MUST provide an admin panel showing all uploaded files with their training status
- **FR-013**: System MUST provide an audit log showing who uploaded what documents with timestamps
- **FR-014**: System MUST retrieve the top 3 relevant chunks from the ketamine knowledge store when answering queries
- **FR-015**: System MUST check if user queries are off-topic before retrieving relevant information

### Key Entities *(include if feature involves data)*

- **KnowledgeDoc**: Represents an uploaded document with attributes for identification, filename, ketamine relevance status, and upload timestamp
- **VectorChunk**: Represents a processed segment of a document with associated embedding vector and content for retrieval
- **ChatSession**: Represents a user's chat session with a unique identifier and user information
- **ChatMessage**: Represents individual messages within a chat session with role (user/system) and content

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can submit ketamine therapy queries and receive relevant responses within 5 seconds in 95% of cases
- **SC-002**: The system correctly classifies 90% of uploaded documents as ketamine-related or non-related
- **SC-003**: At least 95% of ketamine therapy queries receive responses based on relevant information from the knowledge base
- **SC-004**: The system processes and stores 100% of uploaded documents according to their classification (training vs non-training)
- **SC-005**: Admin users can access and view all uploaded documents with their status and audit information within 2 seconds
- **SC-006**: The medical disclaimer is visible at all times during user interactions with 100% consistency
- **SC-007**: The system handles 100 concurrent users without degradation in response time or accuracy
