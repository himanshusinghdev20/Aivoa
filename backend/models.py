from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class InteractionType(str, enum.Enum):
    MEETING = "Meeting"
    PHONE_CALL = "Phone Call"
    EMAIL = "Email"
    VIDEO_CALL = "Video Call"
    CONFERENCE = "Conference"
    OTHER = "Other"


class Sentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class HCP(Base):
    __tablename__ = "hcps"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    specialty = Column(String(255))
    institution = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="hcp")


class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    interaction_type = Column(Enum(InteractionType), nullable=False)
    interaction_date = Column(DateTime, nullable=False)
    attendees = Column(Text)
    topics_discussed = Column(Text)
    materials_shared = Column(JSON)  # Store as JSON array
    samples_distributed = Column(JSON)  # Store as JSON array
    sentiment = Column(Enum(Sentiment), default=Sentiment.NEUTRAL)
    outcomes = Column(Text)
    follow_up_actions = Column(Text)
    ai_suggested_followups = Column(JSON)  # Store as JSON array
    created_by = Column(String(255))  # User/Rep who created the interaction
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hcp = relationship("HCP", back_populates="interactions")
    chat_messages = relationship("ChatMessage", back_populates="interaction", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=True)
    message_type = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON)  # Store additional context (renamed from metadata)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interaction = relationship("Interaction", back_populates="chat_messages")
