#!/usr/bin/env python3
"""
FastAPI Orchestrator API - Intelligent Agent Routing Service

Provides API endpoints for routing tasks to specialized agents using the
efficient skills-based architecture (84% less context, 99% faster).

Deploy to: Any Python hosting platform (Railway, Render, Heroku, VPS)

Usage:
    uvicorn orchestrator_api:app --host 0.0.0.0 --port 8001
"""

from fastapi import FastAPI, HTTPException, Header, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Literal
import os
import sys
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize FastAPI
app = FastAPI(
    title="FibreFlow Agent Orchestrator API",
    description="Intelligent routing to specialized AI agents with skills-based optimization",
    version="3.0.0"
)

# Configure CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: API Key authentication
API_KEY = os.getenv("ORCHESTRATOR_API_KEY")

# Cache for registry (reload every 5 minutes)
registry_cache = {"data": None, "timestamp": None}
CACHE_DURATION = 300  # 5 minutes

# Request/Response Models
class RouteRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=5000, description="Task description to route")
    auto_select: Optional[bool] = Field(default=False, description="Automatically select best agent")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Optional context (page, user, etc)")

    class Config:
        json_schema_extra = {
            "example": {
                "task": "Check CPU usage on the server",
                "auto_select": True,
                "context": {"page": "monitoring", "userId": "user123"}
            }
        }


class ExecuteRequest(BaseModel):
    agent: str = Field(..., description="Agent ID to execute through")
    query: str = Field(..., min_length=1, max_length=5000, description="Query for the agent")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Optional execution context")

    class Config:
        json_schema_extra = {
            "example": {
                "agent": "neon-database",
                "query": "How many active contractors do we have?",
                "context": {"requestId": "req-123"}
            }
        }


class AgentInfo(BaseModel):
    id: str
    name: str
    description: str
    status: str
    triggers: List[str]
    model: str
    cost_per_query: str


class RouteResponse(BaseModel):
    status: Literal["routed", "high_confidence", "multiple_matches", "no_match"]
    agent: Optional[Dict[str, Any]] = None
    alternatives: Optional[List[Dict[str, Any]]] = []
    options: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    task: str
    execution_time_ms: int


class ExecuteResponse(BaseModel):
    success: bool
    agent: str
    query: str
    response: str
    execution_time_ms: int
    model: Optional[str] = None
    error: Optional[str] = None


class WorkforceStats(BaseModel):
    total_agents: int
    active_agents: int
    categories: Dict[str, int]
    agent_types: Dict[str, int]
    models_used: Dict[str, int]
    average_cost: Optional[str]
    summary: Dict[str, Any]


# Helper functions
def load_registry():
    """Load agent registry with caching."""
    global registry_cache

    now = datetime.utcnow()

    # Check cache
    if registry_cache["data"] and registry_cache["timestamp"]:
        cache_age = (now - registry_cache["timestamp"]).total_seconds()
        if cache_age < CACHE_DURATION:
            return registry_cache["data"]

    # Load from file
    registry_path = Path(__file__).parent / "orchestrator" / "registry.json"
    try:
        with open(registry_path, 'r') as f:
            data = json.load(f)
            registry_cache["data"] = data
            registry_cache["timestamp"] = now
            logger.info("Registry loaded and cached")
            return data
    except Exception as e:
        logger.error(f"Failed to load registry: {e}")
        if registry_cache["data"]:
            logger.warning("Using stale cache")
            return registry_cache["data"]
        raise HTTPException(status_code=500, detail=f"Failed to load registry: {str(e)}")


