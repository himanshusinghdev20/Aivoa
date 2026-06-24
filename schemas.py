from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    institution: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class HCPCreate(HCPBase):
    pass


class HCPResponse(HCPBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    hcp_name: str
    interaction_type: Literal["Meeting", "Phone Call", "Email", "Video Call", "Conference", "Other"]
    interaction_date: datetime
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: List[str] = []
    samples_distributed: List[str] = []
    sentiment: Literal["positive", "neutral", "negative"] = "neutral"
    outcomes: Optional[str] = None
    follow_up_actions: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(BaseModel):
    id: int
    hcp_id: int
    hcp_name: str
    interaction_type: str
    interaction_date: datetime
    attendees: Optional[str]
    topics_discussed: Optional[str]
    materials_shared: List[str]
    samples_distributed: List[str]
    sentiment: str
    outcomes: Optional[str]
    follow_up_actions: Optional[str]
    ai_suggested_followups: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatMessageBase(BaseModel):
    content: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageResponse(BaseModel):
    id: int
    message_type: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    conversation_history: List[dict] = []


class ChatResponse(BaseModel):
    message: str
    extracted_data: Optional[dict] = None
    suggested_followups: List[str] = []
