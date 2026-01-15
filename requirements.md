# Project Requirements – AI Chat & Learning System  
## (Ketamine Therapy Focus)

---

## 1. Objective

Build a **Next.js web application** with two main interfaces:

1. **AI Chat Interface** – Interactive chat where the AI improves over time  
2. **Model Training Interface** – Upload files to teach the AI

### Critical Constraint

The system must **ONLY learn and retain knowledge related to ketamine therapy**.  
All other information must be stored separately and **must NOT influence model behavior**.

---

## 2. Interface #1 – Chat Interface

### Core Features

- Chat UI similar to ChatGPT  
- Streaming responses  
- Conversation history per user  
- System prompt enforced at all times  

### AI Behavior Rules

- AI must respond **ONLY within the ketamine therapy domain**
- If a user asks outside scope:
  - Politely refuse, **or**
  - Provide a neutral redirection back to ketamine-related topics

### Learning Logic (Very Important)

- The model **does NOT auto-learn from chat**
- Each chat message is classified as:
  - **Ketamine-therapy relevant**
  - **Non-relevant**
- Only relevant content is eligible for learning

### Implementation

- Use a classifier step before storage:
  - **Is this content related to ketamine therapy?** → `YES / NO`

---

## 3. Interface #2 – File Upload & Training Panel

### Supported File Types

- PDF  
- DOCX  
- TXT  
- Markdown  

### Upload Flow

1. User uploads a file  
2. System extracts text  
3. Content is validated for ketamine relevance  
4. If **relevant**:
   - Chunk text  
   - Generate embeddings  
   - Store in **Ketamine Vector Index**
5. If **not relevant**:
   - Store in **General Knowledge Storage**
   - Mark as **NON-TRAINING**

---

## 4. Knowledge Separation (CRITICAL ARCHITECTURE RULE)

### Two Knowledge Stores (Must Be Separate)

#### Ketamine Knowledge Store

- Used in:
  - Chat responses
  - Fine-tuning
  - RAG retrieval
- Contains **ONLY**:
  - Ketamine therapy content
  - Clinical protocols
  - Patient experience
  - Research & safety data

#### General Storage

- Stores:
  - User chats
  - Logs
  - Admin notes
  - Irrelevant uploads
- **Never queried during AI responses**

---

## 5. Model Learning Strategy (Recommended)

### Do NOT

- Continuous fine-tuning on raw chat logs  
- Auto-training without validation  

### Do This Instead

#### RAG-First Approach

- Base model remains unchanged  
- Ketamine knowledge injected via vector search  
- Optional periodic fine-tuning on curated data only  

#### Optional Fine-Tuning

- Admin-only action  
- Uses:
  - Approved ketamine documents  
  - Sanitized Q&A pairs  
- Versioned models with rollback support  

---

## 6. Safety & Compliance

- No medical diagnosis  
- Educational content only  
- Clear disclaimers  
- Full audit logs of:
  - Uploaded files
  - Training actions
  - Model changes

---

## 7. Admin Controls (Minimal)

- View uploaded files  
- Approve / reject learning data  
- Trigger fine-tuning  
- View vector index statistics  

---

## 8. Success Criteria

- AI never answers non-ketamine topics  
- Knowledge growth is controlled and auditable  
- Uploaded files affect answers without retraining (RAG)  
- Clean separation of training vs non-training data  

---

## 9. Deliverables

- Next.js application (Chat + Admin Panel)  
- Secure backend APIs  
- Vector database integration  
- Documentation covering:
  - Data flow
  - Learning pipeline
  - Fine-tuning process
