# Phase 4 Specification: Team Alignment & Collective Coordination

**Target Level**: Jules Level 4 (Team Alignment)
**Timeline**: 2-3 days implementation
**Estimated Cost**: ~$15-25/month operational

## Overview

Phase 4 transforms FibreFlow from **individual developer intelligence** to **team-wide coordination**. The system will predict merge conflicts before they happen, distribute workload intelligently, and automate knowledge transfer between developers.

## Architecture Evolution

```
Phase 1: Observation      → Discovers tasks (individual)
Phase 2: Automation       → Executes fixes (individual)
Phase 3: Intelligence     → Predicts impact, learns patterns (individual)
Phase 4: Team Alignment   → Coordinates team, prevents conflicts (collective)
```

## Core Components

### 1. Conflict Predictor

**Purpose**: Predict merge conflicts before they happen

**Features**:
- Analyze all active branches
- Detect overlapping file modifications
- Predict semantic conflicts (not just textual)
- Calculate conflict probability
- Suggest merge order
- Alert developers before conflict

**Architecture**:
```
Git Branches → Conflict Analysis
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
    Textual     Semantic    Function
    Conflicts   Conflicts   Signature
        ↓           ↓       Conflicts
        └───────────┴───────────┘
                    ↓
            Conflict Probability
                    ↓
            Merge Order Suggestion
                    ↓
            Developer Alerts
```

**Conflict Types**:

1. **Textual Conflicts** (Easy)
   - Same lines modified in different branches
   - Detected by git diff
   - High confidence

2. **Semantic Conflicts** (Medium)
   - Same function modified differently
   - One branch changes signature, another calls it
   - Requires AST analysis

3. **Integration Conflicts** (Hard)
   - Different parts of system incompatible
   - One branch changes API, another uses old API
   - Requires integration testing

**Prediction Algorithm**:
```python
def predict_conflict(branch_a: str, branch_b: str) -> Dict[str, Any]:
    """Predict conflict between two branches."""

    # Get changed files in each branch
    files_a = get_changed_files(branch_a)
    files_b = get_changed_files(branch_b)

    # Overlapping files?
    overlap = files_a & files_b

    if not overlap:
        return {"probability": 0.0, "type": "none"}

    # Check for textual conflicts
    textual = check_textual_conflicts(overlap, branch_a, branch_b)

    # Check for semantic conflicts
    semantic = check_semantic_conflicts(overlap, branch_a, branch_b)

    # Check for integration conflicts
    integration = check_integration_conflicts(branch_a, branch_b)

    # Calculate probability
    probability = calculate_conflict_probability(
        textual=textual,
        semantic=semantic,
        integration=integration
    )

    return {
        "probability": probability,
        "type": get_highest_severity(textual, semantic, integration),
        "overlapping_files": len(overlap),
        "textual_conflicts": len(textual),
        "semantic_conflicts": len(semantic),
        "integration_conflicts": len(integration),
        "suggestion": suggest_merge_order(probability)
    }
```

**Alert Thresholds**:
- **Critical (>80%)**: Immediate notification, block merge
- **High (60-80%)**: Warning notification, suggest coordination
- **Medium (40-60%)**: Informational, monitor
- **Low (<40%)**: Safe to merge

**Database Schema**:
```sql
CREATE TABLE conflict_predictions (
    id INTEGER PRIMARY KEY,
    branch_a TEXT NOT NULL,
    branch_b TEXT NOT NULL,
    probability REAL NOT NULL,
    conflict_type TEXT NOT NULL,
    overlapping_files INTEGER DEFAULT 0,
    textual_conflicts INTEGER DEFAULT 0,
    semantic_conflicts INTEGER DEFAULT 0,
    predicted_at TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved_at TEXT,
    actual_conflict BOOLEAN
);
```

**Integration**:
- Git hooks: pre-merge hook
- Background worker: Check all branches every 10 minutes
- Slack notifications: Alert developers
- Web UI: Dashboard showing conflict matrix

---

### 2. Workload Analyzer

**Purpose**: Track and balance developer workload

**Features**:
- Track active branches per developer
- Measure task complexity (lines changed, files touched, cognitive load)
- Calculate workload score
- Suggest task redistribution
- Identify bottlenecks

**Metrics Tracked**:

1. **Active Tasks**
   - Number of branches
   - Number of uncommitted changes
   - Number of open PRs

2. **Task Complexity**
   - Lines of code changed
   - Number of files touched
   - Number of agents modified
   - Integration complexity

