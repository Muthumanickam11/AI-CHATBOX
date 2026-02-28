from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, index=True) # e.g. "conv-101", uuid
    user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(Text, nullable=False)
    reply = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="chats")
