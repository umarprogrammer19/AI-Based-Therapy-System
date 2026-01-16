# Ketamine Therapy AI & Learning System

A Next.js web application with AI-powered chat interface and document-based learning system focused exclusively on ketamine therapy knowledge.

## 🚀 Overview

This project implements a specialized AI system that focuses solely on ketamine therapy education and information. The system features:

- **AI Chat Interface**: Interactive chat where users can ask questions about ketamine therapy
- **Document Learning System**: Upload PDF, DOCX, TXT, or Markdown files to teach the AI
- **Knowledge Separation**: Strict separation between ketamine therapy knowledge and general data
- **RAG (Retrieval Augmented Generation)**: Answers based on uploaded documents, not general knowledge

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Next.js 16+, Tailwind CSS, Vercel AI SDK
- **Backend**: Python FastAPI, Uvicorn
- **Database**: Neon Serverless PostgreSQL with pgvector extension
- **AI Model**: Mistral via Hugging Face API
- **Embeddings**: Sentence Transformers

### Knowledge Separation Architecture
The system maintains two separate knowledge stores:

1. **Ketamine Knowledge Store**:
   - Contains only ketamine therapy-related content
   - Used for chat responses via RAG
   - Powered by vector search in pgvector

2. **General Storage**:
   - Stores chat history, logs, and non-training uploads
   - Never queried during AI responses

## 🛠️ Setup

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL with pgvector extension (or Neon account)

### Environment Variables

#### Backend (.env in backend/)
```bash
DATABASE_URL="postgresql+asyncpg://username:password@localhost:5432/ketamine_ai"
HF_API_TOKEN="your_huggingface_api_token_here"
ADMIN_API_KEY="your_admin_api_key_here"
```

#### Frontend (.env.local in frontend/)
```bash
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
NEXT_PUBLIC_ADMIN_API_KEY="your_admin_api_key_here"
```

### Installation

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python -c "from src.database.init_db import init_db; init_db()"  # Initialize database
uvicorn src.main:app --reload --port 8000
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

## 📋 Features

### User Interface (Chat Interface)
- **Chat UI**: Similar to ChatGPT with streaming responses
- **Conversation History**: Per-user session management
- **Medical Disclaimer**: Always visible for safety
- **Ketamine-Focused**: AI responds only within ketamine therapy domain

### Admin Interface (Training Panel)
- **File Upload**: Support for PDF, DOCX, TXT, Markdown
- **Automatic Classification**: AI determines ketamine relevance
- **Knowledge Management**: View training vs non-training documents
- **Audit Trail**: Complete logging of all activities

### Learning Logic
- **Classifier Step**: "Is this content related to ketamine therapy?" → YES/NO
- **Relevant Content**: Chunked, embedded, and stored in Ketamine Vector Index
- **Non-Relevant Content**: Stored separately, marked as NON-TRAINING
- **RAG-First Approach**: Base model unchanged, knowledge injected via vector search

## 🚦 Usage

### For Users
1. Visit the chat interface at `http://localhost:3000`
2. Ask questions about ketamine therapy
3. Receive responses based on the knowledge base

### For Admins
1. Access the admin panel at `http://localhost:3000/admin`
2. Upload documents via the upload interface
3. Monitor which documents are used for training
4. Manage the knowledge base

## 🛡️ Safety & Compliance

- **No Medical Diagnosis**: Educational content only
- **Clear Disclaimers**: Prominent medical disclaimers
- **Auditable Learning**: Complete logs of all training data
- **Controlled Knowledge**: AI never answers non-ketamine topics

## 📊 Success Criteria

- ✅ AI never answers non-ketamine therapy topics
- ✅ Knowledge growth is controlled and auditable
- ✅ Uploaded files affect answers via RAG without retraining
- ✅ Clean separation of training vs non-training data
- ✅ Real-time learning from new documents

## 🚀 Deployment

### Backend (to deploy)
```bash
# Build and run
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Frontend (to deploy)
```bash
# Build and serve
npm run build
npm run start
```

## 🤖 API Endpoints

### Chat API
- `POST /api/v1/chat/chat/` - Submit chat queries with RAG

### Admin APIs
- `POST /api/v1/knowledge-docs/upload/` - Upload and classify documents
- `GET /api/v1/knowledge-docs/` - List all knowledge documents
- `GET /api/v1/vector-chunks/` - List vector chunks (with admin auth)

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

Built with ❤️ for ketamine therapy education and research.