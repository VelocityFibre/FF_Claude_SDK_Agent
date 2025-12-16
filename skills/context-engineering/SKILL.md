---
name: Context Engineering
description: Expert guidance on managing Claude's context window, compaction, memory, and structured documentation for optimal long-term performance
---

# Context Engineering Skill

## When to Use This Skill

Activate this skill when:
- User mentions "context", "compact", "memory", or "session"
- Context window usage exceeds 60%
- Starting a new project or major feature
- Planning long coding sessions
- Experiencing hallucinations or repetition

## Core Capabilities

### 1. Context Monitoring

**Check context regularly** with `/context` command.

**Warning Protocol**:
- **60-70%**: Recommend proactive compaction
- **70-85%**: Warn user before starting new tasks
- **85%+**: Strongly urge compaction before proceeding

**Action**: If context > 70%, inform user of current usage and recommend compaction before major tasks.

### 2. Proactive Compaction

**Don't wait for auto-compact** (triggers at ~92%).

**When to compact**:
- Context exceeds 60%
- Before starting major features
- After completing significant milestones
- Natural breakpoints in work sessions

**Process**:
1. Check current context: `/context`
2. Run manual compact: `/compact`
3. Provide retention instructions (see [compaction-guide.md](compaction-guide.md))
4. Verify new context usage

### 3. Memory Management

Use `#` command to persist critical instructions across sessions.

**What to save in memory**:
- Code style preferences
- Testing requirements
- Workflow conventions
- User-specific preferences
- Project constraints

**Memory types**:
- **Project Memory**: Shared across all sessions in this project
- **Session Memory**: Temporary, cleared after session
- **Global Memory**: Applies to all Claude Code sessions

For detailed workflows, see [memory-workflows.md](memory-workflows.md).

### 4. Structured Documentation

Maintain project state in persistent files outside context window.

**Core files**:
- `claude.md` - Master project instructions (auto-loaded)
- `progress.md` - Task tracking and next steps
- `decisions.md` - Architectural decision log
- `bugs.md` - Bug tracking system

For complete setup, see [structured-notes.md](structured-notes.md).

### 5. Progressive Disclosure

Load context only when needed:
- **Level 1**: Skill metadata (always loaded)
- **Level 2**: SKILL.md body (when triggered)
- **Level 3**: Linked files (on-demand only)

This keeps context lean while maintaining access to deep expertise.

## Quick Actions

### When User Asks About Context
1. Run `/context` to check current usage
2. Report percentage and available space
3. Recommend action based on thresholds above

### When User Requests Compaction
1. Verify current context usage
2. Prepare retention instructions template
3. Execute `/compact` with custom instructions
4. Confirm new context state

### When Starting New Project
1. Create `claude.md` in project root
2. Set up structured note files
3. Save key instructions to memory
4. Establish context monitoring habit

### Before Major Features
1. Check context availability
2. Compact if > 60%
3. Update `progress.md` with new tasks
4. Ensure adequate space for implementation

## Integration with Existing Setup

This skill works with your current files:
- **claude.md**: Automatically loaded each session
- **CONTEXT_ENGINEERING_GUIDE.md**: Reference documentation
- **progress.md, decisions.md, bugs.md**: Structured notes system

## Related Files

- [compaction-guide.md](compaction-guide.md) - Detailed compaction workflows and templates
- [memory-workflows.md](memory-workflows.md) - Memory tool best practices
- [structured-notes.md](structured-notes.md) - Note-taking system setup

## Success Metrics

You'll know context engineering is working when:
- ✅ No unexpected auto-compacts
- ✅ New sessions start with full project understanding
- ✅ Minimal instruction repetition
- ✅ Consistent code patterns
- ✅ Fewer hallucinations
- ✅ Faster, higher-quality task completion

## Notes

- This skill is based on Anthropic's context engineering research
- Uses progressive disclosure to minimize context overhead
- Complements MCP servers for external tool integration
- Reusable across projects with similar workflow needs