3. **Time Metrics**
   - Time since last commit
   - Average commit frequency
   - PR review time

4. **Cognitive Load**
   - Context switches per day
   - Number of different subsystems
   - Dependency complexity

**Workload Score Calculation**:
```python
def calculate_workload_score(developer: str) -> float:
    """Calculate developer workload score (0.0-1.0)."""

    # Get active work
    branches = get_active_branches(developer)
    uncommitted = get_uncommitted_changes(developer)
    open_prs = get_open_prs(developer)

    # Calculate complexity
    total_lines = sum(get_lines_changed(b) for b in branches)
    total_files = sum(get_files_changed(b) for b in branches)
    subsystems = len(get_subsystems_touched(branches))

    # Calculate cognitive load
    context_switches = get_context_switches_today(developer)

    # Weighted score
    score = (
        len(branches) * 0.15 +
        len(open_prs) * 0.15 +
        (total_lines / 1000) * 0.20 +
        (total_files / 50) * 0.15 +
        subsystems * 0.15 +
        (context_switches / 10) * 0.20
    )

    return min(score, 1.0)
```

**Workload Levels**:
- **Overloaded (>0.8)**: Suggest task redistribution
- **Busy (0.6-0.8)**: Normal load
- **Available (0.4-0.6)**: Can take new tasks
- **Light (<0.4)**: Actively looking for work

**Dashboard**:
```
Team Workload Overview:

Developer A: ████████░░ 0.82 (Overloaded)
  - 3 active branches
  - 2 open PRs
  - 450 lines changed
  - High cognitive load

Developer B: ██████░░░░ 0.58 (Available)
  - 1 active branch
  - 0 open PRs
  - 120 lines changed
  - Low cognitive load

Suggestion: Reassign task-456 from Developer A to Developer B
```

**Integration**:
- Git activity monitoring
- PR tracking via GitHub API
- Real-time dashboard
- Slack notifications for overload

---

### 3. Knowledge Graph

**Purpose**: Map expertise across the team

**Features**:
- Track which developers modified which files
- Build expertise graph (developer → subsystem → confidence)
- Suggest reviewers based on expertise
- Identify knowledge silos
- Suggest pairing opportunities

**Graph Structure**:
```
Developer → (commits, lines) → File → (part_of) → Subsystem
    ↓
Expertise Score (0.0-1.0)
```

**Expertise Calculation**:
```python
def calculate_expertise(developer: str, subsystem: str) -> float:
    """Calculate developer expertise in subsystem (0.0-1.0)."""

    # Get subsystem files
    files = get_subsystem_files(subsystem)

    # Calculate contributions
    total_commits = 0
    developer_commits = 0

    for file in files:
        commits = get_file_commits(file)
        total_commits += len(commits)
        developer_commits += len([c for c in commits if c.author == developer])

    # Calculate recency weight
    recent_commits = get_recent_commits(developer, files, days=90)
    recency_weight = len(recent_commits) / max(developer_commits, 1)

    # Calculate diversity (how many files in subsystem)
    files_touched = len([f for f in files if has_committed(developer, f)])
    diversity = files_touched / len(files)

    # Weighted score
    contribution_score = developer_commits / max(total_commits, 1)

    expertise = (
        contribution_score * 0.5 +
        recency_weight * 0.3 +
        diversity * 0.2
    )

    return min(expertise, 1.0)
```

**Knowledge Silos Detection**:
```
⚠️ Knowledge Silo Detected:
  Subsystem: agents/neon-database
  Expert: Developer A (0.92 expertise)
  Next Best: Developer C (0.15 expertise)
  Risk: High (single point of failure)

  Recommendation: Pair Developer A with Developer C on next neon-database task
```

**Reviewer Suggestions**:
```python
def suggest_reviewers(pr: PullRequest, num: int = 2) -> List[str]:
    """Suggest best reviewers for a PR."""

    # Get files changed
    files = pr.get_files_changed()

    # Get subsystems
    subsystems = get_subsystems(files)

    # Calculate expertise for all developers
    candidates = []

    for dev in get_team_members():
        if dev == pr.author:
            continue

        # Average expertise across subsystems
        avg_expertise = sum(
            calculate_expertise(dev, sub) for sub in subsystems
        ) / len(subsystems)

        # Check availability (workload)
        workload = calculate_workload_score(dev)
        availability = 1.0 - workload

        # Combined score
        score = avg_expertise * 0.7 + availability * 0.3

        candidates.append((dev, score, avg_expertise, availability))

    # Sort by score
    candidates.sort(key=lambda x: x[1], reverse=True)

    return [
        {
            "developer": c[0],
            "score": c[1],
            "expertise": c[2],
            "availability": c[3]
        }
        for c in candidates[:num]
    ]
```

