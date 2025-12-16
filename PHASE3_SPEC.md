# Phase 3 Specification: Live Data Integration & Collective Intelligence

**Target Level**: Jules Level 2.5-3.0 (Kitchen Manager + Collective Intelligence)
**Timeline**: 2-3 days implementation
**Estimated Cost**: ~$15-30/month operational

## Overview

Phase 3 transforms FibreFlow from **autonomous maintenance** to **intelligent prediction and collaborative improvement**. The system will correlate live production data with code changes, run multiple agents in parallel for consensus, and learn from developer feedback.

## Architecture Evolution

```
Phase 1: Observation      → Discovers tasks
Phase 2: Automation       → Executes high-confidence fixes
Phase 3: Intelligence     → Predicts impact, learns patterns, multi-agent consensus
```

## Core Components

### 1. Live Data Correlation Engine

**Purpose**: Connect VPS metrics with git commits to understand real-world impact

**Features**:
- Track VPS metrics (CPU, RAM, disk, response time) pre/post commit
- Correlate performance changes with code changes
- Alert when commits cause degradation
- Build historical performance database
- Predict commit impact before deployment

**Architecture**:
```
Git Commit (t0) → Capture VPS Baseline
       ↓
   Deploy
       ↓
Git Commit (t1) → Capture VPS Delta
       ↓
   Analyze Correlation
       ↓
   Update Prediction Model
```

**Implementation**:
- File: `shared/live_data_correlator.py`
- Database: `memory/commit_metrics.db` (SQLite)
- Integration: Extend git hooks to capture metrics
- API: VPS Monitor agent provides current state

**Data Schema**:
```python
{
  "commit_hash": "abc123",
  "timestamp": "2025-12-16T10:00:00Z",
  "metrics_before": {
    "cpu_percent": 15.2,
    "ram_percent": 42.1,
    "disk_percent": 35.8,
    "avg_response_time_ms": 150
  },
  "metrics_after": {
    "cpu_percent": 18.5,
    "ram_percent": 43.2,
    "disk_percent": 35.9,
    "avg_response_time_ms": 165
  },
  "delta": {
    "cpu_delta": +3.3,
    "ram_delta": +1.1,
    "response_time_delta": +15
  },
  "impact_score": "low",  # none/low/medium/high/critical
  "files_changed": ["agents/neon-database/agent.py"],
  "alert_triggered": false
}
```

**Alert Thresholds**:
- **Critical**: Response time +100ms, CPU +20%
- **High**: Response time +50ms, CPU +10%
- **Medium**: Response time +25ms, CPU +5%
- **Low**: Measurable but negligible change
- **None**: Within noise threshold

### 2. Multi-Agent Convergence System

**Purpose**: Run multiple specialized agents on the same commit for consensus-driven analysis

**Agents**:
1. **Code Critic** (already exists) - Security, performance, best practices
2. **Test Generator** (new) - Generates missing tests
3. **Doc Writer** (new) - Generates/updates documentation
4. **Impact Analyzer** (new) - Predicts user-facing consequences

**Convergence Flow**:
```
Git Commit → Orchestrator
                ↓
    ┌───────────┼───────────┬───────────┐
    ↓           ↓           ↓           ↓
Critic      Test-Gen    Doc-Writer  Impact
    ↓           ↓           ↓           ↓
    └───────────┴───────────┴───────────┘
                ↓
        Convergence Layer
                ↓
        Unified Report
                ↓
        Proactivity Queue
```

**Convergence Rules**:
- If 2+ agents agree on issue → High confidence
- If 1 agent finds critical issue → Immediate alert
- If agents disagree → Human review required
- Generate unified task list (no duplicates)

**Implementation**:
- File: `orchestrator/convergence.py`
- Parallel execution using `asyncio`
- Timeout: 30 seconds per agent
- Failure handling: Continue with successful agents

### 3. Test Generator Agent

**Purpose**: Automatically generate missing test coverage

**Capabilities**:
- Detect functions without tests
- Generate pytest test stubs
- Infer test cases from docstrings
- Create integration tests for tools
- Mock external dependencies

**Tool Definition**:
```python
{
  "name": "generate_tests",
  "description": "Generate pytest tests for untested functions",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string"},
      "function_name": {"type": "string"},
      "test_type": {"type": "string", "enum": ["unit", "integration"]}
    }
  }
}
```

**Example Output**:
```python
# Generated test for neon_agent.py::execute_query()
@pytest.mark.unit
@pytest.mark.neon
def test_execute_query_success(neon_agent):
    result = neon_agent.execute_query(
        query="SELECT COUNT(*) FROM contractors"
    )
    assert result["success"] == True
    assert "data" in result
    assert isinstance(result["data"], list)

@pytest.mark.unit
@pytest.mark.neon
def test_execute_query_syntax_error(neon_agent):
    result = neon_agent.execute_query(
        query="INVALID SQL"
    )
    assert result["success"] == False
    assert "error" in result
```

**Integration**:
- File: `agents/test-generator/agent.py`
- Inherits: `BaseAgent`
- Model: Haiku (cheap, fast test generation)
- Validates: Generated tests must actually run

