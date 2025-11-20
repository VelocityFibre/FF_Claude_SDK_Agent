#!/usr/bin/env python3
"""
FastAPI Backend for Dual Database AI Agent (Neon + Convex)

Supports both Neon PostgreSQL and Convex databases with switching capability.

Deploy to: Railway, Render, or any Python hosting platform

Usage:
    uvicorn agent_api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import os
import sys
import logging
from datetime import datetime

# Add parent directory to path to import dual_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dual_agent import DualDatabaseAgent, load_env

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
    title="FibreFlow Dual Database AI Agent API",
    description="Natural language interface to Neon PostgreSQL and Convex databases with comparison mode",
    version="2.0.0"
)

# Configure CORS
# Update origins to match your Next.js deployment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Update in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: API Key authentication
API_KEY = os.getenv("AGENT_API_KEY")

# Initialize agent (singleton pattern for performance)
agent = None

def get_agent() -> DualDatabaseAgent:
    """Get or create dual database agent instance."""
    global agent
    if agent is None:
        logger.info("Initializing Dual Database Agent...")
        agent = DualDatabaseAgent()
        logger.info("Agent initialized successfully")
    return agent


# Request/Response models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User's question")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Optional page context")
    database: Optional[Literal["neon", "convex"]] = Field(default=None, description="Which database to query (neon or convex)")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How many active projects do we have?",
                "context": {
                    "page": "dashboard",
                    "userId": "user123"
                },
                "database": "neon"
            }
        }


class ChatResponse(BaseModel):
    response: str = Field(..., description="Agent's answer")
    success: bool = Field(default=True, description="Whether request succeeded")
    timestamp: str = Field(..., description="Response timestamp")
    query_length: int = Field(..., description="Length of user query")
    tool_calls: Optional[list] = Field(default=None, description="Tool calls made during query")
    database_used: Optional[str] = Field(default=None, description="Database queried")


class HealthResponse(BaseModel):
    status: str
    neon_database: str
    convex_database: str
    agent: str
    active_database: str
    timestamp: str


# Verify API key (if configured)
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key if configured."""
    if not API_KEY:
        return  # No API key required

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        if token != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")


# Routes
@app.get("/", tags=["General"])
async def root():
    """API root - basic info."""
    return {
        "service": "FibreFlow Dual Database AI Agent",
        "version": "2.0.0",
        "status": "running",
        "databases": ["neon", "convex"],
        "endpoints": {
            "chat": "/agent/chat (POST) - add 'database' field to select neon or convex",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """
    Health check endpoint.
    Verifies database connections and agent status.
    """
    try:
        # Try to get agent (will initialize if needed)
        agent_instance = get_agent()

        return HealthResponse(
            status="healthy",
            neon_database="connected" if agent_instance.neon_db else "not configured",
            convex_database="connected" if agent_instance.convex_db else "not configured",
            agent="ready",
            active_database=agent_instance.active_db,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.post("/agent/chat", response_model=ChatResponse, tags=["Agent"])
async def chat(
    request: ChatRequest,
    req: Request,
    authorization: Optional[str] = Header(None)
):
    """
    Main chat endpoint.
    Send a natural language query and get a response.

    The agent will:
    1. Understand the question
    2. Query the database
    3. Analyze the results
    4. Return a human-readable answer
    """
    # Verify API key if configured
    if API_KEY:
        await verify_api_key(authorization)

    start_time = datetime.utcnow()

    try:
        # Get agent instance
        agent_instance = get_agent()

        # Enhance message with context if provided
        enhanced_message = request.message
        if request.context:
            # Add context hints to the message
            context_hints = []

            if request.context.get("page"):
                context_hints.append(f"[User is on {request.context['page']} page]")

            if request.context.get("projectId"):
                context_hints.append(f"[Current project: {request.context['projectId']}]")

            if request.context.get("contractorId"):
                context_hints.append(f"[Current contractor: {request.context['contractorId']}]")

            if context_hints:
                enhanced_message = " ".join(context_hints) + " " + request.message

        # Determine which database to use
        database = request.database or agent_instance.active_db

        # Log request
        logger.info(f"Query: {request.message[:100]}... | Database: {database} | Context: {request.context.get('page', 'none')}")

        # Get response from agent with logging
        agent_response = agent_instance.chat(enhanced_message, database=database, return_logs=True)

        # Handle response (dict if return_logs=True, string otherwise)
        if isinstance(agent_response, dict):
            response_text = agent_response["response"]
            tool_calls = agent_response.get("tool_calls", [])
            database_used = agent_response.get("database", database)
        else:
            response_text = agent_response
            tool_calls = []
            database_used = database

        # Calculate duration
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"Response generated in {duration:.2f}s | Length: {len(response_text)} chars | Tools: {len(tool_calls)}")

        return ChatResponse(
            response=response_text,
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            query_length=len(request.message),
            tool_calls=tool_calls,
            database_used=database_used
        )

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "Failed to process query. Please try again.",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.post("/agent/reset", tags=["Agent"])
async def reset_conversation(authorization: Optional[str] = Header(None)):
    """
    Reset the agent's conversation history.
    Useful when starting a new topic.
    """
    # Verify API key if configured
    if API_KEY:
        await verify_api_key(authorization)

    try:
        agent_instance = get_agent()
        agent_instance.reset_conversation()

        logger.info("Conversation reset")

        return {
            "success": True,
            "message": "Conversation history cleared",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "success": False,
        "error": "Internal server error",
        "detail": str(exc) if os.getenv("DEBUG") else "An error occurred",
        "timestamp": datetime.utcnow().isoformat()
    }


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup."""
    logger.info("Starting Dual Database Agent API...")
    try:
        get_agent()  # Initialize agent
        logger.info("Startup complete - API ready")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global agent
    logger.info("Shutting down...")
    if agent:
        agent.close()
    logger.info("Shutdown complete")


# Run with: uvicorn agent_api:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "agent_api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
