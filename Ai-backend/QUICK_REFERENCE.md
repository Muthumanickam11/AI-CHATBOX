# 🚀 AI-CHATBOX Backend - Quick Reference

## 📞 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

---

## 🔥 Main Endpoints

### 1️⃣ Chat (Days 1, 2, 5, 6, 7)
```http
POST /api/v1/chat
Content-Type: application/json

{
  "session_id": "sess-001",
  "prompt": "Your question here",
  "user": { "email": "user@example.com", "name": "User" },
  "settings": { "temperature": 0.7, "max_tokens": 200 }
}
```

**Response:**
```json
{
  "reply": "AI response here",
  "model": "gpt-4",
  "timestamp": "2025-12-09T...",
  "conversation_id": "conv-abc123",
  "stored": true,
  "tokens_used": 168,
  "processing_time": "1.4s"
}
```

---

### 2️⃣ Signup (Day 4)
```http
POST /api/v1/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass"
}
```

**Response:**
```json
{
  "user_id": 1,
  "token": "jwt_eyJhbGc...",
  "expires_in": 3600,
  "login_status": "success"
}
```

---

### 3️⃣ Login (Day 4)
```http
POST /api/v1/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass"
}
```

**Response:**
```json
{
  "user_id": 1,
  "token": "jwt_eyJhbGc...",
  "expires_in": 3600,
  "login_status": "success"
}
```

---

### 4️⃣ History (Day 3)
```http
POST /api/v1/history
Content-Type: application/json

{
  "user_id": "1",
  "action": "get_history",
  "limit": 10
}
```

**Response:**
```json
{
  "history": [
    { "prompt": "Hello", "reply": "Hi!" },
    { "prompt": "What is AI?", "reply": "..." }
  ],
  "count": 2
}
```

---

### 5️⃣ Upload Document (Day 6)
```http
POST /api/v1/upload
Content-Type: multipart/form-data

file: <file>
user_id: "user-001"
```

**Response:**
```json
{
  "doc_id": "doc-abc123",
  "file_name": "document.pdf",
  "user_id": "user-001",
  "embedding_status": "completed",
  "chunks_indexed": 98
}
```

---

### 6️⃣ Health Check (Day 8)
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "uptime": "99.97%",
  "requests_today": 1280,
  "average_latency": "1.9s",
  "error_rate": "0.4%"
}
```

---

## 🔒 Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
SECRET_KEY=your-secret-key-here

# Optional
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

---

## 🧪 Testing Commands

```bash
# Run all tests
python test_all_days.py

# Run individual day tests
python test_day1.py
python test_day2.py

# Start server
uvicorn app.main:app --reload --port 8000

# Start server (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 Features by Day

| Day | Feature | Status |
|-----|---------|--------|
| 1 | Backend Foundation | ✅ |
| 2 | Database Integration | ✅ |
| 3 | Chat History | ✅ |
| 4 | Authentication | ✅ |
| 5 | AI Logic | ✅ |
| 6 | RAG Pipeline | ✅ |
| 7 | Moderation | ✅ |
| 8 | Deployment | ✅ |

---

## 🎯 Common Use Cases

### Send a simple message
```python
import requests

response = requests.post('http://localhost:8000/api/v1/chat', json={
    "prompt": "Hello!"
})
print(response.json())
```

### Send message with user context
```python
response = requests.post('http://localhost:8000/api/v1/chat', json={
    "user": {"email": "user@example.com", "name": "User"},
    "prompt": "What is AI?"
})
```

### Get chat history
```python
response = requests.post('http://localhost:8000/api/v1/history', json={
    "user_id": "1",
    "limit": 5
})
```

### Upload document
```python
files = {'file': open('document.pdf', 'rb')}
data = {'user_id': 'user-001'}
response = requests.post('http://localhost:8000/api/v1/upload', 
                        files=files, data=data)
```

---

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is available
- Verify all dependencies installed: `pip install -r requirements.txt`

### Database errors
- Delete `sql_app.db` and restart server
- Check DATABASE_URL in .env

### OpenAI errors
- Verify OPENAI_API_KEY is set
- Check API key is valid
- Ensure account has credits

### CORS errors
- Update `origins` list in `app/main.py`
- Add your frontend URL

---

## 📚 Documentation Files

- `README.md` - Main documentation
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation details
- `DEPLOYMENT.md` - Deployment guide
- `QUICK_REFERENCE.md` - This file
- `deployment_config.json` - Configuration template

---

## 🎉 You're Ready!

The backend is fully functional and ready for:
- ✅ Local development
- ✅ Testing
- ✅ Production deployment
- ✅ Frontend integration

**Happy coding! 🚀**
