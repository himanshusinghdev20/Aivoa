"""
Quick start script to initialize and run the HCP CRM backend
"""
import sys
import os

def main():
    print("=" * 60)
    print("HCP CRM Backend - Quick Start")
    print("=" * 60)
    print()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ ERROR: .env file not found!")
        print()
        print("Please create a .env file with the following:")
        print("-" * 60)
        print("DATABASE_URL=postgresql://user:password@localhost:5432/hcp_crm")
        print("GROQ_API_KEY=your_groq_api_key_here")
        print("API_HOST=0.0.0.0")
        print("API_PORT=8000")
        print("CORS_ORIGINS=http://localhost:5173")
        print("DEBUG=True")
        print("-" * 60)
        print()
        print("Copy .env.example to .env and fill in your values.")
        sys.exit(1)
    
    print("✅ .env file found")
    print()
    
    # Try to import required packages
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import langgraph
        import langchain_groq
        print("✅ All required packages installed")
        print()
    except ImportError as e:
        print(f"❌ ERROR: Missing required package: {e}")
        print()
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Import and check settings
    try:
        from config import settings
        print("✅ Configuration loaded")
        print()
        print(f"   Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'Not configured'}")
        print(f"   API Port: {settings.API_PORT}")
        print(f"   Debug: {settings.DEBUG}")
        print()
        
        if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
            print("⚠️  WARNING: GROQ_API_KEY not configured!")
            print("   Get your API key from: https://console.groq.com/")
            print()
    except Exception as e:
        print(f"❌ ERROR loading configuration: {e}")
        sys.exit(1)
    
    # Initialize database
    try:
        from database import init_db
        init_db()
        print("✅ Database initialized")
        print()
    except Exception as e:
        print(f"❌ ERROR initializing database: {e}")
        print()
        print("Make sure your database is running and DATABASE_URL is correct.")
        sys.exit(1)
    
    print("=" * 60)
    print("🚀 Starting FastAPI server...")
    print("=" * 60)
    print()
    print(f"   API: http://localhost:{settings.API_PORT}")
    print(f"   Docs: http://localhost:{settings.API_PORT}/docs")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Run the server
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    main()
