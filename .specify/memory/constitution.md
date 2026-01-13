<!-- Sync Impact Report:
Version change: N/A (initial) → 1.0.0
Added sections: Project Mission, Architecture Standards, Knowledge Firewall Rule
Removed sections: None (completely replaced)
Templates requiring updates: ✅ Updated
Follow-up TODOs: None
-->
# Ketamine Therapy AI Constitution

## Core Principles

### Project Mission
Build a specialized Ketamine Therapy AI that learns ONLY from approved uploads. CRITICAL: Strict separation of "Ketamine Knowledge" (Vectors) and "General Data" (Chats/Logs).
<!-- Rationale: Ensures the AI system remains focused on ketamine therapy applications while maintaining data integrity and preventing contamination between knowledge domains -->

### Architecture Standards
Structure: Monorepo (frontend/ Next.js 16+, backend/ FastAPI). Database: Neon Serverless PostgreSQL with pgvector for the Knowledge Store and SQLModel for structured data. AI Engine: Mistral (via Hugging Face API) for Reasoning & Classification, and Hugging Face (sentence-transformers) for Vectors.
<!-- Rationale: Modern, scalable architecture that supports both the knowledge base and interactive chat capabilities while maintaining separation of concerns -->

### Knowledge Firewall Rule
Ingestion: Every uploaded file MUST be classified by AI. If "Ketamine Related" -> Chunk & Embed into vectors_ketamine. If "Not Related" -> Log metadata ONLY. DO NOT VECTORIZE. Retrieval: Chat interactions must only access the ketamine knowledge vectors when relevant to ketamine therapy topics.
<!-- Rationale: Maintains the integrity of the knowledge base by preventing irrelevant data from polluting the vector space and ensures compliance with the focused mission -->

### Data Security and Compliance
All patient-related data and therapy information must comply with healthcare regulations (HIPAA, etc.). Encryption at rest and in transit for all sensitive data. Access controls must be role-based with audit logging for all data access.
<!-- Rationale: Healthcare applications require strict compliance with privacy regulations and patient confidentiality -->

### Quality Assurance and Validation
All AI responses related to ketamine therapy must be validated against authoritative medical sources. Implement safety checks to prevent inappropriate medical advice. Maintain confidence scores for all responses with fallback procedures for low-confidence queries.
<!-- Rationale: Medical AI applications require high reliability and safety measures to protect patients -->

## Additional Constraints

### Technology Stack Requirements
- Frontend: Next.js 16+ with TypeScript
- Backend: FastAPI with Python 3.10+
- Database: Neon Serverless PostgreSQL with pgvector extension
- AI Services: Hugging Face API for LLM and embeddings
- Authentication: OAuth 2.0 or similar secure authentication mechanism
- Containerization: Docker for consistent deployments

### Performance Standards
- Response time: <2 seconds for typical queries
- Availability: 99.9% uptime for production systems
- Scalability: Support for concurrent users with auto-scaling capability
- Vector search performance: <500ms for similarity searches

## Development Workflow

### Code Quality Standards
- All code must be peer-reviewed before merging
- Unit tests covering >80% of codebase
- Integration tests for all API endpoints
- Static analysis and linting required before merge
- Documentation required for all public interfaces

### Data Pipeline Requirements
- File upload validation and sanitization
- Automated classification of incoming documents
- Audit trail for all data processing steps
- Backup and recovery procedures for vector databases

## Governance

The Ketamine Therapy AI Constitution serves as the governing document for all development activities. All team members must comply with these principles. Amendments require documentation of changes, approval from project leadership, and a migration plan for existing implementations. All pull requests and code reviews must verify compliance with these constitutional principles. Use the project documentation for detailed runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-13