# AI-CHATBOX Backend

Complete backend implementation following the 8-day blueprint.

## 📋 Features Implemented

### ✅ Day 1: Backend Foundation & Environment Setup
- FastAPI application structure
- Environment configuration
- Basic `/chat` endpoint
- Session ID and timestamp tracking

### ✅ Day 2: Database Integration & User Context
- SQLite/PostgreSQL database integration
- User, Chat, and Document models
- Automatic user creation and management
- Conversation ID assignment
- Chat persistence

### ✅ Day 3: Chat History & Retrieval
- `/history` endpoint
- User-specific chat retrieval
- Chronological ordering
- Limit and filtering support

### ✅ Day 4: Authentication Layer
- JWT token-based authentication
- `/signup` and `/login` endpoints
- Password hashing with bcrypt
- Token expiration management

### ✅ Day 5: AI Logic & Model Configuration
- OpenAI integration
- Configurable parameters (temperature, max_tokens)
- Token usage tracking
- Processing time measurement

### ✅ Day 6: Document Ingestion / RAG Pipeline
- `/upload` endpoint for document ingestion
- Text chunking (800 tokens)
- Document metadata storage
- RAG context retrieval (mock implementation)

### ✅ Day 7: Moderation + Analytics
- Content safety filtering
- Unsafe content blocking
- Usage metrics tracking
- Analytics logging

### ✅ Day 8: Deployment + Monitoring
- CORS configuration
- `/health` endpoint
- System metrics reporting
- Production-ready setup

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
SECRET_KEY=your_secret_key_here
```

### 3. Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run Tests
```bash
python test_complete.py
```

## 📁 Project Structure

```
Ai-backend/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── chat.py          # Main chat endpoint (Days 1-7)
│   │   ├── history.py       # Chat history (Day 3)
│   │   ├── auth.py          # Authentication (Day 4)
│   │   ├── documents.py     # Document upload (Day 6)
│   │   └── health.py        # Health check (Day 8)
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Auth utilities
│   │   ├── ai.py            # AI generation logic
│   │   ├── rag.py           # RAG pipeline
│   │   └── moderation.py    # Content moderation
│   ├── db/
│   │   ├── base.py          # SQLAlchemy base
│   │   └── session.py       # Database session
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── chat.py          # Chat model
│   │   └── document.py      # Document model
│   ├── schemas/
│   │   ├── chat.py          # Chat schemas
│   │   ├── auth.py          # Auth schemas
│   │   └── history.py       # History schemas
│   └── main.py              # Application entry
├── test_complete.py         # Full test suite
├── requirements.txt         # Dependencies
└── .env.example            # Environment template
```

## 🔌 API Endpoints

### Chat
- `POST /api/v1/chat` - Send messages and get AI responses

### Authentication
- `POST /api/v1/signup` - Create new user
- `POST /api/v1/login` - User login

### History
- `POST /api/v1/history` - Retrieve chat history

### Documents
- `POST /api/v1/upload` - Upload documents for RAG

### Health
- `GET /api/v1/health` - System health check

## 📊 JSON Schemas

All endpoints follow the exact JSON schemas defined in the 8-day blueprint. See `test_complete.py` for examples.

## 🔒 Security

- Password hashing with bcrypt
- JWT token authentication
- Content moderation
- CORS protection

## 📈 Monitoring

The `/health` endpoint provides:
- System status
- Uptime percentage
- Request count
- Average latency
- Error rate

## 🌐 Deployment

Ready for deployment on:
- Render
- Railway
- Heroku
- Any platform supporting Python/FastAPI

Configure CORS origins in `app/main.py` for your frontend URL.
