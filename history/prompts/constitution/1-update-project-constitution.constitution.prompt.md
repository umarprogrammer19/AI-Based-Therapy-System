---
id: 1
title: "Update Project Constitution"
stage: "constitution"
date_iso: "2026-01-13"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "Umar Farooq"
command: "sp.constitution Overwrite `.specify/memory/constitution.md` with these strict laws:..."
labels: ["constitution", "governance", "project-setup"]
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt

```
Overwrite `.specify/memory/constitution.md` with these strict laws:

1. **Project Mission**:
   - Build a specialized **Ketamine Therapy AI** that learns ONLY from approved uploads.
   - [cite_start]**CRITICAL**: Strict separation of "Ketamine Knowledge" (Vectors) and "General Data" (Chats/Logs)[cite: 7, 51].

2. **Architecture Standards**:
   - **Structure**: Monorepo (`frontend/` Next.js 16+, `backend/` FastAPI).
   - **Database**: **Neon Serverless PostgreSQL**.
     - Use `pgvector` for the Knowledge Store.
     - Use `SQLModel` for structured data.
   - **AI Engine**:
     - **LLM**: Mistral (via Hugging Face API) for Reasoning & Classification.
     - **Embeddings**: Hugging Face (`sentence-transformers`) for Vectors.

3. **The "Knowledge Firewall" Rule**:
   - **Ingestion**: Every uploaded file MUST be classified by AI.
     - If "Ketamine Related" -> Chunk & Embed into `vectors_ketamine`.
     - If "Not Related" -> Log metadata ONLY. [cite_start]DO NOT VECTORIZE[cite: 23, 49].
   - **Retrieval**: Chat
```

# Response

Updated the `.specify/memory/constitution.md` file with the new constitution for the Ketamine Therapy AI project, incorporating all specified principles including the Project Mission, Architecture Standards, and Knowledge Firewall Rule. The new constitution establishes the foundational governance for the project with specific requirements for data handling, security compliance, and development workflows.

# Outcome

Successfully created a comprehensive constitution that defines the core principles, constraints, and governance structure for the Ketamine Therapy AI project. The new constitution emphasizes the critical separation between ketamine knowledge vectors and general data, implements security and compliance requirements for healthcare applications, and establishes clear architectural standards.