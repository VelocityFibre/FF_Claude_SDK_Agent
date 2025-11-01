#!/usr/bin/env python3
"""
FastAPI Backend for Neon Database AI Agent

This wraps neon_agent.py and provides a REST API for the Next.js frontend.

Deploy to: Railway, Render, or any Python hosting platform

Usage:
    uvicorn agent_api:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
import sys
import logging
from datetime import datetime

# Add parent directory to path to import neon_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neon_agent import NeonAgent, load_env

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
    title="Neon Database AI Agent API",
    description="Natural language interface to your Neon PostgreSQL database",
    version="1.0.0"
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

def get_agent() -> NeonAgent:
    """Get or create agent instance."""
    global agent
    if agent is None:
        logger.info("Initializing Neon Agent...")
        agent = NeonAgent()
        logger.info("Agent initialized successfully")
    return agent


# Request/Response models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000, description="User's question")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Optional page context")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "How many active projects do we have?",
                "context": {
                    "page": "dashboard",
                    "userId": "user123"
                }
            }
        }


class ChatResponse(BaseModel):
    response: str = Field(..., description="Agent's answer")
    success: bool = Field(default=True, description="Whether request succeeded")
    timestamp: str = Field(..., description="Response timestamp")
    query_length: int = Field(..., description="Length of user query")


class HealthResponse(BaseModel):
    status: str
    database: str
    agent: str
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
        "service": "Neon Database AI Agent",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/agent/chat (POST)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """
    Health check endpoint.
    Verifies database connection and agent status.
    """
    try:
        # Try to get agent (will initialize if needed)
        agent_instance = get_agent()

        # Quick database connectivity test
        # You could add a simple query here if needed

        return HealthResponse(
            status="healthy",
            database="connected",
            agent="ready",
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

        # Log request
        logger.info(f"Query: {request.message[:100]}... | Context: {request.context.get('page', 'none')}")

        # Get response from agent
        response_text = agent_instance.chat(enhanced_message)

        # Calculate duration
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"Response generated in {duration:.2f}s | Length: {len(response_text)} chars")

        return ChatResponse(
            response=response_text,
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            query_length=len(request.message)
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
    logger.info("Starting Neon Agent API...")
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
        agent.db.close()
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