**Database Schema**:
```sql
CREATE TABLE developer_expertise (
    developer TEXT NOT NULL,
    subsystem TEXT NOT NULL,
    expertise_score REAL NOT NULL,
    total_commits INTEGER DEFAULT 0,
    recent_commits INTEGER DEFAULT 0,
    files_touched INTEGER DEFAULT 0,
    last_contribution TEXT,
    PRIMARY KEY (developer, subsystem)
);

CREATE TABLE knowledge_silos (
    subsystem TEXT PRIMARY KEY,
    primary_expert TEXT NOT NULL,
    primary_expertise REAL NOT NULL,
    secondary_expert TEXT,
    secondary_expertise REAL,
    risk_level TEXT NOT NULL,
    detected_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

### 4. Team Coordinator

**Purpose**: Intelligently assign tasks to developers

**Features**:
- Analyze new tasks from proactivity queue
- Match tasks to developer expertise
- Balance workload
- Suggest pairing for knowledge transfer
- Optimize for learning opportunities

**Task Assignment Algorithm**:
```python
def assign_task(task: Dict[str, Any]) -> Dict[str, Any]:
    """Suggest best developer for a task."""

    # Get task details
    subsystem = get_subsystem_from_file(task["file"])
    complexity = estimate_complexity(task)

    # Get team members
    team = get_team_members()

    candidates = []

    for dev in team:
        # Calculate fit score
        expertise = calculate_expertise(dev, subsystem)
        workload = calculate_workload_score(dev)
        availability = 1.0 - workload

        # Learning opportunity (lower expertise = more learning)
        learning_value = 1.0 - expertise

        # Different strategies
        fit_score_performance = expertise * 0.8 + availability * 0.2
        fit_score_learning = learning_value * 0.5 + availability * 0.5

        candidates.append({
            "developer": dev,
            "fit_score_performance": fit_score_performance,
            "fit_score_learning": fit_score_learning,
            "expertise": expertise,
            "availability": availability
        })

    # Sort by performance score (default)
    candidates.sort(key=lambda x: x["fit_score_performance"], reverse=True)

    return {
        "task": task["id"],
        "recommended": candidates[0]["developer"],
        "alternatives": candidates[1:3],
        "strategy": "performance",
        "learning_opportunity": candidates[0]["fit_score_learning"]
    }
```

**Assignment Strategies**:

1. **Performance** (Default)
   - Assign to most expert developer
   - Fastest completion
   - Use for critical/urgent tasks

2. **Learning**
   - Assign to less expert developer
   - Knowledge transfer
   - Use for non-urgent tasks

3. **Pairing**
   - Assign expert + learner together
   - Best knowledge transfer
   - Use for complex tasks

**Integration**:
- Proactivity queue: Suggest assignments for new tasks
- Slack: "@developer, you're the best fit for task-123"
- Dashboard: Task assignment board

---

### 5. Handoff Assistant

**Purpose**: Automate knowledge transfer when developers switch tasks

**Features**:
- Generate handoff documents automatically
- Summarize uncommitted work
- Document decision rationale
- Create todo lists for successor
- Archive context for future reference

**Handoff Document Generation**:
```python
def generate_handoff(developer: str, branch: str) -> Dict[str, Any]:
    """Generate handoff document for a branch."""

    # Get branch details
    commits = get_commits(branch)
    files_changed = get_files_changed(branch)
    uncommitted = get_uncommitted_changes(developer, branch)

    # Analyze changes
    subsystems = get_subsystems(files_changed)
    complexity = estimate_branch_complexity(branch)

    # Extract decisions from commits
    decisions = extract_decisions_from_commits(commits)

    # Generate todos from uncommitted work
    todos = generate_todos_from_uncommitted(uncommitted)

    # Use Claude to generate summary
    summary = generate_summary_with_llm(
        commits=commits,
        files=files_changed,
        decisions=decisions
    )

    return {
        "branch": branch,
        "developer": developer,
        "summary": summary,
        "subsystems_touched": subsystems,
        "complexity": complexity,
        "decisions_made": decisions,
        "todo_list": todos,
        "uncommitted_work": uncommitted,
        "files_changed": len(files_changed),
        "commits": len(commits),
        "suggested_successor": suggest_successor(branch, developer)
    }
