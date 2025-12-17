"""
Metrics Collection System for FibreFlow Agent Workforce

Tracks:
- Agent performance (response time, success rate)
- Skill usage and effectiveness
- Token consumption
- System health
- Error rates
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import threading


@dataclass
class MetricEvent:
    """Single metric event"""
    timestamp: str
    metric_type: str  # agent, skill, system, error
    name: str  # agent/skill name
    operation: str  # query, execute, health_check, etc.
    duration_ms: float
    success: bool
    tokens_used: Optional[int] = None
    context_tokens: Optional[int] = None
    error_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MetricsCollector:
    """Thread-safe metrics collection"""

    def __init__(self, metrics_dir: Path = Path("metrics")):
        self.metrics_dir = metrics_dir
        self.metrics_dir.mkdir(parents=True, exist_ok=True)

        self.events: List[MetricEvent] = []
        self.lock = threading.Lock()

        # In-memory aggregates for fast queries
        self.agent_stats = defaultdict(lambda: {
            "total_calls": 0,
            "success_count": 0,
            "total_duration_ms": 0,
            "total_tokens": 0,
            "errors": defaultdict(int)
        })

        self.skill_stats = defaultdict(lambda: {
            "total_calls": 0,
            "success_count": 0,
            "total_duration_ms": 0,
            "total_context_tokens": 0,
        })

    def record_agent_call(
        self,
        agent_name: str,
        operation: str,
        duration_ms: float,
        success: bool,
        tokens_used: Optional[int] = None,
        error_type: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        """Record an agent call"""
        event = MetricEvent(
            timestamp=datetime.utcnow().isoformat(),
            metric_type="agent",
            name=agent_name,
            operation=operation,
            duration_ms=duration_ms,
            success=success,
            tokens_used=tokens_used,
            error_type=error_type,
            metadata=metadata,
        )

        with self.lock:
            self.events.append(event)
            stats = self.agent_stats[agent_name]
            stats["total_calls"] += 1
            if success:
                stats["success_count"] += 1
            stats["total_duration_ms"] += duration_ms
            if tokens_used:
                stats["total_tokens"] += tokens_used
            if error_type:
                stats["errors"][error_type] += 1

    def record_skill_execution(
        self,
        skill_name: str,
        operation: str,
        duration_ms: float,
        success: bool,
        context_tokens: Optional[int] = None,
        metadata: Optional[Dict] = None,
    ):
        """Record a skill execution"""
        event = MetricEvent(
            timestamp=datetime.utcnow().isoformat(),
            metric_type="skill",
            name=skill_name,
            operation=operation,
            duration_ms=duration_ms,
            success=success,
            context_tokens=context_tokens,
            metadata=metadata,
        )

        with self.lock:
            self.events.append(event)
            stats = self.skill_stats[skill_name]
            stats["total_calls"] += 1
            if success:
                stats["success_count"] += 1
            stats["total_duration_ms"] += duration_ms
            if context_tokens:
                stats["total_context_tokens"] += context_tokens

    def get_agent_summary(self, agent_name: str) -> Dict:
        """Get summary statistics for an agent"""
        with self.lock:
            stats = self.agent_stats[agent_name]

            if stats["total_calls"] == 0:
                return {"agent": agent_name, "status": "no_data"}

            return {
                "agent": agent_name,
                "total_calls": stats["total_calls"],
                "success_rate": stats["success_count"] / stats["total_calls"],
                "avg_duration_ms": stats["total_duration_ms"] / stats["total_calls"],
                "avg_tokens": stats["total_tokens"] / stats["total_calls"] if stats["total_tokens"] > 0 else 0,
                "errors": dict(stats["errors"]),
            }

    def get_skill_summary(self, skill_name: str) -> Dict:
        """Get summary statistics for a skill"""
        with self.lock:
            stats = self.skill_stats[skill_name]

            if stats["total_calls"] == 0:
                return {"skill": skill_name, "status": "no_data"}

            return {
                "skill": skill_name,
                "total_calls": stats["total_calls"],
                "success_rate": stats["success_count"] / stats["total_calls"],
                "avg_duration_ms": stats["total_duration_ms"] / stats["total_calls"],
                "avg_context_tokens": stats["total_context_tokens"] / stats["total_calls"] if stats["total_context_tokens"] > 0 else 0,
            }

    def get_all_agents_summary(self) -> List[Dict]:
        """Get summary for all agents"""
        with self.lock:
            return [
                self.get_agent_summary(agent_name)
                for agent_name in self.agent_stats.keys()
            ]

    def get_all_skills_summary(self) -> List[Dict]:
        """Get summary for all skills"""
        with self.lock:
            return [
                self.get_skill_summary(skill_name)
                for skill_name in self.skill_stats.keys()
            ]

    def get_recent_events(self, minutes: int = 60, metric_type: Optional[str] = None) -> List[MetricEvent]:
        """Get events from last N minutes"""
        cutoff = datetime.utcnow() - timedelta(minutes=minutes)

        with self.lock:
            recent = [
                event for event in self.events
                if datetime.fromisoformat(event.timestamp) > cutoff
            ]

            if metric_type:
                recent = [e for e in recent if e.metric_type == metric_type]

            return recent

    def flush_to_disk(self):
        """Write metrics to disk"""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        metrics_file = self.metrics_dir / f"metrics_{timestamp}.jsonl"

        with self.lock:
            with open(metrics_file, "a") as f:
                for event in self.events:
                    f.write(json.dumps(asdict(event)) + "\n")

            # Clear events after writing
            self.events.clear()

    def generate_report(self, output_file: Optional[Path] = None) -> Dict:
        """Generate a comprehensive metrics report"""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "agents": self.get_all_agents_summary(),
            "skills": self.get_all_skills_summary(),
            "recent_activity": {
                "last_hour": len(self.get_recent_events(60)),
                "last_24h": len(self.get_recent_events(24 * 60)),
            },
        }

        if output_file:
            with open(output_file, "w") as f:
                json.dumps(report, f, indent=2)

        return report


# Global collector instance
_collector: Optional[MetricsCollector] = None


def get_collector() -> MetricsCollector:
    """Get or create the global metrics collector"""
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector


class PerformanceTracker:
    """Context manager for tracking performance"""

    def __init__(
        self,
        name: str,
        operation: str,
        metric_type: str = "agent",
        collector: Optional[MetricsCollector] = None,
    ):
        self.name = name
        self.operation = operation
        self.metric_type = metric_type
        self.collector = collector or get_collector()
        self.start_time = None
        self.success = False
        self.error_type = None
        self.metadata = {}

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        self.success = exc_type is None

        if exc_type:
            self.error_type = exc_type.__name__

        if self.metric_type == "agent":
            self.collector.record_agent_call(
                agent_name=self.name,
                operation=self.operation,
                duration_ms=duration_ms,
                success=self.success,
                error_type=self.error_type,
                metadata=self.metadata,
            )
        elif self.metric_type == "skill":
            self.collector.record_skill_execution(
                skill_name=self.name,
                operation=self.operation,
                duration_ms=duration_ms,
                success=self.success,
                metadata=self.metadata,
            )

    def set_metadata(self, **kwargs):
        """Add metadata to the metric"""
        self.metadata.update(kwargs)


if __name__ == "__main__":
    # Test metrics collection
    collector = MetricsCollector()

    # Simulate some agent calls
    with PerformanceTracker("neon-database", "query", "agent", collector) as tracker:
        tracker.set_metadata(query_type="SELECT")
        time.sleep(0.02)  # 20ms

    with PerformanceTracker("vps-monitor", "health_check", "agent", collector) as tracker:
        time.sleep(0.01)  # 10ms

    # Simulate a skill execution
    with PerformanceTracker("database-operations", "execute", "skill", collector):
        time.sleep(0.025)  # 25ms

    # Generate report
    report = collector.generate_report()

    print("📊 Metrics Collection Test")
    print("\nAgent Summary:")
    for agent in report["agents"]:
        print(f"  {agent['agent']}: {agent.get('avg_duration_ms', 0):.1f}ms avg")

    print("\nSkill Summary:")
    for skill in report["skills"]:
        print(f"  {skill['skill']}: {skill.get('avg_duration_ms', 0):.1f}ms avg")

    print(f"\n✅ Metrics collection test complete")
