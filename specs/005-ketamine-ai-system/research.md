# Research: Ketamine AI & Learning System

## Decision: Language Versions and Dependencies
**Rationale**: Selected Python 3.10+ for backend to ensure compatibility with FastAPI, pgvector, and SQLModel. Next.js 16+ for frontend to leverage latest features and ecosystem compatibility.

**Alternatives considered**:
- Python 3.11: Could work but lacks newer typing features and performance improvements
- Vue.js/React alternatives: Next.js was specified in the constitution and requirements

## Decision: Database and Vector Storage
**Rationale**: Neon Serverless PostgreSQL with pgvector extension provides the dual storage strategy required: vector storage for ketamine knowledge and standard tables for general storage (chat logs, admin logs). This matches the constitution requirements exactly.

**Alternatives considered**:
- MongoDB with Atlas Vector Search: Would require different architecture approach
- Pinecone/Elasticsearch: Would require additional service dependencies
- SQLite with chromadb: Insufficient for production requirements

## Decision: AI Model Selection
**Rationale**: Mistral via Hugging Face API provides the required RAG-first approach and supports the system prompt requirement. The model is well-suited for the educational, non-diagnostic use case.

**Alternatives considered**:
- OpenAI GPT models: Would create vendor lock-in and additional costs
- Self-hosted models: Would increase operational complexity
- Other open-source models: Mistral offers good balance of performance and licensing

## Decision: Document Processing Pipeline
**Rationale**: The classification step followed by conditional routing (embed vs log-only) ensures strict adherence to the knowledge separation principle from the constitution. PDF, DOCX, TXT, and MD formats cover the most common document types for medical literature.

**Alternatives considered**:
- Processing all documents the same way: Would violate the knowledge separation principle
- Different file format support: Limited to common formats to maintain security and simplicity

## Decision: Frontend Architecture
**Rationale**: Next.js App Router with Tailwind CSS and Vercel AI SDK provides optimal developer experience for the chat interface and streaming responses. The architecture supports the required medical disclaimer visibility and admin panel functionality.

**Alternatives considered**:
- Traditional React with Create React App: Less modern, would lack SSR benefits
- Different CSS frameworks: Tailwind provides utility-first approach that matches requirements