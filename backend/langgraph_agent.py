from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import settings
import json
import re


class AgentState(TypedDict):
    """State for the LangGraph agent"""
    messages: Sequence[BaseMessage]
    extracted_data: dict
    needs_clarification: bool
    suggested_followups: list


class HCPInteractionAgent:
    """LangGraph agent for processing HCP interaction conversations"""
    
    def __init__(self):
        # Initialize Groq LLM with llama-3.3-70b-versatile model (gemma2-9b-it was decommissioned)
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            groq_api_key=settings.GROQ_API_KEY
        )
        
        # Alternative smaller model for simple tasks
        self.llm_small = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.7,
            groq_api_key=settings.GROQ_API_KEY
        )
        
        # Build the agent graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("extract_information", self._extract_information)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("suggest_followups", self._suggest_followups)
        
        # Define edges
        workflow.set_entry_point("extract_information")
        workflow.add_edge("extract_information", "generate_response")
        workflow.add_edge("generate_response", "suggest_followups")
        workflow.add_edge("suggest_followups", END)
        
        return workflow.compile()
    
    def _extract_information(self, state: AgentState) -> AgentState:
        """Extract structured information from conversation"""
        
        extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant helping a pharmaceutical field representative log their interaction with a Healthcare Professional (HCP).

Extract the following information from the conversation:
- HCP name
- Interaction type (Meeting, Phone Call, Email, Video Call, Conference, Other)
- Date and time of interaction
- Attendees
- Topics discussed
- Materials shared (promotional materials, brochures, etc.)
- Samples distributed
- HCP sentiment (positive, neutral, negative)
- Outcomes
- Follow-up actions needed

Return the extracted information as a JSON object. Only include fields that were mentioned in the conversation.
If information is missing or unclear, mark it as null.

Example output format:
{{
    "hcp_name": "Dr. Sarah Johnson",
    "interaction_type": "Meeting",
    "date": "2026-01-27",
    "time": "14:30",
    "attendees": "Dr. Johnson, Medical team",
    "topics_discussed": "Discussed OncoBoost efficacy in treating advanced melanoma",
    "materials_shared": ["OncoBoost Phase III PDF", "Product brochure"],
    "samples_distributed": ["OncoBoost 50mg sample pack"],
    "sentiment": "positive",
    "outcomes": "Dr. Johnson showed interest in prescribing OncoBoost",
    "follow_up_actions": "Schedule follow-up in 2 weeks"
}}"""),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        chain = extraction_prompt | self.llm
        
        try:
            response = chain.invoke({"messages": state["messages"]})
            
            # Extract JSON from response
            content = response.content
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                extracted_data = json.loads(json_match.group())
            else:
                extracted_data = {}
            
            state["extracted_data"] = extracted_data
            state["needs_clarification"] = len(extracted_data) < 3  # Need at least 3 fields
            
        except Exception as e:
            print(f"Error extracting information: {e}")
            state["extracted_data"] = {}
            state["needs_clarification"] = True
        
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """Generate a conversational response"""
        
        response_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant for a pharmaceutical field representative.
You help them log their interactions with Healthcare Professionals (HCPs).

Be conversational, friendly, and professional. 
- If you successfully extracted information, acknowledge it and ask if there's anything else to add.
- If information is missing, politely ask for the missing details.
- Keep responses concise (2-3 sentences max).
- Use natural language, avoid technical jargon.

Current extracted data: {extracted_data}
Needs clarification: {needs_clarification}"""),
            MessagesPlaceholder(variable_name="messages")
        ])
        
        chain = response_prompt | self.llm
        
        try:
            response = chain.invoke({
                "messages": state["messages"],
                "extracted_data": json.dumps(state["extracted_data"], indent=2),
                "needs_clarification": state["needs_clarification"]
            })
            
            # Add AI response to messages
            state["messages"] = list(state["messages"]) + [response]
            
        except Exception as e:
            print(f"Error generating response: {e}")
            fallback_msg = AIMessage(content="I've noted that down. Would you like to add anything else?")
            state["messages"] = list(state["messages"]) + [fallback_msg]
        
        return state
    
    def _suggest_followups(self, state: AgentState) -> AgentState:
        """Generate intelligent follow-up suggestions"""
        
        followup_prompt = ChatPromptTemplate.from_messages([
            ("system", """Based on the HCP interaction details, suggest 3-5 relevant follow-up actions.

Consider:
- HCP sentiment and engagement level
- Topics discussed
- Samples/materials shared
- Standard pharmaceutical sales best practices

Format: Return a JSON array of strings, each being a specific, actionable follow-up.

Example:
["Schedule follow-up meeting in 2 weeks", "Send OncoBoost Phase III clinical data", "Add Dr. Smith to advisory board invitation list"]

Extracted data: {extracted_data}"""),
            ("human", "Generate follow-up suggestions")
        ])
        
        chain = followup_prompt | self.llm
        
        try:
            response = chain.invoke({
                "extracted_data": json.dumps(state["extracted_data"], indent=2)
            })
            
            # Extract JSON array from response
            content = response.content
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            
            if json_match:
                suggested_followups = json.loads(json_match.group())
            else:
                # Fallback suggestions
                suggested_followups = [
                    "Schedule follow-up meeting",
                    "Send relevant product information",
                    "Update CRM notes"
                ]
            
            state["suggested_followups"] = suggested_followups[:5]  # Limit to 5
            
        except Exception as e:
            print(f"Error generating followups: {e}")
            state["suggested_followups"] = [
                "Schedule follow-up meeting",
                "Send relevant product information",
                "Update CRM notes"
            ]
        
        return state
    
    async def process_message(self, user_message: str, conversation_history: list) -> dict:
        """Process a user message and return the response with extracted data"""
        
        # Build message history
        messages = []
        for msg in conversation_history:
            if msg["type"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            elif msg["type"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
        
        # Add current user message
        messages.append(HumanMessage(content=user_message))
        
        # Create initial state
        initial_state = {
            "messages": messages,
            "extracted_data": {},
            "needs_clarification": False,
            "suggested_followups": []
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Extract the last AI message
        ai_messages = [msg for msg in final_state["messages"] if isinstance(msg, AIMessage)]
        response_content = ai_messages[-1].content if ai_messages else "I'm here to help you log the interaction."
        
        return {
            "message": response_content,
            "extracted_data": final_state["extracted_data"],
            "suggested_followups": final_state["suggested_followups"]
        }


# Create a singleton instance
agent = HCPInteractionAgent()