async def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key if configured."""
    if not API_KEY:
        return

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        if token != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")


def run_skill_script(script_path: str, args: List[str]) -> Dict[str, Any]:
    """Run a skill script and return JSON output."""
    try:
        result = subprocess.run(
            [sys.executable, script_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.stdout:
            return json.loads(result.stdout)
        elif result.stderr:
            logger.error(f"Script error: {result.stderr}")
            return {"error": result.stderr}
        else:
            return {"error": "No output from script"}

    except subprocess.TimeoutExpired:
        return {"error": "Script execution timeout"}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON from script: {result.stdout}")
        return {"error": f"Invalid JSON response: {str(e)}"}
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        return {"error": str(e)}


# API Routes
@app.get("/", tags=["General"])
async def root():
    """API root with service information."""
    return {
        "service": "FibreFlow Agent Orchestrator",
        "version": "3.0.0",
        "architecture": "Skills-based (84% less context)",
        "performance": "23ms average routing time",
        "endpoints": {
            "route": "/orchestrator/route (POST)",
            "execute": "/orchestrator/execute (POST)",
            "agents": "/orchestrator/agents (GET)",
            "stats": "/orchestrator/stats (GET)",
            "health": "/health (GET)",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint."""
    try:
        registry = load_registry()
        return {
            "status": "healthy",
            "total_agents": len(registry.get("agents", [])),
            "registry_loaded": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@app.post("/orchestrator/route", response_model=RouteResponse, tags=["Orchestrator"])
async def route_task(
    request: RouteRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Route a task to the most appropriate agent.

    Uses keyword matching to find the best agent for the task.
    Returns routing decision with confidence scores.
    """
    if API_KEY:
        await verify_api_key(authorization)

    start_time = datetime.utcnow()

    # Run routing script
    script_path = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "route_task.py"

    args = ["--task", request.task]
    if request.auto_select:
        args.append("--auto-select")

    result = run_skill_script(str(script_path), args)

    # Calculate execution time
    execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    logger.info(f"Routed task in {execution_time_ms}ms | Status: {result.get('status')} | Task: {request.task[:50]}...")

    # Add execution time to response
    result["execution_time_ms"] = execution_time_ms

    return RouteResponse(**result)


@app.post("/orchestrator/execute", response_model=ExecuteResponse, tags=["Orchestrator"])
async def execute_agent(
    request: ExecuteRequest,
    authorization: Optional[str] = Header(None),
    background_tasks: BackgroundTasks = None
):
    """
    Execute a query through a specific agent.

    Directly executes the query through the specified agent.
    For long-running tasks, consider using background execution.
    """
    if API_KEY:
        await verify_api_key(authorization)

    start_time = datetime.utcnow()

    # Run execution script
    script_path = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "execute_agent.py"

    args = ["--agent", request.agent, "--query", request.query]

    result = run_skill_script(str(script_path), args)

    # Calculate execution time
    execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    logger.info(f"Executed via {request.agent} in {execution_time_ms}ms | Success: {result.get('success', False)}")

    return ExecuteResponse(
        success=result.get("success", False),
        agent=request.agent,
        query=request.query,
        response=result.get("response", result.get("error", "Execution failed")),
        execution_time_ms=execution_time_ms,
        model=result.get("model"),
        error=result.get("error")
    )


@app.get("/orchestrator/agents", response_model=List[AgentInfo], tags=["Orchestrator"])
async def list_agents(
    category: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    List all available agents.

    Returns information about registered agents.
    Optionally filter by category.
    """
    if API_KEY:
        await verify_api_key(authorization)

    # Run list agents script
    script_path = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "list_agents.py"

    args = []
    if category:
        args.extend(["--category", category])

    result = run_skill_script(str(script_path), args)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Transform to AgentInfo models
    agents = []
    for agent_data in result.get("agents", []):
        agents.append(AgentInfo(
            id=agent_data["id"],
            name=agent_data["name"],
            description=agent_data["description"],
            status=agent_data["status"],
            triggers=agent_data["triggers"],
            model=agent_data["model"],
            cost_per_query=agent_data["cost_per_query"]
        ))

    return agents


@app.get("/orchestrator/agents/{agent_id}", tags=["Orchestrator"])
async def get_agent(
    agent_id: str,
    authorization: Optional[str] = Header(None)
):
    """Get detailed information about a specific agent."""
    if API_KEY:
        await verify_api_key(authorization)

    # Run agent info script
    script_path = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "agent_info.py"

    result = run_skill_script(str(script_path), ["--agent", agent_id])

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@app.get("/orchestrator/stats", response_model=WorkforceStats, tags=["Orchestrator"])
async def workforce_stats(authorization: Optional[str] = Header(None)):
    """
    Get workforce statistics.

    Returns aggregate statistics about the agent workforce.
    """
    if API_KEY:
        await verify_api_key(authorization)

    # Run stats script
    script_path = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "workforce_stats.py"

    result = run_skill_script(str(script_path), [])

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return WorkforceStats(**result)


@app.post("/orchestrator/smart-execute", tags=["Orchestrator"])
async def smart_execute(
    task: str = Field(..., description="Natural language task"),
    context: Optional[Dict[str, Any]] = Field(default={}, description="Optional context"),
    authorization: Optional[str] = Header(None)
):
    """
    Smart execution: Route and execute in one call.

    Automatically finds the best agent and executes the task.
    Combines routing and execution for convenience.
    """
    if API_KEY:
        await verify_api_key(authorization)

    start_time = datetime.utcnow()

    # First, route the task
    route_script = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "route_task.py"
    route_result = run_skill_script(str(route_script), ["--task", task, "--auto-select"])

    if route_result.get("status") not in ["routed", "high_confidence"]:
        return {
            "success": False,
            "routing": route_result,
            "error": "Could not find suitable agent",
            "execution_time_ms": int((datetime.utcnow() - start_time).total_seconds() * 1000)
        }

    # Get the selected agent
    selected_agent = route_result.get("agent", {})
    agent_id = selected_agent.get("agent_id")

    if not agent_id:
        return {
            "success": False,
            "error": "No agent selected",
            "execution_time_ms": int((datetime.utcnow() - start_time).total_seconds() * 1000)
        }

    # Execute through the selected agent
    exec_script = Path(__file__).parent / ".claude" / "skills" / "orchestrator" / "scripts" / "execute_agent.py"
    exec_result = run_skill_script(str(exec_script), ["--agent", agent_id, "--query", task])

    execution_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

    return {
        "success": exec_result.get("success", False),
        "agent": agent_id,
        "agent_name": selected_agent.get("agent_name"),
        "confidence": selected_agent.get("confidence"),
        "matched_keywords": selected_agent.get("matched_keywords", []),
        "task": task,
        "response": exec_result.get("response", exec_result.get("error", "Execution failed")),
        "execution_time_ms": execution_time_ms,
        "model": exec_result.get("model")
    }


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
    """Initialize on startup."""
    logger.info("Starting Agent Orchestrator API...")
    try:
        # Preload registry
        load_registry()
        logger.info("Startup complete - Orchestrator API ready")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Orchestrator API...")


# Run with: uvicorn orchestrator_api:app --reload --host 0.0.0.0 --port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "orchestrator_api:app",
        host="0.0.0.0",
        port=int(os.getenv("ORCHESTRATOR_PORT", 8001)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )