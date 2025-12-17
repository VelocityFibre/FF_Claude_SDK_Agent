# Domain Memory Implementation Summary

**Date**: 2025-12-09
**Based on**: Anthropic's "Building Effective Agents" insights
**Status**: ✅ Complete - Knowledge base updated

---

## What Changed

### 1. New Documentation: `DOMAIN_MEMORY_GUIDE.md`

**Comprehensive 200+ line guide** covering:
- The problem with generalized agents ("amnesiacs with tool belts")
- FibreFlow's two memory systems (domain memory vs Superior Agent Brain)
- When to use which memory system
- Design principles for domain memory
- Domain memory schemas for non-coding tasks
- Implementation patterns
- Common pitfalls
- Strategic implications (your moat isn't smarter AI, it's better memory schemas)

**Location**: `/home/louisdup/Agents/claude/DOMAIN_MEMORY_GUIDE.md`

---

### 2. Updated: `CLAUDE.md`

**Changes**:
- Added explicit "Core Principle" under Memory Systems section
- Distinguished between Domain Memory (task state) vs Superior Agent Brain (learning)
- Added when-to-use guidance for each memory system
- Referenced new DOMAIN_MEMORY_GUIDE.md in documentation structure
- Updated Special Notes to emphasize "Domain Memory First" principle

**Key addition**:
> "The magic is in the memory. The agent is a policy that transforms one consistent memory state into another."

---

### 3. Enhanced: `shared/base_agent.py`

**New features**:
- `state_file` parameter in `__init__()` for persistent state
- `load_state()` - Implements "bootup ritual" (read where we are)
- `save_state()` - Persist state after interactions
- `initialize_state()` - Override to define domain-specific schemas
- `get_state()`, `set_state()`, `update_state()` - State accessors
- `clear_state()` - Reset to initial state

**Usage**:
```python
class MyAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(
            api_key,
            state_file="agents/my-agent/state.json"  # ← Domain memory!
        )

    def initialize_state(self):
        return {"tasks": [], "status": "idle"}

    def chat(self, msg):
        response = super().chat(msg)
        # State automatically persisted!
        return response
```

---

### 4. New Memory Schema Templates

**4 pre-built templates** for non-coding domains:

#### A. Research Agent (`templates/memory_schemas/research_agent_state.json`)
- Hypotheses tracking with confidence levels
- Experiment registry
- Evidence log
- Decision journal

**Use for**: Market research, competitive analysis, scientific investigation

#### B. Operations Agent (`templates/memory_schemas/operations_agent_state.json`)
- Incident tracking with timeline
- SLA monitoring
- System health metrics
- Maintenance windows
- Escalation history

**Use for**: System monitoring, incident response, SRE tasks, runbook automation

#### C. Project Management Agent (`templates/memory_schemas/project_management_agent_state.json`)
- Milestones with status
- Task tracking
- Risk register
- Blocker log
- Status reports
- Decision log

**Use for**: Project tracking, milestone management, risk assessment

#### D. Customer Support Agent (`templates/memory_schemas/customer_support_agent_state.json`)
- Customer context
- Ticket history
- Known issues database
- Escalations
- Satisfaction tracking (NPS)
- Pending follow-ups

**Use for**: Help desk, customer inquiries, ticket management

**Complete guide**: `templates/memory_schemas/README.md` with usage examples

---

## What You Already Had Right ✅

Your Agent Harness **already implements** Anthropic's recommended pattern:

| Anthropic Pattern | Your Implementation |
|-------------------|---------------------|
| Initializer agent | ✅ `harness/prompts/initializer.md` |
| Feature list (pass/fail state) | ✅ `feature_list.json` |
| Progress log | ✅ `claude_progress.md` |
| Git-based state | ✅ Git commits per session |
| Fresh context per session | ✅ Each coding agent is stateless |
| Domain-specific agents | ✅ Orchestrator + specialized agents |

**You were doing it right, you just didn't call it "domain memory."**

---

## Key Insights from Transcript

### 1. Generalized Agents Don't Work

