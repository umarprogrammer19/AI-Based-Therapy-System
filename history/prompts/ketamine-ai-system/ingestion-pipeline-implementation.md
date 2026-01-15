---
id: impl_002
title: Ingestion Pipeline Implementation
date: 2026-01-15
stage: implement
feature: ketamine-ai-system
---

# Ingestion Pipeline Implementation

## Prompt Text
@.claude/agents/rag-engineer.md **Step 2: Ingestion Pipeline**
1. Implement `POST /api/admin/upload`.
2. **Classification Service**: Use `huggingface_hub` to send the first page of text to Mistral. Prompt: "Is this text about Ketamine Therapy? Answer YES/NO"[cite: 29].
3. **Storage Logic**:
   - If YES: Parse full text, chunk it (500 chars), generate embeddings (using `sentence-transformers`), and save to `VectorChunk` [cite: 43-47].
   - If NO: Save to `KnowledgeDoc` with `is_ketamine_relevant=False` and DO NOT create vectors [cite: 48-50].

## Response Text
Successfully implemented the complete ingestion pipeline for the Ketamine AI & Learning System. Created the classification service using HuggingFace inference API to determine if documents are ketamine-related. Implemented text extraction utilities for PDF, DOCX, TXT, and MD formats. Created embedding generation service using sentence-transformers to create vector embeddings. Built the ingestion service that orchestrates the entire pipeline: upload, classification, conditional processing (chunking and embedding if relevant, metadata-only if not), and storage. Updated the upload endpoint with proper authentication and processing logic. All required tasks for the ingestion pipeline have been completed.