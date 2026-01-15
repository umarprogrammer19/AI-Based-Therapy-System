# Tasks: Ketamine AI & Learning System

**Feature**: Ketamine AI & Learning System
**Branch**: 005-ketamine-ai-system
**Created**: 2026-01-15
**Based on**: specs/005-ketamine-ai-system/spec.md, specs/005-ketamine-ai-system/plan.md

## Implementation Strategy

**MVP Approach**: Implement core chat functionality first (US1), then add document ingestion (US2), then admin features (US3).

**Parallel Opportunities**: Database models and API endpoints can be developed in parallel where they don't share dependencies.

**Independent Test Criteria**:
- US1: Users can submit ketamine therapy queries and receive responses
- US2: Admins can upload documents and see classification results
- US3: Admins can view knowledge base and audit logs

## Phase 1: Setup

- [X] T001 Create backend directory structure: backend/src/{models,services,api,database,utils}
- [ ] T002 Create frontend directory structure: frontend/src/{app,components,pages,styles,types,utils}
- [X] T003 Initialize Python project with requirements.txt for FastAPI, SQLModel, pgvector
- [ ] T004 Initialize Next.js project with package.json dependencies
- [X] T005 Create initial .gitignore for Python/Node.js project
- [X] T006 Set up database connection configuration in backend

## Phase 2: Foundational

- [X] T007 Create database models: KnowledgeDoc, VectorChunk, ChatSession, ChatMessage
- [X] T008 Set up database migration to enable vector extension
- [X] T009 Create database initialization script
- [X] T010 Implement basic FastAPI app structure
- [X] T011 Create SQLModel base class and engine setup

## Phase 3: [US1] Ketamine Therapy Information Query

- [X] T012 [US1] Create chat endpoint POST /api/chat
- [X] T013 [US1] Implement RAG service for retrieving relevant chunks
- [X] T014 [US1] Implement chat service with Mistral integration
- [ ] T015 [US1] Create frontend chat interface component
- [ ] T016 [US1] Implement streaming responses in frontend
- [ ] T017 [US1] Add medical disclaimer to frontend

## Phase 4: [US2] Document Upload and Classification

- [X] T018 [US2] Create upload endpoint POST /api/upload
- [X] T019 [US2] Implement document classification service
- [X] T020 [US2] Create document processing pipeline
- [X] T021 [US2] Implement text extraction for PDF, DOCX, TXT, MD
- [X] T022 [US2] Implement embedding generation and storage
- [ ] T023 [US2] Create file upload zone component in frontend

## Phase 5: [US3] Admin Knowledge Management

- [X] T024 [US3] Create admin endpoints for document listing
- [X] T025 [US3] Create admin endpoints for audit logs
- [X] T026 [US3] Implement admin authentication with API key
- [ ] T027 [US3] Create knowledge base view component
- [ ] T028 [US3] Create audit log view component
- [ ] T029 [US3] Implement admin panel UI

## Phase 6: Polish & Cross-Cutting

- [ ] T030 Add API key protection to admin routes
- [ ] T031 Implement error handling and logging
- [ ] T032 Add input validation and sanitization
- [ ] T033 Write integration tests for core functionality
- [ ] T034 Update documentation with API usage
- [ ] T035 Perform final testing and bug fixes

## Dependencies

- **US2 depends on**: US1 (needs chat infrastructure for response generation)
- **US3 depends on**: US1, US2 (needs both chat and document management)

## Parallel Execution Examples

- T001-T002: Backend and frontend structure can be created in parallel
- T012-T013: Endpoint and service can be developed in parallel with agreed interface
- T018-T019: Upload endpoint and classification service can be developed in parallel
- T024-T025: Admin endpoints can be developed in parallel