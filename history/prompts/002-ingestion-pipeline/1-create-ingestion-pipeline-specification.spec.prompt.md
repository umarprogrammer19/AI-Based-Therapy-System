---
id: 1
title: Create ingestion pipeline specification
stage: spec
feature: ingestion-pipeline
date: 2026-01-14
surface: agent
model: claude-sonnet-4-5-20250929
branch: 002-ingestion-pipeline
user: Umar Farooq
labels: [specification, ingestion, pipeline, ai-classification]
links:
  spec: D:/Ai-brain/specs/002-ingestion-pipeline/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - D:/Ai-brain/specs/002-ingestion-pipeline/spec.md
  - D:/Ai-brain/specs/002-ingestion-pipeline/checklists/requirements.md
tests: []
---

# Create ingestion pipeline specification

## Command
```
@.claude/agents/rag-engineer.md I want to build the Ingestion Pipeline.

**Requirements**:
1. **Endpoint**: `POST /api/admin/upload`.
2. **Logic Flow**:
   - [cite_start]Receive file (PDF/TXT)[cite: 31].
   - **Step A (Classification)**: Send first 500 chars to Mistral. Ask: "Is this about Ketamine Therapy?".
   - **Step B (Branching)**:
     - [cite_start]If NO: Save to `KnowledgeDoc(relevant=False)` and STOP[cite: 49].
     - If YES: Save to `KnowledgeDoc(relevant=True)`.
   - **Step C (Processing)**:
     - Extract full text.
     - Split into 500-char chunks.
     - Embed using Hugging Face (MiniLM).
     - Save to `VectorChunk`. (branch name starts with 002)
```

## Response
Created feature specification for ingestion pipeline with file upload, AI classification, text extraction, chunking, and vector embedding capabilities. Created branch 002-ingestion-pipeline with proper spec file and requirements checklist.