# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of the ingestion pipeline to handle document uploads with AI classification for ketamine therapy relevance. The pipeline will receive PDF/TXT files via the POST /api/admin/upload endpoint, classify them using Mistral AI to determine if they're related to ketamine therapy, and then either store them as irrelevant (with metadata only) or process them through text extraction, chunking, and vector embedding using Hugging Face MiniLM model. This aligns with the Knowledge Firewall Rule in the constitution by maintaining strict separation between ketamine-related and general content.

## Technical Context

**Language/Version**: Python 3.13 (as established in the backend foundation)
**Primary Dependencies**: FastAPI, SQLModel, Hugging Face API, pgvector, PyPDF2/fitz for PDF processing, python-docx for DOCX processing
**Storage**: Neon Serverless PostgreSQL with pgvector for vector storage, SQLModel for structured data
**Testing**: pytest with coverage reporting, integration tests for API endpoints
**Target Platform**: Linux server (containerized with Docker)
**Project Type**: Backend service component of web application
**Performance Goals**: Process and store document vectors within 30 seconds per average-sized document (10 pages/5000 words), maintain <500ms response time for vector similarity searches
**Constraints**: File size limits of 50MB maximum per document, processing timeouts of 60 seconds, must maintain separation between "Ketamine Knowledge" and "General Data" as per constitution
**Scale/Scope**: Support for concurrent document uploads, maintain 99% accuracy in document classification for ketamine therapy relevance

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Project Mission Compliance**: The ingestion pipeline supports the mission of building a specialized Ketamine Therapy AI by ensuring only approved uploads are processed into the knowledge base. The classification step ensures that only ketamine-related documents are vectorized.

2. **Architecture Standards Compliance**: Uses the mandated technology stack - FastAPI backend with Neon Serverless PostgreSQL and pgvector for knowledge storage, Hugging Face API for AI classification and embeddings.

3. **Knowledge Firewall Rule Compliance**: Implements the required classification step - every uploaded file is classified by AI. Ketamine-related documents will be chunked and embedded into vectors_ketamine, while non-related documents will only have metadata logged without vectorization.

4. **Data Security Compliance**: Will implement proper access controls for the admin upload endpoint and maintain audit logs for all document processing activities.

5. **Quality Assurance Compliance**: The classification accuracy requirement (90% precision) aligns with the quality standards for medical AI applications.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
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
│   │   ├── knowledge_doc.py
│   │   ├── vector_chunk.py
│   │   └── audit_log.py
│   ├── services/
│   │   ├── ingestion.py      # NEW: Handles document upload, classification, and processing
│   │   ├── ai.py             # NEW: Manages AI interactions (classification, embeddings)
│   │   ├── knowledge_service.py
│   │   ├── vector_service.py
│   │   └── audit_service.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── knowledge_docs.py
│   │       ├── vector_chunks.py
│   │       └── audit_logs.py
│   ├── config/
│   │   ├── database.py
│   │   └── settings.py
│   └── utils/
│       ├── security.py
│       └── validators.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

**Structure Decision**: Selected Option 2: Web application structure with backend/ directory containing the FastAPI application. The ingestion and AI services will be added to the existing services/ directory as specified in the user request. This maintains consistency with the existing backend foundation and follows the established architecture patterns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations identified. All design decisions align with the Ketamine Therapy AI Constitution.
