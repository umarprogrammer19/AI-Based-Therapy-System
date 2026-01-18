---
id: "PHR-0001"
title: "Amend Constitution Storage Rule"
stage: "constitution"
date: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "005-ketamine-ai-system"
user: "Umar Farooq"
command: "/sp.phr"
labels: ["constitution", "storage", "cloudflare-r2", "fine-tuning"]
links_spec: null
links_ticket: null
links_adr: null
links_pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml:
  - "none"
---

# Amend Constitution Storage Rule

## Original Prompt

```
Overwrite `.specify/memory/constitution.md` with these strict laws:

1. **Project Mission**:
   - Build a **Ketamine Therapy AI** with a Hybrid Architecture (RAG + Optional Fine-Tuning).
   - **Knowledge Firewall**: The AI must ONLY learn from approved Ketamine documents.
   - **Storage Rule**: All original uploaded files MUST be stored in **Cloudflare R2** (S3 Compatible).

2. **Tech Stack Standards**:
   - **Frontend**: Next.js 16+, Tailwind, Vercel AI SDK.
   - **Backend**: Python FastAPI, SQLModel.
   - **Database**: Neon Serverless (pgvector).
   - **File Storage**: Cloudflare R2 (via `boto3`).
   - **AI Engine**: Mistral (via Hugging Face).

3. **Fine-Tuning Protocol (Strict)**:
   - **Trigger**: ADMIN ONLY. Never automatic.
   - **Data Source**: Only files marked `is_ketamine_relevant=True` and approved by Admin.
   - [cite_start]**Constraint**: User chat logs must NEVER be used for training[cite: 72].
   - [cite_start]**Versioning**: Every fine-tuning job must be logged with a version ID for rollback[
```

## Response Summary

Updated the project constitution to incorporate new principles regarding Cloudflare R2 storage requirements, fine-tuning protocols, and tech stack standards. The constitution now mandates that all original uploaded files must be stored in Cloudflare R2, and defines strict guidelines for fine-tuning that can only be triggered by admins using approved ketamine-relevant documents.

## Outcome Impact

The constitution has been updated from version 1.1.0 to 1.2.0, incorporating new requirements for cloud storage using Cloudflare R2 and establishing clear fine-tuning protocols. This ensures the project follows the required architecture for document storage and AI training procedures.

## Tests Summary

none

## Files Summary

- .specify/memory/constitution.md

## Next Prompts

Consider updating related templates to align with the new constitution principles, particularly plan-template.md, spec-template.md, and tasks-template.md.

## Reflection Note

The constitution update successfully enforces the required storage and fine-tuning protocols while maintaining the existing project mission and tech stack standards.

## Failure Modes Observed

None

## Next Experiment to Improve Prompt Quality

N/A