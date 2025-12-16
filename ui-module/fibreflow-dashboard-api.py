"""
FibreFlow Dashboard API

FastAPI backend that serves FibreFlow proactive system data to the React dashboard.

Endpoints:
    GET /api/dashboard/overview - System overview (all metrics)
    GET /api/dashboard/convergence - Latest convergence results
    GET /api/dashboard/consequences - Latest consequence analysis
    GET /api/dashboard/patterns - Pattern learning statistics
    GET /api/dashboard/knowledge - Knowledge graph data
    GET /api/dashboard/workload - Team workload distribution
    GET /api/dashboard/conflicts - Active conflict predictions
    GET /api/dashboard/tasks - Proactivity queue status

Usage:
    uvicorn fibreflow-dashboard-api:app --host 0.0.0.0 --port 8001 --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.confidence import ProactivityQueue
from shared.pattern_learner import PatternLearner
from shared.knowledge_graph import KnowledgeGraph
from shared.workload_analyzer import WorkloadAnalyzer
from shared.conflict_predictor import ConflictPredictor
from shared.consequence_analyzer import ConsequenceAnalyzer

app = FastAPI(title="FibreFlow Dashboard API", version="1.0.0")

# CORS configuration for React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://app.fibreflow.app",  # Production
        "http://app.fibreflow.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/dashboard/overview")
async def get_overview() -> Dict[str, Any]:
    """Get complete system overview."""
    try:
        # Initialize components
        queue = ProactivityQueue()
        learner = PatternLearner()
        workload = WorkloadAnalyzer()

        # Get queue status
        queue_data = queue.load_queue()

        # Get pattern learning summary
        learning = learner.get_learning_summary(days=7)

        # Get team workload
        team = workload.analyze_team()

        return {
            "success": True,
            "timestamp": queue_data.get("last_updated"),
            "queue": {
                "total_tasks": queue_data.get("total_tasks", 0),
                "high_confidence": queue_data.get("high_confidence", 0),
                "medium_confidence": queue_data.get("medium_confidence", 0),
                "low_confidence": queue_data.get("low_confidence", 0)
            },
            "learning": {
                "total_feedback": learning.get("total_feedback", 0),
                "approval_rate": learning.get("approval_rate", 0),
                "rejection_rate": learning.get("rejection_rate", 0)
            },
            "team": {
                "total_developers": team.get("total_developers", 0),
                "overloaded_count": team.get("overloaded_count", 0),
                "average_workload": team.get("average_score", 0)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/convergence/latest")
async def get_latest_convergence() -> Dict[str, Any]:
    """Get latest multi-agent convergence results."""
    try:
        # This would typically fetch from a database
        # For now, return example structure
        return {
            "success": True,
            "commit_hash": "HEAD",
            "agents_run": 3,
            "files_analyzed": 44,
            "tasks_generated": 365,
            "consensus_files": 13,
            "critical_issues": 0,
            "execution_time_seconds": 30,
            "agent_results": {
                "critic": {"success": True, "issues_found": 466},
                "test_gen": {"success": True, "untested_functions": 8},
                "doc_writer": {"success": True, "missing_docstrings": 7}
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/consequences/latest")
async def get_latest_consequences() -> Dict[str, Any]:
    """Get latest consequence analysis."""
    try:
        analyzer = ConsequenceAnalyzer()
        result = analyzer.analyze_commit("HEAD")

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))

        return {
            "success": True,
            "commit_hash": result["commit_hash"][:7],
            "overall_impact": result["overall_impact"],
            "deployment_risk": result["deployment_risk"],
            "categories": result["categories"],
            "blast_radius": result["blast_radius"],
            "recommendations": result["recommendations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/patterns")
async def get_pattern_statistics() -> Dict[str, Any]:
    """Get pattern learning statistics."""
    try:
        learner = PatternLearner()

        # Get all weights
        weights = learner.get_all_weights()

        # Get learning summary
        summary = learner.get_learning_summary(days=30)

        # Get detailed stats for top patterns
        pattern_stats = []
        for pattern in ["unused_import", "n_plus_one_query", "trailing_whitespace"]:
            stats = learner.get_pattern_statistics(pattern)
            if stats.get("success"):
                pattern_stats.append(stats)

        return {
            "success": True,
            "weights": weights,
            "summary": summary,
            "detailed_stats": pattern_stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/knowledge")
async def get_knowledge_graph() -> Dict[str, Any]:
    """Get knowledge graph data."""
    try:
        graph = KnowledgeGraph()

        # Detect silos
        silos = graph.detect_knowledge_silos()

        return {
            "success": True,
            "silos": silos,
            "silo_count": len(silos),
            "critical_silos": len([s for s in silos if s["risk_level"] == "critical"]),
            "high_silos": len([s for s in silos if s["risk_level"] == "high"])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/workload")
async def get_workload_distribution() -> Dict[str, Any]:
    """Get team workload distribution."""
    try:
        analyzer = WorkloadAnalyzer()
        team = analyzer.analyze_team()

        if not team.get("success"):
            raise HTTPException(status_code=500, detail=team.get("error"))

        return {
            "success": True,
            "total_developers": team["total_developers"],
            "average_workload": team["average_score"],
            "distribution": {
                "overloaded": team["overloaded_count"],
                "busy": team["busy_count"],
                "available": team["available_count"],
                "light": team["light_count"]
            },
            "developers": team["developers"],
            "recommendations": team["recommendations"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/conflicts")
async def get_conflict_predictions() -> Dict[str, Any]:
    """Get active conflict predictions."""
    try:
        predictor = ConflictPredictor()
        matrix = predictor.check_all_branches()

        if not matrix.get("success"):
            # Return empty state if no branches
            if "message" in matrix:
                return {
                    "success": True,
                    "conflicts": [],
                    "total_pairs": 0,
                    "message": matrix["message"]
                }
            raise HTTPException(status_code=500, detail=matrix.get("error"))

        return {
            "success": True,
            "total_branches": matrix.get("total_branches", 0),
            "total_pairs_checked": matrix.get("total_pairs_checked", 0),
            "conflicts": matrix.get("conflicts", []),
            "critical_count": matrix.get("critical_count", 0),
            "high_count": matrix.get("high_count", 0),
            "medium_count": matrix.get("medium_count", 0)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/tasks")
async def get_tasks() -> Dict[str, Any]:
    """Get proactivity queue status and recent tasks."""
    try:
        queue = ProactivityQueue()
        data = queue.load_queue()

        # Get high-confidence tasks
        high_conf_tasks = [
            task for task in data.get("tasks", [])
            if task.get("confidence") == "high"
        ][:10]  # Top 10

        return {
            "success": True,
            "total_tasks": data.get("total_tasks", 0),
            "high_confidence": data.get("high_confidence", 0),
            "medium_confidence": data.get("medium_confidence", 0),
            "low_confidence": data.get("low_confidence", 0),
            "recent_tasks": high_conf_tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "FibreFlow Dashboard API"}


if __name__ == "__main__":
    import uvicorn
    print("Starting FibreFlow Dashboard API on http://localhost:8001")
    print("API documentation: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
