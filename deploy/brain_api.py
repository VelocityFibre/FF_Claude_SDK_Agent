#!/usr/bin/env python3
"""
FastAPI Backend for Superior Brain Agent

Provides RESTful API for the Superior Brain with memory systems.
Runs on port 8001 alongside the Dual Agent (port 8000).

Usage:
    uvicorn brain_api:app --host 0.0.0.0 --port 8001
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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Superior Brain
try:
    from superior_agent_brain import SuperiorAgentBrain
except ImportError:
    SuperiorAgentBrain = None
    logging.warning("Superior Brain not available - check dependencies")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment
def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# Initialize FastAPI
app = FastAPI(
    title="FibreFlow Superior Brain API",
    description="Advanced AI agent with memory, learning, and multi-agent orchestration",
    version="2.0.0"
)

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize brain (singleton)
brain = None

def get_brain() -> SuperiorAgentBrain:
    """Get or create brain instance."""
    global brain
    if brain is None and SuperiorAgentBrain is not None:
        logger.info("Initializing Superior Brain...")
        # Initialize with optional components based on availability
        brain = SuperiorAgentBrain(
            enable_vector_memory=True,  # Requires Qdrant
            enable_persistent_memory=True,  # Requires Neon
            enable_meta_learning=True,
            enable_knowledge_graph=True,
            enable_orchestration=True
        )
        logger.info("Superior Brain initialized")
    return brain


# Request/Response Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    user_id: Optional[str] = Field(default="anonymous")
    use_memory: bool = Field(default=True, description="Use vector memory for recall")
    use_orchestration: bool = Field(default=True, description="Route to specialized agents")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "What patterns do you see in our contractor data?",
                "user_id": "user_123",
                "use_memory": True,
                "use_orchestration": True
            }
        }


class ChatResponse(BaseModel):
    response: str
    success: bool = True
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    status: str
    components: Dict[str, bool]
    timestamp: str
    brain_initialized: bool


# Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint - API info."""
    return {
        "name": "Superior Brain API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "docs": "/docs",
            "memory_stats": "/memory/stats"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check with component status."""
    brain_instance = None
    components = {
        "api": True,
        "brain": False,
        "vector_memory": False,
        "persistent_memory": False,
        "orchestration": False,
        "meta_learning": False,
        "knowledge_graph": False
    }

    try:
        brain_instance = get_brain()
        if brain_instance:
            components["brain"] = True
            components["vector_memory"] = brain_instance.vector_memory is not None
            components["persistent_memory"] = brain_instance.persistent_memory is not None
            components["orchestration"] = brain_instance.orchestrator is not None
            components["meta_learning"] = brain_instance.meta_learner is not None
            components["knowledge_graph"] = brain_instance.knowledge_graph is not None
    except Exception as e:
        logger.error(f"Health check error: {e}")

    return HealthResponse(
        status="healthy" if components["brain"] else "degraded",
        components=components,
        timestamp=datetime.utcnow().isoformat(),
        brain_initialized=brain_instance is not None
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the Superior Brain.

    Uses memory, learning, and orchestration for intelligent responses.
    """
    start_time = datetime.utcnow()

    try:
        brain_instance = get_brain()
        if not brain_instance:
            raise HTTPException(
                status_code=503,
                detail="Superior Brain not available - check Qdrant and database connections"
            )

        # Process query through brain
        result = brain_instance.process_query(
            query=request.message,
            user_id=request.user_id
        )

        execution_time = (datetime.utcnow() - start_time).total_seconds()

        # Add execution time to metadata
        if result.get("metadata"):
            result["metadata"]["execution_time_seconds"] = execution_time

        return ChatResponse(
            response=result.get("response", "No response generated"),
            success=True,
            timestamp=datetime.utcnow().isoformat(),
            metadata=result.get("metadata")
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/memory/stats")
async def memory_stats():
    """Get memory system statistics."""
    try:
        brain_instance = get_brain()
        if not brain_instance:
            return {"error": "Brain not initialized"}

        stats = {}

        # Vector memory stats
        if brain_instance.vector_memory:
            try:
                collection = brain_instance.vector_memory.client.get_collection(
                    collection_name=brain_instance.vector_memory.collection_name
                )
                stats["vector_memory"] = {
                    "vectors_count": collection.vectors_count or 0,
                    "status": "available"
                }
            except Exception as e:
                stats["vector_memory"] = {"status": "error", "message": str(e)}

        # Persistent memory stats
        if brain_instance.persistent_memory:
            # This would query Neon for conversation count, etc.
            stats["persistent_memory"] = {"status": "available"}

        return stats

    except Exception as e:
        logger.error(f"Memory stats error: {e}")
        return {"error": str(e)}


@app.post("/memory/consolidate")
async def consolidate_memory():
    """
    Trigger memory consolidation (like sleep).

    This optimizes memory by compressing old data and improving recall.
    Should be run periodically (weekly).
    """
    try:
        brain_instance = get_brain()
        if not brain_instance or not brain_instance.consolidator:
            raise HTTPException(status_code=503, detail="Consolidator not available")

        # Run consolidation
        result = brain_instance.sleep(
            conversation_days=7,
            performance_days=14
        )

        return {
            "status": "completed",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Consolidation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Startup/Shutdown events

@app.on_event("startup")
async def startup_event():
    """Initialize brain on startup."""
    logger.info("🧠 Starting Superior Brain API...")
    try:
        get_brain()
        logger.info("✅ Superior Brain API ready")
    except Exception as e:
        logger.error(f"❌ Failed to initialize brain: {e}")
        logger.warning("⚠️  API will run in degraded mode")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global brain
    logger.info("Shutting down Superior Brain API...")
    if brain:
        try:
            brain.close()
        except:
            pass
    logger.info("Shutdown complete")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
