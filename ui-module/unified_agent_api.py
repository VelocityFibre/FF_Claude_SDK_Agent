#!/usr/bin/env python3
"""
Simple FastAPI Backend for Unified Convex Agent

ONE agent with ALL tools - contractors, projects, tasks, and universal table access.

Usage:
    uvicorn unified_agent_api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from convex_agent import ConvexAgent, load_env

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_env()

# Initialize FastAPI
app = FastAPI(
    title="FibreFlow Unified Convex Agent API",
    description="ONE agent with access to contractors, projects, tasks, and all FibreFlow data",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

def get_agent() -> ConvexAgent:
    """Get or create unified agent."""
    global agent
    if agent is None:
        logger.info("Initializing Unified Convex Agent...")
        agent = ConvexAgent()
        logger.info(f"✅ Agent ready with 17 tools")
    return agent


# Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Show me all contractors"
            }
        }


class ChatResponse(BaseModel):
    response: str
    success: bool = True
    timestamp: str
    tools_available: int = 17


class HealthResponse(BaseModel):
    status: str
    agent: str
    tools: int
    tables_accessible: List[str]
    convex_url: str


# Endpoints
@app.get("/")
async def root():
    """API info."""
    return {
        "name": "Unified Convex Agent API",
        "version": "1.0.0",
        "status": "operational",
        "agent": "ConvexAgent (Unified)",
        "tools": 17,
        "capabilities": [
            "Contractors (9 records)",
            "Projects (2 records)",
            "Tasks",
            "Sync stats"
        ]
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check."""
    try:
        agent = get_agent()

        return HealthResponse(
            status="healthy",
            agent="Unified ConvexAgent",
            tools=17,
            tables_accessible=[
                "contractors (9)",
                "projects (2)",
                "tasks (0)",
                "syncRecords"
            ],
            convex_url=agent.convex_url
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with unified Convex agent.

    ONE agent handles everything:
    - Contractors
    - Projects
    - Tasks
    - Sync operations
    """
    try:
        logger.info(f"Query: {request.message[:100]}")

        agent = get_agent()
        response_text = agent.chat(request.message)

        # Don't reset - maintain conversation context!
        # agent.reset_conversation()

        return ChatResponse(
            response=response_text,
            success=True,
            timestamp=datetime.now().isoformat(),
            tools_available=17
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset():
    """Reset conversation history."""
    try:
        agent = get_agent()
        agent.reset_conversation()
        return {"message": "Conversation reset", "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
