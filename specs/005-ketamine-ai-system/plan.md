# Implementation Plan: Ketamine AI & Learning System

**Branch**: `005-ketamine-ai-system` | **Date**: 2026-01-15 | **Spec**: specs/005-ketamine-ai-system/spec.md
**Input**: Feature specification from `/specs/005-ketamine-ai-system/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Ketamine AI & Learning System with dual storage strategy: a ketamine knowledge store for vector embeddings of approved documents (used for RAG) and general storage for chat history and logs. The system features an ingestion pipeline that classifies uploaded documents using AI to determine ketamine relevance, with ketamine-related documents being chunked and embedded while non-related documents are logged for audit purposes only. The frontend provides a chat interface with streaming responses and admin panel for document management.

## Technical Context

**Language/Version**: Python 3.13 (Backend), JavaScript/TypeScript (Frontend)
**Primary Dependencies**: FastAPI (Backend), Next.js 16+ (Frontend), pgvector (PostgreSQL extension), SQLModel, Mistral API (Hugging Face), Vercel AI SDK
**Storage**: Neon Serverless PostgreSQL with pgvector extension for vector storage
**Testing**: pytest (Backend), Jest/Vitest (Frontend)
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web (monorepo with frontend and backend components)
**Performance Goals**: 95% of queries responded within 5 seconds, 90% document classification accuracy
**Constraints**: <500ms vector search performance, API key protection for admin routes, medical disclaimer always visible
**Scale/Scope**: Support for 100 concurrent users, proper separation of ketamine knowledge vs general storage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Project Mission Compliance**: ✅ The system adheres to "Knowledge Separation" architecture with strict focus on ketamine therapy knowledge. Non-relevant data is stored separately and never vector-indexed as required.

**Tech Stack Standards Compliance**: ✅ Uses specified technologies: Frontend: Next.js 16+ (App Router), Tailwind CSS, Vercel AI SDK. Backend: Python FastAPI, Uvicorn. Database: Neon Serverless PostgreSQL with pgvector for ketamine knowledge store and standard tables for general storage.

**Core Logic Rules Compliance**: ✅ Implements ingestion pipeline with AI classification step for all uploads. System prompt is "You are a medical information assistant specializing ONLY in ketamine therapy". Safety constraint implemented with no medical diagnoses, strictly educational.

**Documentation Compliance**: ✅ Maintains specs/ folder with architecture diagrams and API definitions as required.

## Project Structure

### Documentation (this feature)

```text
specs/005-ketamine-ai-system/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── knowledge_doc.py      # KnowledgeDoc entity
│   │   ├── vector_chunk.py       # VectorChunk entity
│   │   ├── chat_session.py       # ChatSession entity
│   │   └── chat_message.py       # ChatMessage entity
│   ├── services/
│   │   ├── ingestion_service.py  # Document classification and processing
│   │   ├── rag_service.py        # RAG operations
│   │   ├── chat_service.py       # Chat functionality
│   │   └── classification_service.py  # AI classification
│   ├── api/
│   │   ├── main.py               # Main API router
│   │   ├── upload_router.py      # Upload endpoint
│   │   ├── chat_router.py        # Chat endpoint
│   │   └── admin_router.py       # Admin endpoints
│   ├── database/
│   │   ├── connection.py         # DB connection
│   │   └── init_db.py            # DB initialization
│   └── utils/
│       ├── file_utils.py         # File processing utilities
│       ├── text_extractor.py     # Text extraction from documents
│       └── embeddings.py         # Embedding utilities
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chatService.ts    # Chat API calls
│   │   │   ├── uploadService.ts  # Upload API calls
│   │   │   └── adminService.ts   # Admin API calls
│   │   ├── components/
│   │   │   ├── ChatWindow.tsx    # Chat interface
│   │   │   ├── MedicalDisclaimer.tsx  # Disclaimer component
│   │   │   ├── FileUploadZone.tsx     # Upload component
│   │   │   ├── KnowledgeBaseView.tsx  # Knowledge base view
│   │   │   └── AuditLogView.tsx       # Audit log view
│   │   ├── pages/
│   │   │   ├── chat.tsx          # Chat page
│   │   │   ├── admin.tsx         # Admin panel
│   │   │   └── index.tsx         # Home page
│   │   └── utils/
│   │       └── streamingUtils.ts # Streaming response utilities
│   ├── styles/
│   │   └── globals.css           # Global styles with Tailwind
│   └── types/
│       └── index.ts              # Type definitions
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Selected Option 2: Web application structure to accommodate the monorepo architecture with separate frontend (Next.js) and backend (FastAPI) components as specified in the feature requirements.

## Phase 1 Status

**Completed Artifacts**:
- research.md: Technical decisions and rationale documented
- data-model.md: Complete data model with entities, fields, validation rules, and relationships
- contracts/: API contracts for chat, upload, and admin endpoints
- quickstart.md: Complete setup and usage guide
- Agent context: Updated CLAUDE.md with new technologies for this feature

## Complexity Tracking

Not applicable - No Constitution Check violations identified that require justification.
