# System Architecture Documentation

## Overview

AI-First CRM for Healthcare Professional Interactions using LangGraph and Groq LLMs.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────────────┐              ┌──────────────────┐     │
│  │ Interaction Form │              │  AI Assistant    │     │
│  │   Component      │◄────────────►│     Chat         │     │
│  └──────────────────┘              └──────────────────┘     │
│           │                                   │               │
│           └───────────────┬───────────────────┘               │
│                           │                                   │
│                    ┌──────▼───────┐                          │
│                    │ Redux Store  │                          │
│                    └──────────────┘                          │
│                           │                                   │
└───────────────────────────┼───────────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   API Client   │
                    └───────┬────────┘
                            │ HTTP/REST
┌───────────────────────────┼───────────────────────────────────┐
│                    ┌──────▼────────┐                          │
│                    │ FastAPI Router│                          │
│                    └───┬───────┬───┘                          │
│                        │       │                               │
│         ┌──────────────┘       └──────────────┐               │
│         │                                      │               │
│  ┌──────▼──────┐                      ┌───────▼────────┐     │
│  │   Database  │                      │   LangGraph    │     │
│  │  Operations │                      │     Agent      │     │
│  │ (SQLAlchemy)│                      │                │     │
│  └──────┬──────┘                      └───────┬────────┘     │
│         │                                      │               │
│  ┌──────▼──────┐                      ┌───────▼────────┐     │
│  │ PostgreSQL/ │                      │  Groq API      │     │
│  │   MySQL     │                      │ (gemma2-9b-it) │     │
│  └─────────────┘                      └────────────────┘     │
│                     Backend (Python)                          │
└───────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Layer

#### 1. InteractionDetailsForm Component
- **Location**: `src/components/LogInteraction/InteractionDetailsForm/`
- **Purpose**: Structured form for logging HCP interactions
- **Features**:
  - HCP name, type, date/time input
  - Materials and samples tracking
  - Sentiment selector
  - Auto-populated from AI extraction

#### 2. AIAssistant Component
- **Location**: `src/components/LogInteraction/AIAssistant/`
- **Purpose**: Conversational interface for logging
- **Features**:
  - Real-time chat with AI agent
  - Automatic form population
  - Loading states and error handling

#### 3. Redux Store
- **Location**: `src/store/slices/interactionSlice.js`
- **Purpose**: Centralized state management
- **State**:
  - Form field values
  - Chat message history
  - Materials and samples arrays
  - AI suggested follow-ups

#### 4. API Client
- **Location**: `src/services/api.js`
- **Purpose**: HTTP communication with backend
- **Endpoints**:
  - `/api/chat` - AI conversation
  - `/api/interactions` - CRUD operations
  - `/api/hcps` - HCP management

### Backend Layer

#### 1. FastAPI Application
- **Location**: `backend/main.py`
- **Purpose**: REST API server
- **Routes**:
  - Health check
  - HCP CRUD endpoints
  - Interaction CRUD endpoints
  - Chat endpoint (AI integration)

#### 2. LangGraph Agent
- **Location**: `backend/langgraph_agent.py`
- **Purpose**: AI conversation orchestration
- **Workflow**:
  ```
  User Message
      ↓
  Extract Information (LLM call)
      ↓
  Generate Response (LLM call)
      ↓
  Suggest Follow-ups (LLM call)
      ↓
  Return Results
  ```
- **State Management**:
  - Messages history
  - Extracted data dictionary
  - Clarification flags
  - Follow-up suggestions

#### 3. Database Layer
- **Location**: `backend/models.py`, `backend/database.py`
- **ORM**: SQLAlchemy
- **Models**:
  - `HCP`: Healthcare Professional records
  - `Interaction`: Interaction logs
  - `ChatMessage`: Conversation history

#### 4. Groq LLM Integration
- **Model**: `gemma2-9b-it` (primary)
- **Alternative**: `llama-3.3-70b-versatile` (complex tasks)
- **Provider**: LangChain Groq
- **Use Cases**:
  - Natural language understanding
  - Data extraction (NER, entity recognition)
  - Conversational responses
  - Follow-up generation

## Data Flow

### Scenario: User sends chat message

```
1. User types: "Met Dr. Smith, discussed Product X"
   ↓
2. Frontend: AIAssistant.jsx
   - Adds to chat UI
   - Calls api.sendMessage()
   ↓
3. API Client: services/api.js
   - POST /api/chat
   - Sends message + conversation history
   ↓
4. Backend: main.py
   - Receives request
   - Calls agent.process_message()
   ↓
5. LangGraph Agent: langgraph_agent.py
   
   Node 1: Extract Information
   - Calls Groq LLM (gemma2-9b-it)
   - Prompt: "Extract HCP name, date, topics, sentiment..."
   - Returns: { hcp_name: "Dr. Smith", topics: "Product X", ... }
   
   Node 2: Generate Response
   - Calls Groq LLM
   - Prompt: "Acknowledge extracted data, ask for clarification..."
   - Returns: "Got it! I noted Dr. Smith and Product X discussion..."
   
   Node 3: Suggest Follow-ups
   - Calls Groq LLM
   - Prompt: "Based on interaction, suggest follow-ups..."
   - Returns: ["Schedule follow-up", "Send materials", ...]
   ↓
6. Backend Response
   - Returns JSON:
     {
       "message": "AI response text",
       "extracted_data": {...},
       "suggested_followups": [...]
     }
   ↓
7. Frontend: AIAssistant.jsx
   - Displays AI message in chat
   - Dispatches Redux actions to update form fields
   - Populates HCP name, topics, sentiment, etc.
   ↓
8. User sees:
   - AI response in chat
   - Form auto-filled with extracted data
   - Suggested follow-ups listed
```

## LangGraph Agent Deep Dive

### State Definition

```python
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]      # Conversation history
    extracted_data: dict                  # Structured data
    needs_clarification: bool             # Flag for missing info
    suggested_followups: list             # AI-generated actions
```

### Graph Structure

```
START
  │
  ▼
┌─────────────────────┐
│ extract_information │  ← LLM Call 1: Extract structured data
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ generate_response   │  ← LLM Call 2: Create conversational reply
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ suggest_followups   │  ← LLM Call 3: Generate action items
└──────────┬──────────┘
           │
           ▼
          END
```

### Prompt Engineering

#### Extraction Prompt
```
You are an AI assistant helping a pharmaceutical field representative.
Extract: HCP name, interaction type, date, topics, materials, sentiment...
Return as JSON: { "hcp_name": "...", "sentiment": "positive", ... }
```

#### Response Prompt
```
You are helpful and conversational.
- If data extracted successfully → acknowledge and ask for more
- If data missing → politely ask for details
Keep responses concise (2-3 sentences).
```

#### Follow-up Prompt
```
Based on interaction details, suggest 3-5 actionable follow-ups.
Consider: sentiment, topics discussed, materials shared.
Return as JSON array: ["action 1", "action 2", ...]
```

## Database Schema