### 4. Doc Writer Agent

**Purpose**: Automatically maintain up-to-date documentation

**Capabilities**:
- Generate docstrings for undocumented functions
- Update README.md when tools change
- Create usage examples
- Generate API documentation
- Update CLAUDE.md for architectural changes

**Tool Definition**:
```python
{
  "name": "write_docstring",
  "description": "Generate Google-style docstring for function",
  "input_schema": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string"},
      "function_name": {"type": "string"},
      "function_signature": {"type": "string"}
    }
  }
}
```

**Example Output**:
```python
def execute_query(self, query: str, params: Dict = None) -> Dict[str, Any]:
    """Execute SQL query against Neon PostgreSQL database.

    Supports parameterized queries for SQL injection prevention.

    Args:
        query: SQL query string (can use %s placeholders)
        params: Optional dictionary of query parameters

    Returns:
        Dict with keys:
            - success (bool): Whether query succeeded
            - data (list): Query results (if SELECT)
            - rows_affected (int): Number of rows affected (if INSERT/UPDATE/DELETE)
            - error (str): Error message (if failed)

    Example:
        >>> result = agent.execute_query(
        ...     query="SELECT * FROM contractors WHERE status = %s",
        ...     params={"status": "active"}
        ... )
        >>> print(result["data"])
        [{"id": 1, "name": "John Doe", ...}]

    Raises:
        None - All errors returned in result dict
    """
```

**Integration**:
- File: `agents/doc-writer/agent.py`
- Inherits: `BaseAgent`
- Model: Sonnet (better writing quality)

### 5. Consequence Awareness Analyzer

**Purpose**: Predict real-world impact of code changes on users

**Analysis Types**:

**1. API Impact**:
- Does commit change public API?
- Are endpoints added/removed/modified?
- Will existing clients break?

**2. Database Impact**:
- Does commit modify schema?
- Will migrations break production?
- Are there data consistency risks?

**3. Performance Impact**:
- Does commit add expensive operations?
- Are there new N+1 queries?
- Will response times degrade?

**4. User Impact**:
- Does commit affect UI/UX?
- Are there breaking changes?
- How many users affected?

**Impact Score**:
```python
{
  "overall_impact": "medium",  # none/low/medium/high/critical
  "categories": {
    "api": {"level": "high", "reason": "Removed /legacy endpoint"},
    "database": {"level": "none", "reason": "No schema changes"},
    "performance": {"level": "low", "reason": "Added index optimization"},
    "user": {"level": "medium", "reason": "Changed button color"}
  },
  "blast_radius": {
    "affected_files": 5,
    "affected_endpoints": 1,
    "affected_users": "~50% (estimated)"
  },
  "recommendations": [
    "Deploy during low-traffic window",
    "Notify users of /legacy endpoint deprecation",
    "Monitor error rates for 24h post-deployment"
  ]
}
```

**Implementation**:
- File: `shared/consequence_analyzer.py`
- Integration: Runs on every commit before deployment
- Alerts: Critical/high impact requires approval

### 6. E2B Sandbox Integration

**Purpose**: Run fixes in isolated sandboxes and choose best result

**Architecture**:
```
Auto-Fix Task → Generate 3 Variations
                      ↓
          ┌───────────┼───────────┐
          ↓           ↓           ↓
      Sandbox A   Sandbox B   Sandbox C
          ↓           ↓           ↓
      Run Tests   Run Tests   Run Tests
          ↓           ↓           ↓
          └───────────┴───────────┘
                      ↓
              Choose Best Result
                      ↓
              Apply to Main Repo
```

**Best-of-N Strategy**:
- Generate N variations of the same fix
- Run in parallel sandboxes
- Measure: test pass rate, execution time, code quality
- Select: highest scoring variation
- Apply: winning fix to main repository

**E2B Setup**:
```bash
pip install e2b-sdk
export E2B_API_KEY=your_key_here
```

**Implementation**:
```python
from e2b import Sandbox

async def execute_fix_with_best_of_n(task: Dict, n: int = 3) -> Dict:
    """Execute fix with best-of-n parallel sandboxes."""

    # Generate n variations
    variations = generate_fix_variations(task, count=n)

    # Run in parallel sandboxes
    results = await asyncio.gather(*[
        run_in_sandbox(variation) for variation in variations
    ])

    # Score results
    scored = [score_result(r) for r in results]

    # Choose winner
    winner = max(scored, key=lambda x: x["score"])

    return winner
```

**Cost**: ~$0.05-0.10 per fix (3 sandboxes × 30 seconds)

### 7. Pattern Learning & Feedback System

**Purpose**: Learn from developer decisions to improve predictions

**Learning Sources**:
1. **Approval/Rejection**: Which suggested tasks get approved?
2. **Manual Edits**: How do developers modify generated code?
3. **Reverted Fixes**: Which auto-fixes get manually reverted?
4. **Test Failures**: Which patterns cause tests to fail?

**Learning Loop**:
```
System Suggests Fix
        ↓
Developer Approves/Rejects/Edits
        ↓
    Log Decision
        ↓
Update Pattern Weights
        ↓
Improve Future Suggestions
```

