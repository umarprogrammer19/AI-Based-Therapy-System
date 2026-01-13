# Skill: RAG & Vector Operations

## 1. Database Schema (Neon + pgvector)
- **Table `KnowledgeDoc`**: `id`, `filename`, `upload_date`, `is_ketamine_relevant` (bool).
- **Table `VectorChunk`**: `id`, `doc_id`, `content` (text), `embedding` (vector[384]).
- **Setup**: Must run `CREATE EXTENSION vector;` in Postgres.

## 2. Ingestion Pipeline
- [cite_start]**Extract**: Use `pypdf` or `python-docx` to read text[cite: 32].
- [cite_start]**Classify**: Ask Mistral: "Is this text about Ketamine Therapy? Yes/No"[cite: 29].
- **Embed**: If Yes, use `sentence-transformers` to generate embeddings.
- **Store**: Insert into `VectorChunk`.

## 3. Retrieval Logic
- On Chat: Convert user query to vector -> Query `VectorChunk` (Cosine Similarity) -> Pass top 3 chunks to Mistral.