**Problem**: "An amnesiac walking around with a tool belt"

**Why**: LLMs are stateless. Each API call has no memory of previous calls.

**Solution**: Domain memory as the primary interface (not the agent's personality)

---

### 2. Memory is the Scaffolding

**Core principle**:
> "The agent is a policy that transforms one consistent memory state into another.
>
> Memory is the scaffolding. The agent plays its part on that stage."

**Implication**: Focus your effort on designing good memory schemas, not on "smarter" prompts or personalities.

---

### 3. Two-Agent Pattern

**Pattern**:
```
Initializer Agent → Generates domain memory artifacts (feature_list.json, progress.md)
                    ↓
Coding Agent #1   → Reads memory, implements feature, updates memory, commits
                    ↓ (agent forgets everything)
Coding Agent #2   → Reads memory, implements feature, updates memory, commits
                    ↓ (agent forgets everything)
...
```

**Why it works**: Each agent is stateless, but memory persists in files.

---

### 4. Design Principles

From transcript and formalized in `DOMAIN_MEMORY_GUIDE.md`:

1. **Externalize the goal** - Turn vague instructions into machine-readable backlogs
2. **Make progress atomic** - One feature per session, test it, mark pass/fail
3. **Enforce clean state** - Every run ends with tests passing, memory updated, git commit
4. **Standardize bootup ritual** - Read memory → Validate → Choose task → Act → Update → Commit
5. **Keep tests close to memory** - feature_list.json is source of truth for test status

---

### 5. Strategic Moat

**Key insight**: Your competitive advantage isn't in having access to Claude Sonnet 4.5 (everyone can buy that).

**Your moat is**:
- Well-designed domain memory schemas for your business domains
- Harnesses that enforce discipline and consistency
- Testing loops that keep agents honest
- Accumulated knowledge in vector memory

**Example**: FibreFlow's fiber deployment domain memory (BOQs, RFQs, contractor tracking) is unique to your business. Competitors can't replicate that easily.

---

## How to Use This in Your Workflow

### For Harness-Built Agents (Coding)

**No changes needed!** Your harness already implements domain memory correctly:
- `feature_list.json` ← Single source of truth for test status
- `claude_progress.md` ← Session-to-session communication
- Git commits ← Atomic state snapshots

**Continue using**: `/agents/build [agent-name]` for complex agents

---

### For Manually-Built Agents (Non-Coding)

**Now you have templates!** Use the new memory schemas:

#### Example: Building an Operations Agent

```bash
# 1. Create agent directory
mkdir -p agents/fiber-ops

# 2. Copy memory schema template
cp templates/memory_schemas/operations_agent_state.json agents/fiber-ops/state.json

# 3. Customize template
nano agents/fiber-ops/state.json
# Add fiber-specific fields:
# - "fiber_cuts": []
# - "contractor_dispatches": []
# - "repair_timeline": []

# 4. Implement agent with state_file
```

```python
# agents/fiber-ops/agent.py
from shared.base_agent import BaseAgent

class FiberOpsAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(
            api_key,
            model="claude-3-haiku-20240307",
            state_file="agents/fiber-ops/state.json"  # ← Domain memory!
        )

    def initialize_state(self):
        """Load operations template + fiber-specific fields"""
        import json
        with open("templates/memory_schemas/operations_agent_state.json") as f:
            state = json.load(f)

        # Add fiber deployment fields
        state["fiber_cuts"] = []
        state["contractor_dispatches"] = []
        state["repair_timeline"] = []
        return state

    def define_tools(self):
        return [
            {
                "name": "record_fiber_cut",
                "description": "Record a fiber optic cable cut incident",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
                        "affected_customers": {"type": "integer"}
                    },
                    "required": ["location", "severity"]
                }
            }
        ]

    def execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "record_fiber_cut":
            # Read current state
            cuts = self.get_state("fiber_cuts", [])

            # Add incident
            incident_id = f"FC-{len(cuts) + 1:03d}"
            cuts.append({
                "id": incident_id,
                "location": tool_input["location"],
                "severity": tool_input["severity"],
                "affected_customers": tool_input.get("affected_customers", 0),
                "status": "open",
                "created_at": datetime.utcnow().isoformat()
            })

            # Also add to incidents (standard ops format)
            incidents = self.get_state("incidents", [])
            incidents.append({
                "id": incident_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "severity": tool_input["severity"],
                "description": f"Fiber cut at {tool_input['location']}",
                "status": "open",
                "timeline": []
            })

            # Update state
            self.set_state("fiber_cuts", cuts)
            self.set_state("incidents", incidents)
            self.save_state()  # ← Persist to disk!

            return json.dumps({
                "status": "recorded",
                "incident_id": incident_id
            })

        return json.dumps({"error": "Unknown tool"})

    def get_system_prompt(self) -> str:
        return """You are a fiber optic operations assistant.

        You help track and respond to fiber infrastructure incidents:
        - Fiber cuts
        - Network outages
        - Contractor dispatches
        - Repair timelines

        Always record incidents to maintain operational state."""
```

```python
# Test state persistence
# tests/test_fiber_ops.py
def test_fiber_ops_memory(tmp_path):
    state_file = tmp_path / "state.json"

    # Session 1
    agent = FiberOpsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    agent.state_file = str(state_file)
    agent.load_state()

    result = agent.execute_tool("record_fiber_cut", {
        "location": "Main St & 5th Ave",
        "severity": "high",
        "affected_customers": 150
    })

    assert agent.get_state("fiber_cuts")[0]["id"] == "FC-001"

    # Session 2 (agent restart)
    agent2 = FiberOpsAgent(api_key=os.getenv("ANTHROPIC_API_KEY"))
    agent2.state_file = str(state_file)
    agent2.load_state()

    # Memory persists!
    assert len(agent2.get_state("fiber_cuts")) == 1
    assert agent2.get_state("fiber_cuts")[0]["location"] == "Main St & 5th Ave"
```

---

### For Existing Agents Without Memory

**Audit and retrofit**:

```bash
# 1. Find agents without state files
grep -r "class.*Agent.*BaseAgent" agents/ | while read -r line; do
    agent_dir=$(echo "$line" | cut -d: -f1 | xargs dirname)
    if [ ! -f "$agent_dir/state.json" ]; then
        echo "Missing state: $agent_dir"
    fi
done

# 2. Add state_file parameter to each agent's __init__
# 3. Override initialize_state() with appropriate template
# 4. Update execute_tool() to read/write state
# 5. Test that state persists across restarts
```

---

## Next Steps

### Immediate (This Week)

1. **Read the guide**
   ```bash
   cat DOMAIN_MEMORY_GUIDE.md | less
   ```

2. **Audit existing agents** - Which ones need domain memory?
   ```bash
   # VPS Monitor - Already stateless (queries on-demand) ✅
   # Neon Database - Stateless (queries on-demand) ✅
   # Convex Database - Stateless (queries on-demand) ✅
   # Contractor Agent - Could benefit from caching/session state 🤔
   # Project Agent - Could benefit from session tracking 🤔
   ```

3. **Test BaseAgent memory methods**
   ```bash
   # Create simple test agent with state
   ./venv/bin/pytest tests/test_base_agent_memory.py -v
   ```

---

### Short Term (This Month)

4. **Build one non-coding agent with domain memory**
   - Pick a domain: Operations, Research, PM, or Support
   - Use appropriate template from `templates/memory_schemas/`
   - Implement using BaseAgent + state_file
   - Test state persistence across sessions

5. **Document your domain memory schemas**
   - For each agent, document its state schema
   - Add to agent's README.md
   - Update orchestrator/registry.json with "stateful": true/false

6. **Add memory validation tests**
   ```python
   # tests/test_agent_memory_consistency.py
   def test_feature_list_matches_git_history():
       """Ensure feature_list.json status matches actual test results"""
       feature_list = load_json("harness/runs/latest/feature_list.json")
       for feature in feature_list["features"]:
           if feature["passes"]:
               # Verify test actually passes
               assert run_test(feature["validation_steps"]) == True
   ```

---

### Long Term (Next Quarter)

7. **Formalize bootup ritual** across all agents
   - Standard sequence: Orient → Validate → Choose → Act → Update → Commit
   - Add to BaseAgent as optional enforcement
   - Document in agent development guide

8. **Memory schema registry**
   - Centralized catalog of all agent state schemas
   - Similar to orchestrator/registry.json but for memory
   - Enables cross-agent memory compatibility

9. **Memory analytics dashboard**
   - Visualize agent state across all agents
   - Track state growth over time
   - Identify memory bloat or inconsistencies

10. **Cross-agent memory patterns**
    - Design patterns for agents that share state
    - Example: Contractor Agent + Project Agent both need contractor data
    - Avoid duplication, ensure consistency

---

## Testing Your Understanding

**Quick Quiz**:

1. **What makes an agent an "amnesiac"?**
   - ❌ It has a small context window
   - ❌ It uses Haiku instead of Sonnet
   - ✅ **It has no persistent state that survives across sessions**

2. **Where does the "magic" lie in long-running agents?**
   - ❌ The LLM model (Sonnet 4.5 vs Haiku)
   - ❌ The agent's personality/system prompt
   - ✅ **The memory scaffolding (domain state)**

3. **When should you use Superior Agent Brain vs Domain Memory?**
   - Domain Memory: Task state (feature_list.json, progress tracking)
   - Superior Agent Brain: Cross-session learning (semantic search, meta-learning)

4. **What's your competitive moat?**
   - ❌ Access to Claude Sonnet 4.5
   - ❌ Having an orchestrator
   - ✅ **Well-designed domain memory schemas for your business**

---

## Files Created/Updated

### Created
- ✅ `DOMAIN_MEMORY_GUIDE.md` (200+ lines)
- ✅ `templates/memory_schemas/research_agent_state.json`
- ✅ `templates/memory_schemas/operations_agent_state.json`
- ✅ `templates/memory_schemas/project_management_agent_state.json`
- ✅ `templates/memory_schemas/customer_support_agent_state.json`
- ✅ `templates/memory_schemas/README.md` (300+ lines with examples)
- ✅ `DOMAIN_MEMORY_IMPLEMENTATION_SUMMARY.md` (this file)

### Updated
- ✅ `CLAUDE.md` - Memory Systems section rewritten
- ✅ `CLAUDE.md` - Documentation Structure updated
- ✅ `CLAUDE.md` - Special Notes updated
- ✅ `shared/base_agent.py` - Added domain memory methods

---

## Cost/Benefit Analysis

**Time invested**: ~30 minutes to read transcript + integrate insights
**Value gained**:
- ✅ Formalized implicit knowledge (what you were doing right)
- ✅ Filled documentation gaps (the "why" behind your architecture)
- ✅ Enabled non-coding agents (operations, research, PM, support)
- ✅ Created reusable templates (4 domain schemas + guide)
- ✅ Enhanced BaseAgent (state management methods)
- ✅ Strategic clarity (your moat is memory schemas, not model access)

**ROI**: High. You now have a complete framework for building memory-backed agents.

---

## References

- **Anthropic Blog**: [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- **Your Harness**: `harness/README.md` - Already implements these patterns
- **BaseAgent**: `shared/base_agent.py` - Now with memory methods
- **Philosophy**: `DOMAIN_MEMORY_GUIDE.md` - Complete guide

---

## Questions?

If you need clarification on:
- When to use domain memory vs Superior Agent Brain
- How to retrofit existing agents with state
- Designing custom memory schemas for new domains
- Testing memory persistence

Refer to:
1. `DOMAIN_MEMORY_GUIDE.md` - Comprehensive philosophy and patterns
2. `templates/memory_schemas/README.md` - Practical implementation guide
3. `shared/base_agent.py` - Code-level documentation

---

**Remember**:
> "Generalized agents are a fantasy.
> Domain memory is the reality that makes agents work."
