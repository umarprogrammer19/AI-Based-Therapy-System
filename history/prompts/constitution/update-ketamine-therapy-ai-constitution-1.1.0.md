---
id: constitution_001
title: Update Ketamine Therapy AI Constitution to v1.1.0
date: 2026-01-15
stage: constitution
version: 1.1.0
---

# Update Ketamine Therapy AI Constitution to v1.1.0

## Prompt Text
Overwrite `.specify/memory/constitution.md` with these strict laws:

1. **Project Mission**:
   - Build a **Ketamine Therapy AI** that strictly adheres to the "Knowledge Separation" architecture.
   - **CRITICAL**: The system must ONLY learn/retain knowledge related to ketamine therapy[cite: 7].
   - **Constraint**: Non-relevant data (general chats, random uploads) must be stored separately and NEVER vector-indexed[cite: 8, 70].

2. **Tech Stack Standards**:
   - **Frontend**: Next.js 16+ (App Router), Tailwind CSS, Vercel AI SDK.
   - **Backend**: Python FastAPI, Uvicorn.
   - **Database**: Neon Serverless PostgreSQL.
     - Use `pgvector` for the **Ketamine Knowledge Store** in vectors [cite: 47].
     - Use standard tables for **General Storage** (Chats/Logs)[cite: 64].
   - **AI Engine**:
     - **Model**: Mistral (via Hugging Face API).
     - **Strategy**: RAG-First (Retrieval Augmented Generation)[cite: 77].

3. **Core Logic Rules**:
   - **Ingestion**: Every upload MUST undergo an AI Classification Step ("Is this Ketamine related?")[cite: 23, 29].
   - **Response**: The System Prompt must be "You are a medical information assistant specializing ONLY in ketamine therapy"[cite: 88].
   - **Safety**: No medical diagnoses; strictly educational[cite: 95].

4. **Documentation**:
   - Maintain a `specs/` folder with current architecture diagrams and API definitions[cite: 112].

## Response Text
Updated the constitution file with the new requirements, changing version from 1.0.0 to 1.1.0. Modified principles to align with the user's specifications, adding Core Logic Rules and Documentation sections as required. The update follows the "Knowledge Separation" architecture and implements the tech stack standards with proper citations. Removed previous sections that were not part of the new requirements.