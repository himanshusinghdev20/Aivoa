from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uvicorn

from config import settings
from database import get_db, init_db
from models import HCP, Interaction, ChatMessage, InteractionType, Sentiment
from schemas import (
    HCPCreate, HCPResponse,
    InteractionCreate, InteractionResponse,
    ChatRequest, ChatResponse
)
from langgraph_agent import agent

# Initialize FastAPI app
app = FastAPI(
    title="HCP CRM API",
    description="AI-First CRM for Healthcare Professional Interactions",
    version="1.0.0"
)

# Configure CORS - explicitly allow frontend origins
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://aivoa-he4h.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        print(f"Startup DB Error: {e}")

    print("Application Started")


# ==================== HCP Endpoints ====================

@app.get("/api/hcps", response_model=List[HCPResponse])
def get_hcps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of HCPs"""
    hcps = db.query(HCP).offset(skip).limit(limit).all()
    return hcps


@app.get("/api/hcps/search")
def search_hcps(query: str, db: Session = Depends(get_db)):
    """Search HCPs by name"""
    hcps = db.query(HCP).filter(HCP.name.ilike(f"%{query}%")).limit(10).all()
    return [{"id": hcp.id, "name": hcp.name, "specialty": hcp.specialty} for hcp in hcps]


@app.post("/api/hcps", response_model=HCPResponse)
def create_hcp(hcp: HCPCreate, db: Session = Depends(get_db)):
    """Create a new HCP"""
    # Check if HCP already exists
    existing_hcp = db.query(HCP).filter(HCP.name == hcp.name).first()
    if existing_hcp:
        return existing_hcp
    
    db_hcp = HCP(**hcp.dict())
    db.add(db_hcp)
    db.commit()
    db.refresh(db_hcp)
    return db_hcp


@app.get("/api/hcps/{hcp_id}", response_model=HCPResponse)
def get_hcp(hcp_id: int, db: Session = Depends(get_db)):
    """Get a specific HCP by ID"""
    hcp = db.query(HCP).filter(HCP.id == hcp_id).first()
    if not hcp:
        raise HTTPException(status_code=404, detail="HCP not found")
    return hcp


# ==================== Interaction Endpoints ====================

@app.get("/api/interactions", response_model=List[InteractionResponse])
def get_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of interactions"""
    interactions = db.query(Interaction).offset(skip).limit(limit).all()
    
    result = []
    for interaction in interactions:
        hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
        result.append({
            "id": interaction.id,
            "hcp_id": interaction.hcp_id,
            "hcp_name": hcp.name if hcp else "Unknown",
            "interaction_type": interaction.interaction_type.value,
            "interaction_date": interaction.interaction_date,
            "attendees": interaction.attendees,
            "topics_discussed": interaction.topics_discussed,
            "materials_shared": interaction.materials_shared or [],
            "samples_distributed": interaction.samples_distributed or [],
            "sentiment": interaction.sentiment.value,
            "outcomes": interaction.outcomes,
            "follow_up_actions": interaction.follow_up_actions,
            "ai_suggested_followups": interaction.ai_suggested_followups or [],
            "created_at": interaction.created_at
        })
    
    return result


@app.post("/api/interactions", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction"""
    
    # Find or create HCP
    hcp = db.query(HCP).filter(HCP.name == interaction.hcp_name).first()
    if not hcp:
        hcp = HCP(name=interaction.hcp_name)
        db.add(hcp)
        db.commit()
        db.refresh(hcp)
    
    # Create interaction
    db_interaction = Interaction(
        hcp_id=hcp.id,
        interaction_type=InteractionType(interaction.interaction_type),
        interaction_date=interaction.interaction_date,
        attendees=interaction.attendees,
        topics_discussed=interaction.topics_discussed,
        materials_shared=interaction.materials_shared,
        samples_distributed=interaction.samples_distributed,
        sentiment=Sentiment(interaction.sentiment),
        outcomes=interaction.outcomes,
        follow_up_actions=interaction.follow_up_actions,
        ai_suggested_followups=[]  # Will be populated by AI
    )
    
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    
    return {
        "id": db_interaction.id,
        "hcp_id": hcp.id,
        "hcp_name": hcp.name,
        "interaction_type": db_interaction.interaction_type.value,
        "interaction_date": db_interaction.interaction_date,
        "attendees": db_interaction.attendees,
        "topics_discussed": db_interaction.topics_discussed,
        "materials_shared": db_interaction.materials_shared or [],
        "samples_distributed": db_interaction.samples_distributed or [],
        "sentiment": db_interaction.sentiment.value,
        "outcomes": db_interaction.outcomes,
        "follow_up_actions": db_interaction.follow_up_actions,
        "ai_suggested_followups": db_interaction.ai_suggested_followups or [],
        "created_at": db_interaction.created_at
    }


@app.get("/api/interactions/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction by ID"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    hcp = db.query(HCP).filter(HCP.id == interaction.hcp_id).first()
    
    return {
        "id": interaction.id,
        "hcp_id": interaction.hcp_id,
        "hcp_name": hcp.name if hcp else "Unknown",
        "interaction_type": interaction.interaction_type.value,
        "interaction_date": interaction.interaction_date,
        "attendees": interaction.attendees,
        "topics_discussed": interaction.topics_discussed,
        "materials_shared": interaction.materials_shared or [],
        "samples_distributed": interaction.samples_distributed or [],
        "sentiment": interaction.sentiment.value,
        "outcomes": interaction.outcomes,
        "follow_up_actions": interaction.follow_up_actions,
        "ai_suggested_followups": interaction.ai_suggested_followups or [],
        "created_at": interaction.created_at
    }


# ==================== AI Chat Endpoints ====================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat message with AI agent"""
    try:
        # Process message through LangGraph agent
        result = await agent.process_message(
            user_message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            message=result["message"],
            extracted_data=result["extracted_data"],
            suggested_followups=result["suggested_followups"]
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HCP CRM API",
        "version": "1.0.0"
    }


# ==================== Main ====================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )



