# AI-First CRM - HCP Interaction Module

An AI-powered Customer Relationship Management system for Healthcare Professionals (HCP) interactions, designed for pharmaceutical field representatives.

## 🎯 Features

- **Dual Input Methods**: Log interactions via structured form OR conversational AI chat
- **LangGraph AI Agent**: Intelligent conversation processing with automatic data extraction
- **Groq LLM Integration**: Uses `gemma2-9b-it` for fast, accurate responses
- **Auto-Fill Forms**: AI extracts structured data from natural language conversations
- **Smart Follow-ups**: AI-generated follow-up action suggestions
- **Real-time Updates**: Redux state management for seamless UX

## 🏗️ Tech Stack

### Frontend
- **React 19.2** - UI framework
- **Redux Toolkit** - State management
- **Vite** - Build tool
- **Google Inter Font** - Typography

### Backend
- **FastAPI** - Modern Python web framework
- **LangGraph** - AI agent orchestration framework
- **Groq** - LLM provider (gemma2-9b-it, llama-3.3-70b-versatile)
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL/MySQL** - Database options

## 📋 Prerequisites

- **Node.js** 20.19+ or 22.12+
- **Python** 3.10+
- **PostgreSQL** or **MySQL** database
- **Groq API Key** - Get one at https://console.groq.com/

## 🚀 Installation & Setup

### 1. Clone & Navigate

```bash
cd C:\Users\rajpu\Downloads\AiVoa\AiVoa
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env and set:
VITE_API_URL=http://localhost:8000
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 4. Configure Backend Environment

Edit `backend/.env`:

```env
# Database (choose one)
DATABASE_URL=postgresql://username:password@localhost:5432/hcp_crm
# OR for MySQL:
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hcp_crm

# Groq API Key (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173

DEBUG=True
```

### 5. Database Setup

#### PostgreSQL:

```bash
# Create database
psql -U postgres
CREATE DATABASE hcp_crm;
\q
```

#### MySQL:

```bash
# Create database
mysql -u root -p
CREATE DATABASE hcp_crm;
exit;
```

### 6. Initialize Database

The database tables will be automatically created when you start the backend server for the first time.

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Start Frontend Dev Server

Open a new terminal:

```bash
cd C:\Users\rajpu\Downloads\AiVoa\AiVoa
npm run dev
```

Frontend will be available at: http://localhost:5173

## 📖 Usage Guide

### Method 1: Conversational AI Chat

1. Click on the AI Assistant chat interface
2. Type naturally: *"I met Dr. Sarah Johnson today at 2 PM. We discussed OncoBoost efficacy for melanoma treatment. She was very positive and interested. I shared the Phase III results PDF and gave her sample packs."*
3. The AI will:
   - Extract structured data (HCP name, date, topics, materials, sentiment)
   - Auto-fill the form fields
   - Suggest intelligent follow-up actions

### Method 2: Structured Form

1. Manually fill out the form fields:
   - HCP Name
   - Interaction Type
   - Date & Time
   - Topics Discussed
   - Materials Shared
   - Samples Distributed
   - Sentiment
   - Outcomes
   - Follow-up Actions

## 🤖 AI Agent Architecture

The LangGraph agent follows a three-node workflow:

```
User Message → Extract Information → Generate Response → Suggest Follow-ups → Return
```

### Node Functions:

1. **Extract Information**: Parses conversation for structured data (HCP name, date, sentiment, etc.)
2. **Generate Response**: Creates natural, conversational AI responses
3. **Suggest Follow-ups**: Generates context-aware action items

### LLM Models Used:

- **Primary**: `gemma2-9b-it` (fast, efficient for most tasks)
- **Complex Tasks**: `llama-3.3-70b-versatile` (available for advanced reasoning)

## 🗄️ Database Schema

### Tables:

- **hcps**: Healthcare Professional records
- **interactions**: Interaction logs with HCPs
- **chat_messages**: Conversation history

### Key Fields:

- HCP: name, specialty, institution, email, phone
- Interaction: type, date, topics, materials, samples, sentiment, outcomes
- Chat: message type, content, metadata

## 🔌 API Endpoints

### Chat
- `POST /api/chat` - Send message to AI agent

### HCPs
- `GET /api/hcps` - List all HCPs
- `GET /api/hcps/search?query={name}` - Search HCPs
- `POST /api/hcps` - Create new HCP
- `GET /api/hcps/{id}` - Get HCP by ID

### Interactions
- `GET /api/interactions` - List all interactions
- `POST /api/interactions` - Create new interaction
- `GET /api/interactions/{id}` - Get interaction by ID

### Health
- `GET /api/health` - Health check

## 🛠️ Development

### Project Structure

```
AiVoa/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── langgraph_agent.py      # LangGraph AI agent
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database connection
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
├── src/
│   ├── components/
│   │   └── LogInteraction/
│   │       ├── AIAssistant/    # AI chat component
│   │       └── InteractionDetailsForm/  # Form component
│   ├── store/
│   │   └── slices/
│   │       └── interactionSlice.js  # Redux state
│   └── services/
│       └── api.js              # API client
├── package.json
└── vite.config.js
```

## 🐛 Troubleshooting

### Backend won't start:
- Check if database is running
- Verify DATABASE_URL in .env
- Ensure GROQ_API_KEY is valid

### Frontend can't connect to backend:
- Verify backend is running on port 8000
- Check VITE_API_URL in frontend .env
- Check CORS settings in backend config.py

### AI responses are slow:
- Groq is generally fast; check your internet connection
- Consider using gemma2-9b-it instead of larger models

### Database errors:
- Run migrations: Tables auto-create on first run
- Check database credentials
- Ensure database exists

## 📝 Environment Variables Summary

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (backend/.env)
```
DATABASE_URL=postgresql://user:pass@localhost:5432/hcp_crm
GROQ_API_KEY=your_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173
DEBUG=True
```

## 🔐 Security Notes

- Never commit `.env` files to version control
- Keep your GROQ_API_KEY secret
- Use environment variables for all sensitive data
- In production, set DEBUG=False

## 📦 Building for Production

### Frontend:
```bash
npm run build
```

### Backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🎓 Key Implementation Details

### LangGraph Integration
The AI agent uses LangGraph's StateGraph to maintain conversation context and extract structured data across multiple turns of conversation.

### Groq LLM Usage
- **gemma2-9b-it**: Primary model for conversation and extraction
- **llama-3.3-70b-versatile**: Available for complex reasoning tasks

### Redux State Management
All form fields and chat messages are managed in Redux, allowing the AI to seamlessly update the UI with extracted data.

## 📄 License

This project is part of an AI-First CRM assignment.

## 🤝 Support

For issues or questions, check:
- FastAPI docs: http://localhost:8000/docs
- LangGraph docs: https://langchain-ai.github.io/langgraph/
- Groq docs: https://console.groq.com/docs/models
