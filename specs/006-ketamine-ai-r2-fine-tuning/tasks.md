# Implementation Tasks: Ketamine AI System with R2 Storage and Fine-Tuning

**Feature**: Ketamine AI System with R2 Storage and Fine-Tuning
**Branch**: `006-ketamine-ai-r2-fine-tuning`
**Generated**: 2026-01-18
**Input**: spec.md, plan.md, data-model.md, contracts/

## Implementation Strategy

Build an MVP focusing on US1 (Document Upload and Classification) first, then incrementally add US2 (Fine-tuning) and US3 (Knowledge Retrieval). Each user story is designed to be independently testable with clear acceptance criteria.

## Dependencies

- **US1 (P1)**: Foundation for all other stories - requires document processing pipeline
- **US2 (P2)**: Depends on US1 - needs processed documents to fine-tune
- **US3 (P3)**: Depends on US1 - needs processed knowledge base to query

## Parallel Execution Opportunities

- **US1 Tasks**: Models and services can be developed in parallel (T010-T020 range)
- **US2 Tasks**: Fine-tuning models and services can be developed in parallel (T030-T040 range)
- **US3 Tasks**: Chat models and services can be developed in parallel (T050-T060 range)
- **Frontend**: UI components for each story can be developed in parallel with backend

---

## Phase 1: Project Setup

**Goal**: Initialize the monorepo structure with backend and frontend components following the specified tech stack

- [ ] T001 Create project directory structure: backend/src, backend/tests, frontend/src, frontend/tests
- [ ] T002 [P] Initialize backend with FastAPI, SQLModel, pgvector dependencies in backend/requirements.txt
- [ ] T003 [P] Initialize frontend with Next.js 16+, Tailwind, Vercel AI SDK dependencies in frontend/package.json
- [ ] T004 Set up environment configuration files (.env.example) for both backend and frontend
- [ ] T005 Configure database migrations using Alembic for Neon DB with pgvector extension
- [X] T006 [P] Set up Cloudflare R2 integration with boto3 in backend configuration
- [ ] T007 Configure development and production deployment scripts
- [ ] T008 Set up basic CI/CD configuration files (GitHub Actions or similar)

---

## Phase 2: Foundational Components

**Goal**: Implement core infrastructure components needed by all user stories

- [ ] T009 Create base database models and establish connection patterns
- [ ] T010 [P] Create User model in backend/src/models/user.py with role-based access control
- [ ] T011 Create authentication middleware and JWT token handling in backend/src/middleware/auth.py
- [X] T012 Set up R2 storage service in backend/src/services/r2_storage.py
- [ ] T013 Implement vector store service in backend/src/services/vector_store.py with pgvector
- [ ] T014 Create document processing utilities in backend/src/utils/document_processor.py
- [ ] T015 [P] Set up Mistral API integration service in backend/src/services/document_classifier.py
- [ ] T016 Configure logging and monitoring infrastructure
- [ ] T017 Implement error handling and exception management patterns

---

## Phase 3: US1 - Document Upload and Classification (Priority: P1)

**Goal**: Enable admin users to upload medical documents and have them classified as relevant/irrelevant with storage in R2 and vector database

**Independent Test**: Can be fully tested by uploading various documents (ketamine-related and non-ketamine related) and verifying that relevant documents are properly stored in the vector database while irrelevant ones are marked accordingly.

- [X] T018 [US1] Create KnowledgeDoc model in backend/src/models/knowledge_doc.py following data model specifications
- [ ] T019 [US1] Create VectorChunk model in backend/src/models/vector_chunk.py following data model specifications
- [ ] T020 [US1] [P] Implement KnowledgeDoc CRUD operations in backend/src/services/knowledge_doc_service.py
- [ ] T021 [US1] [P] Implement VectorChunk CRUD operations in backend/src/services/vector_chunk_service.py
- [X] T022 [US1] [P] Create document ingestion pipeline in backend/src/services/document_ingestor.py
- [ ] T023 [US1] Implement PDF/DOCX parsing with PyPDF2/docx in backend/src/utils/document_parser.py
- [ ] T024 [US1] Create embedding generation service in backend/src/services/embedding_service.py
- [X] T025 [US1] [P] Create admin upload endpoint POST /api/admin/upload in backend/src/api/admin_routes.py
- [ ] T026 [US1] Implement file size validation and security checks for uploads
- [ ] T027 [US1] Create admin UI component for document upload in frontend/src/components/DocumentUpload.jsx
- [ ] T028 [US1] [P] Implement document upload form with progress tracking in frontend/src/pages/Admin.jsx
- [ ] T029 [US1] Create document listing page in frontend/src/pages/Admin.jsx with relevance status
- [ ] T030 [US1] [P] Add document approval workflow in frontend/src/components/AdminPanel.jsx
- [ ] T031 [US1] Implement acceptance test for ketamine-related document upload and processing
- [ ] T032 [US1] Implement acceptance test for non-ketamine document classification and storage

---

