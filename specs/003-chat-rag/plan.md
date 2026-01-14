# Implementation Plan: Chat Endpoint with RAG

**Branch**: `003-chat-rag` | **Date**: 2026-01-14 | **Spec**: [link]
**Input**: Feature specification from `/specs/003-chat-rag/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a chat endpoint with RAG (Retrieval-Augmented Generation) functionality that allows users to interact with a ketamine therapy knowledge base. The system receives user queries, implements guardrail logic to detect off-topic queries, converts queries to vectors for similarity search against VectorChunk records, and generates contextual responses using the Mistral AI model with appropriate system prompts.

## Technical Context

**Language/Version**: Python 3.13 (as established in the backend foundation)
**Primary Dependencies**: FastAPI, SQLModel, Hugging Face API, pgvector, sentence-transformers, Pydantic
**Storage**: Neon Serverless PostgreSQL with pgvector for vector storage, SQLModel for structured data
**Testing**: pytest with coverage reporting, integration tests for API endpoints
**Target Platform**: Linux server (containerized with Docker)
**Project Type**: Backend service component of web application
**Performance Goals**: Respond to queries within 10 seconds under normal load, maintain <500ms response time for vector similarity searches
**Constraints**: Must follow Knowledge Firewall Rule - only use ketamine-related context for responses, implement guardrails for off-topic queries
**Scale/Scope**: Support for concurrent user queries, maintain 95% success rate for relevant query responses

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **Project Mission Compliance**: The chat endpoint supports the mission of building a specialized Ketamine Therapy AI by ensuring that responses are generated using ONLY the approved ketamine therapy knowledge base. The system implements guardrails to detect off-topic queries.

2. **Architecture Standards Compliance**: Uses the mandated technology stack - FastAPI backend with Neon Serverless PostgreSQL and pgvector for knowledge storage, Hugging Face API for AI generation.

3. **Knowledge Firewall Rule Compliance**: Implements the required retrieval mechanism - queries are matched against vectors_ketamine to ensure only ketamine-related context is used. The system follows the rule of using only approved uploads for responses.

4. **Data Security Compliance**: Will implement proper access controls for the chat endpoint and maintain audit logs for all chat interactions.

5. **Quality Assurance Compliance**: The system will follow the specified system prompt ensuring responses are based ONLY on provided context, with appropriate fallback when context is missing.

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
│   │   ├── chat_query.py
│   │   └── chat_response.py
│   ├── services/
│   │   ├── chat.py      # NEW: Handles chat queries, RAG logic, guardrails
│   │   ├── ai.py        # UPDATED: Extend with query embedding and response generation
│   │   ├── knowledge_service.py
│   │   ├── vector_service.py
│   │   └── audit_service.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── chat.py  # NEW: Chat endpoint implementation
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

**Structure Decision**: Selected Option 2: Web application structure with backend/ directory containing the FastAPI application. The chat service will be added to the existing services/ directory as specified in the user request, with a new chat endpoint in the API layer. This maintains consistency with the existing backend foundation and follows the established architecture patterns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations identified. All design decisions align with the Ketamine Therapy AI Constitution.
