"""
Script to test the Groq API connection and LangGraph agent
"""
import asyncio
from config import settings
from langgraph_agent import agent


async def test_agent():
    print("=" * 60)
    print("Testing HCP Interaction AI Agent")
    print("=" * 60)
    print()
    
    # Test message
    test_message = """
    I met Dr. Sarah Johnson today at 2 PM at Memorial Hospital. 
    We discussed OncoBoost efficacy for melanoma patients. 
    She was very interested and positive about the Phase III results. 
    I shared the clinical trial PDF and gave her some sample packs.
    She wants to follow up in 2 weeks.
    """
    
    print("Test Message:")
    print("-" * 60)
    print(test_message)
    print("-" * 60)
    print()
    print("Processing with LangGraph agent...")
    print()
    
    try:
        result = await agent.process_message(test_message, [])
        
        print("=" * 60)
        print("AI Response:")
        print("=" * 60)
        print(result["message"])
        print()
        
        print("=" * 60)
        print("Extracted Data:")
        print("=" * 60)
        import json
        print(json.dumps(result["extracted_data"], indent=2))
        print()
        
        print("=" * 60)
        print("Suggested Follow-ups:")
        print("=" * 60)
        for i, followup in enumerate(result["suggested_followups"], 1):
            print(f"{i}. {followup}")
        print()
        
        print("✅ Agent test successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Make sure:")
        print("1. GROQ_API_KEY is set in .env")
        print("2. You have internet connection")
        print("3. All dependencies are installed")


if __name__ == "__main__":
    asyncio.run(test_agent())