## Phase 4: US2 - AI Model Fine-Tuning (Priority: P2)

**Goal**: Enable system administrators to trigger the fine-tuning process to specialize the AI model for ketamine-related medical inquiries

**Independent Test**: Can be tested by triggering the fine-tuning endpoint and verifying that the system fetches all approved vector chunks, formats them into JSONL for instruction tuning, and initiates the fine-tuning process.

- [ ] T033 [US2] Create FineTuningJob model in backend/src/models/fine_tuning_job.py following data model specifications
- [ ] T034 [US2] Create ModelVersion model in backend/src/models/model_version.py following data model specifications
- [ ] T035 [US2] [P] Implement FineTuningJob service in backend/src/services/fine_tuning_service.py
- [ ] T036 [US2] [P] Implement ModelVersion service in backend/src/services/model_version_service.py
- [ ] T037 [US2] Create JSONL formatter for training data in backend/src/utils/training_data_formatter.py
- [ ] T038 [US2] [P] Implement training data fetcher in backend/src/services/training_data_service.py
- [ ] T039 [US2] Create fine-tuning API trigger in backend/src/services/fine_tuning_trigger.py
- [ ] T040 [US2] [P] Add fine-tuning endpoint POST /api/admin/train in backend/src/api/admin_routes.py
- [ ] T041 [US2] Implement model versioning and rollback functionality
- [ ] T042 [US2] [P] Create fine-tuning status monitoring in backend/src/services/job_monitor.py
- [ ] T043 [US2] Create admin UI for fine-tuning in frontend/src/components/FineTuningPanel.jsx
- [ ] T044 [US2] [P] Implement fine-tuning trigger form in frontend/src/pages/Admin.jsx
- [ ] T045 [US2] Add job status tracking UI in frontend/src/components/FineTuningStatus.jsx
- [ ] T046 [US2] Implement acceptance test for triggering fine-tuning with approved documents
- [ ] T047 [US2] Implement acceptance test for model version tracking and rollback

---

## Phase 5: US3 - Knowledge Retrieval for AI Responses (Priority: P3)

**Goal**: Enable healthcare professionals to ask questions about ketamine treatments and receive accurate, relevant answers based on the medical knowledge base

**Independent Test**: Can be tested by querying the system with ketamine-related questions and verifying that relevant knowledge from the processed documents is retrieved and used to generate accurate responses.

- [ ] T048 [US3] Create ChatSession model in backend/src/models/chat_session.py following data model specifications
- [ ] T049 [US3] Create ChatMessage model in backend/src/models/chat_message.py following data model specifications
- [ ] T050 [US3] [P] Implement ChatSession service in backend/src/services/chat_session_service.py
- [ ] T051 [US3] [P] Implement ChatMessage service in backend/src/services/chat_message_service.py
- [ ] T052 [US3] Create RAG (Retrieval Augmented Generation) service in backend/src/services/rag_service.py
- [ ] T053 [US3] [P] Implement vector similarity search in backend/src/services/vector_search_service.py
- [ ] T054 [US3] Create AI response generator using Mistral in backend/src/services/ai_response_service.py
- [ ] T055 [US3] [P] Add chat API endpoints in backend/src/api/chat_routes.py (POST /api/chat/sessions, POST /api/chat/sessions/{id}/messages)
- [ ] T056 [US3] Implement session management and history tracking
- [ ] T057 [US3] [P] Create chat interface component in frontend/src/components/ChatInterface.jsx
- [ ] T058 [US3] Implement chat page with session management in frontend/src/pages/Chat.jsx
- [ ] T059 [US3] [P] Add message display with source references in frontend/src/components/ChatMessage.jsx
- [ ] T060 [US3] Create current model info endpoint GET /api/chat/models/current
- [ ] T061 [US3] [P] Implement chat history sidebar in frontend/src/components/ChatHistory.jsx
- [ ] T062 [US3] Implement acceptance test for ketamine-related question and response generation
- [ ] T063 [US3] Implement acceptance test for source document reference in responses

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Enhance the system with additional features, error handling, and quality improvements across all components

- [ ] T064 Implement comprehensive error handling and user-friendly error messages
- [ ] T065 Add input validation and sanitization for all user inputs
- [ ] T066 [P] Enhance security with proper authentication and authorization for all endpoints
- [ ] T067 Add rate limiting and API usage monitoring
- [ ] T068 [P] Implement comprehensive logging for debugging and monitoring
- [ ] T069 Add caching mechanisms for frequently accessed data
- [ ] T070 [P] Conduct performance testing and optimization
- [ ] T071 Add comprehensive unit and integration tests for all services
- [ ] T072 [P] Implement end-to-end testing for all user stories
- [ ] T073 Create comprehensive documentation for API endpoints
- [ ] T074 [P] Add monitoring and alerting for system health
- [ ] T075 Conduct security review and penetration testing
- [ ] T076 [P] Prepare production deployment configuration
- [ ] T077 Perform final acceptance testing for all user stories
- [ ] T078 Prepare deployment scripts and rollback procedures