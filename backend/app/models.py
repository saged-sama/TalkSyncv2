from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    image = Column(String, nullable=True)
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    sender = Column(String)
    time = Column(DateTime, default=datetime.utcnow )
    message = Column(Text)
    is_file = Column(Boolean, default=False)
    mime_type = Column(String, nullable=True)
    filename = Column(String, nullable=True)