**Feedback Database**:
```python
{
  "task_id": "task-001",
  "type": "unused_import",
  "suggested_fix": "Remove line 12",
  "developer_action": "approved",  # approved/rejected/edited/reverted
  "developer_edit": null,  # If edited, what changed
  "time_to_decision_seconds": 5,
  "confidence_was": "high",
  "confidence_should_be": "high",  # Updated based on outcome
  "pattern_weight_delta": +0.1  # Increase confidence in this pattern
}
```

**Pattern Weight Updates**:
- **Approved**: +0.1 to pattern weight
- **Rejected**: -0.2 to pattern weight
- **Edited**: -0.05 to pattern weight (partial success)
- **Reverted**: -0.3 to pattern weight (failure)

**Implementation**:
- File: `memory/feedback.db` (SQLite)
- File: `shared/pattern_learner.py`
- Integration: Update weights weekly via cron job

### 8. Cross-Repository Knowledge Sharing

**Purpose**: Share learnings across multiple FibreFlow deployments

**Architecture**:
```
FibreFlow Instance A → Shared Knowledge API ← FibreFlow Instance B
        ↓                                              ↓
  Learns Pattern X                              Learns Pattern Y
        ↓                                              ↓
    Uploads Finding                              Uploads Finding
        ↓                                              ↓
        └──────────────→ Both Benefit ←───────────────┘
```

**Shared Knowledge Types**:
- Common auto-fix patterns (high success rate)
- Security vulnerabilities discovered
- Performance optimization patterns
- Best practice recommendations

**Privacy**:
- Only anonymized patterns shared (no code)
- Opt-in sharing (disabled by default)
- Local-only mode available

**Implementation**:
- File: `shared/knowledge_sync.py`
- API: `https://fibreflow-knowledge.example.com/api/v1`
- Optional: Deploy central knowledge API

## Implementation Order

### Week 1: Foundation (Days 1-3)
1. ✅ Live Data Correlator
2. ✅ Test Generator Agent
3. ✅ Doc Writer Agent

### Week 2: Intelligence (Days 4-6)
4. ✅ Multi-Agent Convergence
5. ✅ Consequence Analyzer
6. ✅ Pattern Learning System

### Week 3: Advanced (Days 7-9)
7. ✅ E2B Sandbox Integration
8. ✅ Cross-Repo Knowledge Sharing
9. ✅ Documentation & Testing

## Success Criteria

- [ ] VPS metrics correlated with commits (historical database)
- [ ] Multi-agent convergence generates unified reports
- [ ] Test-gen agent creates runnable pytest tests
- [ ] Doc-writer agent generates Google-style docstrings
- [ ] Consequence analyzer predicts impact accurately
- [ ] E2B sandboxes run best-of-n strategy
- [ ] Pattern learning improves fix success rate 50% → 80%
- [ ] Cross-repo knowledge sharing functional (opt-in)

## Cost Estimates

| Component | API Calls | Cost/Month |
|-----------|-----------|------------|
| Live Data Correlator | $0 (deterministic) | $0 |
| Test Generator | ~$0.01/commit | ~$2.50 (250 commits) |
| Doc Writer | ~$0.02/commit | ~$5 (250 commits) |
| Consequence Analyzer | ~$0.01/commit | ~$2.50 (250 commits) |
| E2B Sandboxes | ~$0.08/fix | ~$4 (50 fixes) |
| Pattern Learning | $0 (local ML) | $0 |
| **Total Phase 3** | | **~$14/month** |

**Combined Operational Cost** (Phases 1-3): ~$19-24/month

## Comparison to Jules

| Feature | Jules Level 3 | FibreFlow Phase 3 |
|---------|---------------|-------------------|
| Live Data Integration | ✅ | ✅ |
| Multi-Agent Convergence | ✅ | ✅ |
| Consequence Awareness | ✅ | ✅ |
| Parallel Sandboxes | ✅ | ✅ |
| Pattern Learning | ✅ | ✅ |
| Cross-Repo Sharing | ✅ | ✅ |
| Team Alignment | ⏳ Jules Level 4 | ❌ Future |
| Meta-Learning | ⏳ Jules Level 4 | ❌ Future |

**Achievement Target**: FibreFlow at **Jules Level 3** (Collective Intelligence)

## Risk Mitigation

1. **E2B Costs**: Set monthly budget cap ($20/month)
2. **False Positives**: Require 2+ agent agreement for high-confidence
3. **Privacy**: Default to local-only mode (no external sharing)
4. **Performance**: Async execution prevents blocking
5. **Complexity**: Each component independently testable

## Next Phase (Phase 4 - Speculative)

**Team Alignment**:
- Multi-developer coordination
- Merge conflict prediction
- Workload distribution
- Knowledge transfer automation

**Meta-Learning**:
- Agent performance optimization
- Self-improving prompts
- Architecture evolution suggestions

---

**Phase 3: Ready to Build**

This specification provides the roadmap for FibreFlow to reach Jules Level 3. Implementation begins with live data correlation and builds up to collective intelligence.
