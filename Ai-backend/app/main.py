from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import chat, history, auth, documents, health, analytics, hybrid_chat
from app.db.session import engine
from app.db.base import Base

app = FastAPI(title="AI-CHATBOX Backend")

# Day 8: CORS Configuration
origins = [
    "http://localhost:3000",
    "https://ai-chatbox.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(history.router, prefix="/api/v1/history", tags=["history"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(hybrid_chat.router, prefix="/api/v1/hybrid", tags=["hybrid"])

@app.get("/")
async def root():
    return {"message": "AI-CHATBOX Backend is running"}
