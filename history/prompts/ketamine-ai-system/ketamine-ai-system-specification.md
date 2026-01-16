---
id: spec_001
title: Ketamine AI System Specification
date: 2026-01-15
stage: spec
feature: ketamine-ai-system
---

# Ketamine AI System Specification

## Prompt Text
I want to define the Master Spec for the "Ketamine AI & Learning System".

**1. System Architecture**
- **Monorepo**: `frontend/` (Next.js) and `backend/` (FastAPI).
- **Dual Storage Strategy**[cite: 52]:
  - **Store A (Ketamine Knowledge)**: Stores vector embeddings of approved PDFs/Docs. Used for RAG.
  - **Store B (General Storage)**: Stores raw Chat History, User Logs, and "Non-Training" files.

**2. Backend Features (FastAPI)**
- **Auth**: API Key protection for Admin routes.
- **Ingestion Pipeline** [cite: 36-50]:
  - `POST /api/upload`: Accepts PDF/DOCX/TXT.
  - **Step 1 (Classify)**: Ask Mistral "Is this regarding Ketamine Therapy?".
  - **Step 2 (Route)**:
    - *If Yes*: Extract Text -> Chunk -> Embed -> Store in `vectors_ketamine`.
    - *If No*: Save Metadata to `admin_logs` -> Mark "NON-TRAINING" -> Do NOT Embed.
- **Chat API**[cite: 10]:
  - `POST /api/chat`:
  - **Step 1**: Check if query is off-topic[cite: 17].
  - **Step 2**: Retrieve top 3 relevant chunks from `vectors_ketamine`.
  - **Step 3**: Generate response using Mistral with System Prompt[cite: 88].

**3. Frontend Features (Next.js)**
- **User Interface**[cite: 11]:
  - Chat Window (Streaming responses).
  - "Medical Disclaimer" footer visible at all times[cite: 95].
- **Admin Panel**[cite: 100]:
  - File Upload Zone.
  - "Knowledge Base" View: List all files with status (Training / Non-Training).
  - "Audit Log": View who uploaded what[cite: 96].

**4. Data Models (SQLModel)**
- `KnowledgeDoc`: id, filename, is_ketamine_relevant (bool), uploaded_at.
- `VectorChunk`: id, doc_id, embedding (vector), content.
- `ChatSession`: id, user_identifier.
- `ChatMessage`: id, session_id, role, content.

## Response Text
Created comprehensive specification for the Ketamine AI & Learning System with three priority-ranked user stories: 1) Ketamine Therapy Information Query (P1), 2) Document Upload and Classification (P2), and 3) Admin Knowledge Management (P3). Defined 15 functional requirements covering document upload, AI classification, chat interface, and admin functionality. Identified four key entities (KnowledgeDoc, VectorChunk, ChatSession, ChatMessage) and established seven measurable success criteria. All requirements are testable and measurable without implementation details.