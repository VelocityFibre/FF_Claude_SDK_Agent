#!/usr/bin/env python3
"""
FastAPI Backend for Orchestrated Agent Workforce

Uses the orchestrator to automatically route queries to:
- Contractor Agent
- Project Agent
- Convex Database Agent
- Universal Convex Agent (for all 30+ tables)

Deploy to: Railway, Render, or any Python hosting platform

Usage:
    uvicorn orchestrated_agent_api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import orchestrator and agents
from orchestrator.orchestrator import AgentOrchestrator
from universal_convex_agent import UniversalConvexAgent, load_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_env()

# Initialize FastAPI
app = FastAPI(
    title="FibreFlow Orchestrated Agent API",
    description="Smart routing to contractor, project, and database agents with 14k+ FibreFlow records",
    version="3.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator and universal agent
orchestrator = None
universal_agent = None

def get_orchestrator() -> AgentOrchestrator:
    """Get or create orchestrator instance."""
    global orchestrator
    if orchestrator is None:
        logger.info("Initializing Agent Orchestrator...")
        orchestrator = AgentOrchestrator()
        logger.info("Orchestrator initialized with 5 agents")
    return orchestrator

def get_universal_agent() -> UniversalConvexAgent:
    """Get or create universal agent instance."""
    global universal_agent
    if universal_agent is None:
        logger.info("Initializing Universal Convex Agent...")
        universal_agent = UniversalConvexAgent()
        logger.info(f"Universal Agent initialized with {len(universal_agent.available_tables)} tables")
    return universal_agent


# Request/Response models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    mode: Optional[str] = Field(default="orchestrated", description="'orchestrated' or 'universal'")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me all contractors",
                "mode": "orchestrated"
            }
        }


class ChatResponse(BaseModel):
    response: str
    success: bool = True
    timestamp: str
    agent_used: Optional[str] = None
    mode: str
    routing_info: Optional[Dict] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    agents_available: int
    tables_accessible: int
    records_accessible: int


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_model=Dict)
async def root():
    """API information."""
    return {
        "name": "FibreFlow Orchestrated Agent API",
        "version": "3.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "agents": "/agents"
        },
        "features": [
            "Smart routing to 5 specialized agents",
            "Universal access to 30+ Convex tables",
            "14,000+ FibreFlow records",
            "Natural language queries"
        ]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        orch = get_orchestrator()
        universal = get_universal_agent()

        return HealthResponse(
            status="healthy",
            version="3.0.0",
            agents_available=orch.total_agents,
            tables_accessible=len(universal.available_tables),
            records_accessible=14173  # Known count
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all available agents."""
    orch = get_orchestrator()

    agents_info = []
    for agent in orch.agents:
        agents_info.append({
            "id": agent["id"],
            "name": agent["name"],
            "type": agent["type"],
            "triggers": agent.get("triggers", []),
            "status": agent["status"]
        })

    return {
        "total_agents": len(agents_info),
        "agents": agents_info
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with agents - automatically routes to the right specialist.

    Modes:
    - orchestrated: Routes based on query keywords
    - universal: Uses universal agent for any table
    """
    try:
        logger.info(f"Received query: {request.message[:100]}...")

        if request.mode == "universal":
            # Use universal agent for direct table access
            universal = get_universal_agent()
            response_text = universal.chat(request.message)
            universal.reset_conversation()

            return ChatResponse(
                response=response_text,
                success=True,
                timestamp=datetime.now().isoformat(),
                agent_used="universal-convex-agent",
                mode="universal",
                routing_info={
                    "tables_available": len(universal.available_tables),
                    "direct_access": True
                }
            )

        else:
            # Use orchestrator for smart routing
            orch = get_orchestrator()
            result = orch.route_task(request.message, auto_select=True)

            if result["status"] == "routed":
                agent_info = result["agent"]

                return ChatResponse(
                    response=result["response"],
                    success=True,
                    timestamp=datetime.now().isoformat(),
                    agent_used=agent_info["agent_id"],
                    mode="orchestrated",
                    routing_info={
                        "agent_name": agent_info["agent_name"],
                        "confidence": result.get("confidence", "high"),
                        "matched_keywords": result.get("matched_keywords", [])
                    }
                )
            else:
                # Fallback to universal agent
                universal = get_universal_agent()
                response_text = universal.chat(request.message)
                universal.reset_conversation()

                return ChatResponse(
                    response=response_text,
                    success=True,
                    timestamp=datetime.now().isoformat(),
                    agent_used="universal-convex-agent (fallback)",
                    mode="universal",
                    routing_info={
                        "fallback": True,
                        "reason": "No specific agent matched"
                    }
                )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/contractor")
async def chat_contractor(request: ChatRequest):
    """Direct access to Contractor Agent."""
    from agents.contractor_agent.agent import ContractorAgent

    agent = ContractorAgent()
    response = agent.chat(request.message)
    agent.reset_conversation()

    return ChatResponse(
        response=response,
        success=True,
        timestamp=datetime.now().isoformat(),
        agent_used="contractor-agent",
        mode="direct"
    )


@app.post("/chat/project")
async def chat_project(request: ChatRequest):
    """Direct access to Project Agent."""
    from agents.project_agent.agent import ProjectAgent

    agent = ProjectAgent()
    response = agent.chat(request.message)
    agent.reset_conversation()

    return ChatResponse(
        response=response,
        success=True,
        timestamp=datetime.now().isoformat(),
        agent_used="project-agent",
        mode="direct"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