```

**Handoff Document Structure**:
```markdown
# Handoff Document: Feature Branch XYZ

**From**: Developer A
**Generated**: 2025-12-16 14:30
**Branch**: feature/add-consequence-analyzer
**Duration**: 2 days
**Complexity**: High

## Summary

This branch implements a consequence awareness analyzer that predicts
real-world impact of code changes before deployment. The system analyzes
API, database, performance, and user impact categories.

## What's Complete

✅ Impact analysis for API endpoints
✅ Database schema change detection
✅ Performance anti-pattern detection
✅ Blast radius calculation

## What's In Progress

🔄 User impact calculation (70% done)
  - File: shared/consequence_analyzer.py:234
  - Next: Add UI change detection

## Uncommitted Changes

- consequence_analyzer.py: 45 lines (local testing)
- test_consequence.py: 23 lines (new test cases)

## Key Decisions Made

1. **Regex-based pattern matching** (commit abc123)
   - Rationale: Fast, deterministic, no LLM needed
   - Alternative considered: LLM-based analysis (too expensive)

2. **Four impact categories** (commit def456)
   - API, Database, Performance, User
   - Rationale: Covers all deployment risks

## Todo List for Successor

- [ ] Complete user impact calculation
- [ ] Add integration test for high-impact scenarios
- [ ] Update documentation with usage examples
- [ ] Run full test suite
- [ ] Create PR with description

## Files to Understand

- `shared/consequence_analyzer.py` (main implementation)
- `PHASE3_SPEC.md` (specification)
- `tests/test_consequence.py` (test cases)

## Recommended Successor

**Developer B** (0.65 expertise in shared modules, 0.42 workload)

## Questions to Ask Me

- How does blast radius scoring work?
- Why did we choose regex over LLM analysis?
- What's the performance threshold for alerts?
```

**Integration**:
- Git hooks: Generate on branch switch
- Slack: Share handoff document with team
- Wiki: Archive for future reference

---

## Implementation Order

### Week 1: Foundation (Days 1-2)
1. ✅ Conflict Predictor
2. ✅ Workload Analyzer

### Week 2: Intelligence (Days 3-4)
3. ✅ Knowledge Graph
4. ✅ Team Coordinator

### Week 3: Automation (Day 5)
5. ✅ Handoff Assistant

## Success Criteria

- [ ] Conflict predictions >80% accuracy
- [ ] Workload balanced across team (no single overload)
- [ ] Knowledge silos identified and addressed
- [ ] Task assignments match expertise
- [ ] Handoff documents reduce onboarding time by 50%

## Cost Estimates

| Component | API Calls | Cost/Month |
|-----------|-----------|------------|
| Conflict Predictor | $0 (deterministic) | $0 |
| Workload Analyzer | $0 (git analysis) | $0 |
| Knowledge Graph | $0 (local analysis) | $0 |
| Team Coordinator | ~$0.01/task | ~$5 (500 tasks) |
| Handoff Assistant | ~$0.02/handoff | ~$10 (500 handoffs) |
| **Total Phase 4** | | **~$15/month** |

**Combined Operational Cost** (Phases 1-4): ~$40-47/month

## Comparison to Jules

| Feature | Jules Level 4 | FibreFlow Phase 4 |
|---------|---------------|-------------------|
| Conflict Prediction | ✅ | ✅ |
| Workload Balancing | ✅ | ✅ |
| Knowledge Graph | ✅ | ✅ |
| Task Assignment | ✅ | ✅ |
| Handoff Automation | ✅ | ✅ |
| Meta-Learning | ⏳ Jules Level 5 | ❌ Future |

**Achievement Target**: FibreFlow at **Jules Level 4** (Team Alignment)

## Risk Mitigation

1. **Privacy Concerns**: All data stays local (no external sharing)
2. **Gaming the System**: Track both quantity and quality metrics
3. **False Positives**: Conflict predictions require validation
4. **Overload Alerts**: Configurable thresholds per team
5. **Knowledge Silos**: Balance performance vs learning

---

**Phase 4: Ready to Build**

This specification provides the roadmap for FibreFlow to achieve Jules Level 4 (Team Alignment). Implementation focuses on multi-developer coordination, conflict prevention, and knowledge transfer automation.
