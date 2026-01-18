<!-- Sync Impact Report:
Version change: 1.1.0 → 1.2.0
Modified principles: Project Mission, Tech Stack Standards, Core Logic Rules → Project Mission, Tech Stack Standards, Fine-Tuning Protocol
Added sections: Fine-Tuning Protocol
Removed sections: Core Logic Rules, Documentation
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Ketamine Therapy AI Constitution

## Core Principles

### Project Mission
- Build a **Ketamine Therapy AI** with a Hybrid Architecture (RAG + Optional Fine-Tuning).
- **Knowledge Firewall**: The AI must ONLY learn from approved Ketamine documents.
- **Storage Rule**: All original uploaded files MUST be stored in **Cloudflare R2** (S3 Compatible).
<!-- Rationale: Ensures the AI system remains focused on ketamine therapy applications while maintaining data integrity and preventing contamination between knowledge domains -->

### Tech Stack Standards
- **Frontend**: Next.js 16+, Tailwind, Vercel AI SDK.
- **Backend**: Python FastAPI, SQLModel.
- **Database**: Neon Serverless (pgvector).
- **File Storage**: Cloudflare R2 (via `boto3`).
- **AI Engine**: Mistral (via Hugging Face).
<!-- Rationale: Modern, scalable architecture that supports both the knowledge base and interactive chat capabilities while maintaining separation of concerns -->

### Fine-Tuning Protocol (Strict)
- **Trigger**: ADMIN ONLY. Never automatic.
- **Data Source**: Only files marked `is_ketamine_relevant=True` and approved by Admin.
- [cite_start]**Constraint**: User chat logs must NEVER be used for training[cite: 72].
- [cite_start]**Versioning**: Every fine-tuning job must be logged with a version ID for rollback[</command-args>.
<!-- Rationale: Maintains the integrity of the knowledge base by ensuring only relevant information is processed and the AI responds appropriately within its scope -->

## Governance

The Ketamine Therapy AI Constitution serves as the governing document for all development activities. All team members must comply with these principles. Amendments require documentation of changes, approval from project leadership, and a migration plan for existing implementations. All pull requests and code reviews must verify compliance with these constitutional principles. Use the project documentation for detailed runtime development guidance.

**Version**: 1.2.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-18