```sql
-- HCPs Table
CREATE TABLE hcps (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255),
    institution VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Interactions Table
CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    hcp_id INTEGER REFERENCES hcps(id),
    interaction_type VARCHAR(50) NOT NULL,
    interaction_date TIMESTAMP NOT NULL,
    attendees TEXT,
    topics_discussed TEXT,
    materials_shared JSON,
    samples_distributed JSON,
    sentiment VARCHAR(20) DEFAULT 'neutral',
    outcomes TEXT,
    follow_up_actions TEXT,
    ai_suggested_followups JSON,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chat Messages Table
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    interaction_id INTEGER REFERENCES interactions(id),
    message_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Technology Justification

### Why LangGraph?
- **State Management**: Maintains conversation context across multiple turns
- **Workflow Control**: Explicit control over LLM call sequence
- **Debugging**: Clear visibility into agent decision-making
- **Scalability**: Easy to add new nodes for additional processing

### Why Groq?
- **Speed**: Fastest inference times (important for real-time chat)
- **Cost-Effective**: Competitive pricing
- **Model Selection**: gemma2-9b-it balances speed and quality
- **Reliability**: High uptime and availability

### Why FastAPI?
- **Async Support**: Native async/await for LLM calls
- **Auto Documentation**: OpenAPI/Swagger docs out of the box
- **Type Safety**: Pydantic models for validation
- **Performance**: One of the fastest Python frameworks

### Why Redux?
- **Predictable State**: Single source of truth for form data
- **DevTools**: Time-travel debugging capabilities
- **Middleware**: Easy to add logging, persistence, etc.
- **Scalability**: Works well as app grows

## Performance Considerations

### Frontend
- **Debouncing**: Chat input debounced to avoid excessive API calls
- **Optimistic Updates**: UI updates immediately, syncs with backend
- **Loading States**: Clear feedback during LLM processing

### Backend
- **Connection Pooling**: SQLAlchemy pool for database connections
- **Async Processing**: FastAPI async endpoints for non-blocking I/O
- **Caching**: Consider Redis for frequent HCP lookups

### LLM Calls
- **Model Selection**: gemma2-9b-it for speed, llama-3.3-70b for accuracy
- **Prompt Optimization**: Concise prompts to reduce token usage
- **Batch Processing**: Future optimization for multiple extractions

## Security Considerations

1. **API Key Management**: Groq key in environment variables, never in code
2. **CORS**: Strict origin checking in production
3. **SQL Injection**: SQLAlchemy ORM prevents injection attacks
4. **Input Validation**: Pydantic schemas validate all API inputs
5. **Rate Limiting**: Consider adding rate limiting for production

## Future Enhancements

1. **Authentication**: Add user login and role-based access
2. **Real-time Updates**: WebSocket for live chat updates
3. **Voice Input**: Integrate voice-to-text for field use
4. **Offline Mode**: PWA with local storage for offline logging
5. **Analytics**: Dashboard for interaction trends and insights
6. **Multi-language**: Support for international markets
7. **Mobile App**: React Native version for mobile devices

## Monitoring & Observability

### Metrics to Track
- LLM response times
- Data extraction accuracy
- User session lengths
- API endpoint latencies
- Database query performance

### Logging
- Structured logging with Python logging module
- LLM call logs for debugging prompts
- User interaction logs (privacy-compliant)
- Error tracking with stack traces

## Deployment Architecture

```
Production Environment:

┌────────────────┐
│   Load         │
│   Balancer     │
└────┬───────────┘
     │
     ├──────────┬──────────┐
     │          │          │
┌────▼────┐ ┌──▼────┐ ┌──▼────┐
│Frontend │ │Frontend│ │Frontend│
│ (Nginx) │ │ (Nginx)│ │ (Nginx)│
└─────────┘ └────────┘ └────────┘
     │          │          │
     └──────────┼──────────┘
                │
         ┌──────▼────────┐
         │   API Gateway │
         └──────┬────────┘
                │
     ┌──────────┼──────────┐
     │          │          │
┌────▼────┐ ┌──▼────┐ ┌──▼────┐
│Backend  │ │Backend│ │Backend│
│ (uvicorn│ │(uvicorn│ │(uvicorn│
└─────────┘ └────────┘ └────────┘
     │          │          │
     └──────────┼──────────┘
                │
         ┌──────┴──────┐
         │             │
    ┌────▼────┐   ┌───▼────┐
    │PostgreSQL│   │  Groq  │
    │(Primary) │   │  API   │
    └──────────┘   └────────┘
```

## Conclusion

This architecture provides:
- ✅ **Dual Input**: Form OR chat
- ✅ **AI-Powered**: LangGraph + Groq
- ✅ **Scalable**: Microservices-ready
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Production-Ready**: Error handling, validation, security

The system is designed to scale from MVP to enterprise-grade CRM.
