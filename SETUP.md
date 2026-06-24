# 🚀 QUICK START GUIDE

## Prerequisites Checklist
- [ ] Node.js 20.19+ installed
- [ ] Python 3.10+ installed
- [ ] PostgreSQL or MySQL database running
- [ ] Groq API key (get from https://console.groq.com/)

## Step-by-Step Setup (5 minutes)

### 1. Backend Setup

```bash
# Navigate to backend
cd C:\Users\rajpu\Downloads\AiVoa\AiVoa\backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate




# install 
pip install -r requirements.txt

# Create .env file
copy .env.example .env
```

**Edit `backend\.env` with your settings:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/hcp_crm
GROQ_API_KEY=gsk_your_actual_groq_key_here
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173
DEBUG=True
```

**Create the database:**
```bash
# For PostgreSQL
psql -U postgres
CREATE DATABASE hcp_crm;
\q

# For MySQL
mysql -u root -p
CREATE DATABASE hcp_crm;
exit;
```

### 2. Test Backend

```bash
# Test the AI agent
python test_agent.py

# Start the server
python start.py
```

✅ Backend should be running at http://localhost:8000
📚 API docs available at http://localhost:8000/docs

### 3. Frontend Setup

Open a **NEW** terminal:

```bash
cd C:\Users\rajpu\Downloads\AiVoa\AiVoa

# .env already created, verify it contains:
# VITE_API_URL=http://localhost:8000

# Start frontend
npm run dev
```

✅ Frontend should be running at http://localhost:5173

## 🎯 Usage

### Try the AI Chat!

1. Open http://localhost:5173
2. In the AI Assistant panel, type:

```
I met Dr. Sarah Johnson today at 2 PM. We discussed OncoBoost 
for melanoma treatment. She was very positive and interested. 
I shared the Phase III PDF and gave her sample packs.
```

3. Watch the AI:
   - Extract structured data
   - Auto-fill the form
   - Suggest follow-up actions

### Or Use the Form

Just fill out the form fields manually - both methods work!

## 🐛 Troubleshooting

**Backend won't start:**
- Check if PostgreSQL/MySQL is running
- Verify GROQ_API_KEY in .env
- Run `python test_agent.py` to test connection

**Frontend can't connect:**
- Make sure backend is running on port 8000
- Check browser console for errors
- Verify CORS settings

**AI not responding:**
- Check GROQ_API_KEY is valid
- Check internet connection
- See backend terminal for error logs

## 📖 Full Documentation

See `backend/README.md` for complete documentation.

## 🎓 Tech Stack Verification

✅ Frontend: React + Redux + Vite
✅ Backend: FastAPI + Python
✅ AI: LangGraph framework
✅ LLM: Groq (gemma2-9b-it)
✅ Database: PostgreSQL/MySQL
✅ Font: Google Inter

All requirements met! 🎉
