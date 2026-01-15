<!-- Sync Impact Report:
Version change: 1.0.0 → 1.1.0
Modified principles: Project Mission, Architecture Standards → Project Mission, Tech Stack Standards
Added sections: Core Logic Rules, Documentation requirements
Removed sections: Data Security and Compliance, Quality Assurance and Validation, Technology Stack Requirements, Performance Standards, Code Quality Standards, Data Pipeline Requirements
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Ketamine Therapy AI Constitution

## Core Principles

### Project Mission
Build a Ketamine Therapy AI that strictly adheres to the "Knowledge Separation" architecture. CRITICAL: The system must ONLY learn/retain knowledge related to ketamine therapy[cite: 7]. Constraint: Non-relevant data (general chats, random uploads) must be stored separately and NEVER vector-indexed[cite: 8, 70].
<!-- Rationale: Ensures the AI system remains focused on ketamine therapy applications while maintaining data integrity and preventing contamination between knowledge domains -->

### Tech Stack Standards
Frontend: Next.js 16+ (App Router), Tailwind CSS, Vercel AI SDK. Backend: Python FastAPI, Uvicorn. Database: Neon Serverless PostgreSQL. Use pgvector for the Ketamine Knowledge Store in vectors [cite: 47]. Use standard tables for General Storage (Chats/Logs)[cite: 64]. AI Engine: Model: Mistral (via Hugging Face API). Strategy: RAG-First (Retrieval Augmented Generation)[cite: 77].
<!-- Rationale: Modern, scalable architecture that supports both the knowledge base and interactive chat capabilities while maintaining separation of concerns -->

### Core Logic Rules
Ingestion: Every upload MUST undergo an AI Classification Step ("Is this Ketamine related?")[cite: 23, 29]. Response: The System Prompt must be "You are a medical information assistant specializing ONLY in ketamine therapy"[cite: 88]. Safety: No medical diagnoses; strictly educational[cite: 95].
<!-- Rationale: Maintains the integrity of the knowledge base by ensuring only relevant information is processed and the AI responds appropriately within its scope -->

### Documentation
Maintain a specs/ folder with current architecture diagrams and API definitions[cite: 112].
<!-- Rationale: Proper documentation ensures maintainability and enables team collaboration -->

## Governance

The Ketamine Therapy AI Constitution serves as the governing document for all development activities. All team members must comply with these principles. Amendments require documentation of changes, approval from project leadership, and a migration plan for existing implementations. All pull requests and code reviews must verify compliance with these constitutional principles. Use the project documentation for detailed runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2026-01-13 | **Last Amended**: 2026-01-15