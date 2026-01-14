---
description: "Task list for ingestion pipeline implementation"
---

# Tasks: Ingestion Pipeline

**Input**: Design documents from `/specs/002-ingestion-pipeline/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `tests/`
- **Backend service**: Following the existing backend foundation structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Install required dependencies for ingestion pipeline in backend/requirements.txt
- [ ] T002 [P] Set up file processing libraries (PyPDF2/fitz, python-docx) in backend/requirements.txt
- [ ] T003 [P] Set up Hugging Face API integration dependencies in backend/requirements.txt

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Update KnowledgeDoc model with ingestion-specific fields in backend/src/models/knowledge_doc.py
- [ ] T005 Create VectorChunk model for storing text chunks and embeddings in backend/src/models/vector_chunk.py
- [ ] T006 Create UploadSession model for tracking upload processing in backend/src/models/upload_session.py
- [ ] T007 Set up database migration for new models in backend/migrations/
- [ ] T008 [P] Configure Hugging Face API client in backend/src/config/settings.py
- [ ] T009 [P] Set up environment variables for AI services in backend/.env.example

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - File Upload and Classification (Priority: P1) 🎯 MVP

**Goal**: Admin users can upload documents (PDF/TXT) which are automatically classified as ketamine therapy related or not using AI classification.

**Independent Test**: Can be fully tested by uploading various documents (both ketamine therapy related and unrelated) and verifying that relevant documents are marked as such while irrelevant ones are flagged as not relevant and not processed further.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for POST /api/admin/upload endpoint in backend/tests/contract/test_upload.py
- [ ] T011 [P] [US1] Integration test for document classification workflow in backend/tests/integration/test_classification.py

### Implementation for User Story 1

- [ ] T012 [US1] Implement file upload endpoint POST /api/admin/upload in backend/src/api/v1/knowledge_docs.py
- [ ] T013 [US1] Create document classification service using Mistral AI in backend/src/services/ai.py
- [ ] T014 [US1] Implement logic to send first 500 characters to Mistral for relevance check in backend/src/services/ingestion.py
- [ ] T015 [US1] Update KnowledgeDoc with classification results (relevant=True/False) in backend/src/services/knowledge_service.py
- [ ] T016 [US1] Implement branching logic: save irrelevant docs and stop processing vs continue for relevant docs in backend/src/services/ingestion.py
- [ ] T017 [US1] Add file type validation (PDF/TXT) in backend/src/utils/validators.py
- [ ] T018 [US1] Add file size validation (max 50MB) in backend/src/utils/validators.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Text Extraction and Chunking (Priority: P2)

**Goal**: For documents classified as relevant, the system extracts the full text content and splits it into manageable chunks of approximately 500 characters each for vector storage and retrieval.

**Independent Test**: Can be tested by uploading a relevant document and verifying that it gets split into appropriately sized chunks without losing content integrity.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Contract test for text extraction functionality in backend/tests/contract/test_extraction.py
- [ ] T020 [P] [US2] Integration test for document chunking workflow in backend/tests/integration/test_chunking.py

### Implementation for User Story 2

- [ ] T021 [US2] Implement PDF text extraction using fitz in backend/src/services/ingestion.py
- [ ] T022 [US2] Implement TXT text extraction in backend/src/services/ingestion.py
- [ ] T023 [US2] Implement sentence-aware text chunking algorithm (~500 chars) in backend/src/services/ingestion.py
- [ ] T024 [US2] Create VectorChunk records with extracted text in backend/src/services/vector_service.py
- [ ] T025 [US2] Link VectorChunks to parent KnowledgeDoc in backend/src/services/vector_service.py
- [ ] T026 [US2] Add text extraction error handling in backend/src/services/ingestion.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Vector Embedding and Storage (Priority: P3)

**Goal**: Processed document chunks are converted to vector embeddings using Hugging Face MiniLM model and stored in the vector database for similarity search capabilities.

**Independent Test**: Can be tested by uploading a document and verifying that vector embeddings are created and stored properly for later retrieval.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Contract test for embedding generation in backend/tests/contract/test_embeddings.py
- [ ] T028 [P] [US3] Integration test for complete ingestion pipeline in backend/tests/integration/test_pipeline.py

### Implementation for User Story 3

- [ ] T029 [US3] Implement Hugging Face MiniLM embedding generation in backend/src/services/ai.py
- [ ] T030 [US3] Store vector embeddings in VectorChunk records in backend/src/services/vector_service.py
- [ ] T031 [US3] Ensure pgvector compatibility for embedding storage in backend/src/models/vector_chunk.py
- [ ] T032 [US3] Add embedding generation error handling in backend/src/services/ai.py
- [ ] T033 [US3] Optimize embedding batch processing in backend/src/services/ai.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T034 [P] Add comprehensive logging for ingestion pipeline in backend/src/utils/logging.py
- [ ] T035 [P] Add processing status tracking in UploadSession model in backend/src/models/upload_session.py
- [ ] T036 Add error handling and graceful failure mechanisms across all services
- [ ] T037 [P] Add progress tracking for long-running uploads in backend/src/services/ingestion.py
- [ ] T038 Add audit logging for all document processing activities in backend/src/services/audit_service.py
- [ ] T039 [P] Update API documentation for new endpoints in backend/docs/api.md
- [ ] T040 Run complete ingestion pipeline test with sample documents

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 completion - processes only relevant documents
- **User Story 3 (P3)**: Depends on User Story 2 completion - requires text chunks to embed

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /api/admin/upload endpoint in backend/tests/contract/test_upload.py"
Task: "Integration test for document classification workflow in backend/tests/integration/test_classification.py"

# Launch all models for User Story 1 together:
Task: "Create document classification service using Mistral AI in backend/src/services/ai.py"
Task: "Update KnowledgeDoc with classification results in backend/src/services/knowledge_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 (waits for US1)
   - Developer C: User Story 3 (waits for US2)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence