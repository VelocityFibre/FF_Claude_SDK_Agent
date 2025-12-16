# Compaction Guide

## Overview

Manual compaction gives you control over what Claude remembers vs. discards, preventing unexpected auto-compacts and improving continuity.

## When to Compact

### Thresholds
- **60-70%**: Recommended - proactive compaction
- **70-85%**: Warning zone - compact before new features
- **85%+**: Critical - compact immediately before proceeding

### Situations
- Before starting major new features
- After completing significant milestones
- Natural breakpoints between work sessions
- When context feels "cluttered" with old tool outputs
- After extensive debugging or exploration

## Compaction Process

### Step 1: Check Current Context
```bash
/context
```

Review the output:
- System prompt and tools (fixed overhead)
- Messages (your conversation)
- Reserved space (for output)
- Free space (available for work)

### Step 2: Prepare Retention Instructions

Use this template and customize:

```
Retain:
- All architectural decisions from the past 3 tasks
- Current bugs and their workarounds
- User preferences for [specific preference]
- The current implementation approach for [active feature]
- Testing requirements and conventions
- File structure and naming conventions
- Dependencies and version requirements

Discard:
- Completed tasks from progress.md
- Failed experimental code that wasn't used
- Debugging output and error traces
- Tool outputs from >5 messages ago
- Resolved issues and old discussions
```

### Step 3: Run Compaction
```bash
/compact
```

When prompted, paste your retention instructions.

### Step 4: Verify Results
```bash
/context
```

Check that:
- Context usage dropped significantly (ideally to 30-40%)
- Free space increased
- You have room for new work

## Retention Instruction Templates

### For Active Development
```
Retain:
- Current implementation of [feature name]
- Architectural decisions about [specific choices]
- User requirements for [feature]
- Code patterns established (e.g., React hooks, async/await)
- Testing approach and coverage goals
- Outstanding tasks from progress.md

Discard:
- Completed and verified tasks
- Old debugging sessions
- Superseded code attempts
```

### For Debugging Session
```
Retain:
- Root cause analysis of [bug]
- Successful debugging steps
- Workarounds currently in place
- Patterns that led to the bug
- Prevention strategies

Discard:
- Failed debugging attempts
- Error logs and stack traces
- Code that didn't work
```

### For Refactoring
```
Retain:
- Refactoring goals and rationale
- New architectural patterns
- Migration plan and progress
- Breaking changes and their impacts
- Updated file structure

Discard:
- Old code that's been replaced
- Initial exploratory approaches
- Superseded design decisions
```

### For Project Setup
```
Retain:
- Tech stack decisions and rationale
- Project structure choices
- Development workflow
- Testing and CI/CD setup
- Environment configuration

Discard:
- Installation output
- Setup experimentation
- Alternative approaches considered but rejected
```

## Best Practices

### 1. Compact Proactively
Don't wait for auto-compact. Manual compaction at 60-70% gives you control.

### 2. Be Specific in Retention
Instead of "remember everything", specify:
- Exact decisions to keep
- Specific bugs/workarounds
- Particular user preferences

### 3. Review Before Compacting
Quickly scan recent conversation for important items you want retained.

### 4. Update Structured Notes First
Before compacting:
- Update `progress.md` with completed tasks
- Document decisions in `decisions.md`
- Log bugs in `bugs.md`

This ensures information persists outside the context window.

### 5. Compact at Natural Breakpoints
Good times to compact:
- End of work session
- After completing a feature
- Before switching to different area of codebase
- After resolving major bugs

### 6. Use Memory for Long-term Persistence
For truly permanent instructions, use `#` command to save to memory instead of relying on compaction retention.

## Context Usage Patterns

### Healthy Pattern
```
Session 1: Start 15% → Work to 65% → Compact to 35%
Session 2: Start 35% → Work to 70% → Compact to 40%
Session 3: Start 40% → Work to 68% → Compact to 35%
```

### Unhealthy Pattern
```
Session 1: Start 15% → Work to 92% → Auto-compact (lose control)
Session 2: Start 50% → Work to 92% → Auto-compact (lose control)
Session 3: Start 60% → Work to 92% → Auto-compact (lose control)
```

## Troubleshooting

### "I compacted but context is still high"
- System prompt and tools are fixed overhead (~15-20%)
- Reserved space is constant (~22%)
- Check if large files are loaded in messages
- Consider if MCP servers are adding context

### "Claude forgot important information after compact"
- Review your retention instructions
- Be more specific about what to retain
- Use memory (`#` command) for permanent storage
- Update structured notes before compacting

### "Auto-compact happened unexpectedly"
- You waited too long (>92% triggers auto)
- Compact proactively at 60-70% instead
- Monitor context more regularly

### "How do I know what to retain?"
- Review recent messages for key decisions
- Check `progress.md` for active work
- Identify current bugs/blockers
- Note user preferences mentioned
- Think about what you'll need for next tasks

## Examples

### Example 1: After Building Feature
**Context before**: 72%

**Retention instructions**:
```
Retain:
- The authentication flow architecture we just implemented
- User's preference for JWT over sessions
- Testing requirements (80% coverage minimum)
- Known issue with refresh token timing
- Next task: implement password reset

Discard:
- Installation and setup output
- Failed attempts at OAuth integration
- Debugging logs from token validation
- Completed tasks from progress.md
```

**Context after**: 38%

### Example 2: Before Major Refactoring
**Context before**: 68%

**Retention instructions**:
```
Retain:
- Current file structure and component hierarchy
- Rationale for moving to TypeScript
- Migration checklist from progress.md
- User's requirement to maintain backward compatibility
- Testing strategy for refactored code

Discard:
- Old JavaScript code being replaced
- Exploratory TypeScript attempts
- Resolved linting errors
```

**Context after**: 35%

### Example 3: After Debugging Session
**Context before**: 78%

**Retention instructions**:
```
Retain:
- Root cause: race condition in useEffect
- Solution: added cleanup function and dependency array
- User's coding standard: always cleanup side effects
- Pattern to avoid this bug in future

Discard:
- All console.log debugging attempts
- Error stack traces
- Failed solutions tried
- Old code before fix
```

**Context after**: 42%

## Integration with Workflow

### Daily Workflow
```
Morning:
1. Start session (context ~35%)
2. Check /context
3. Review progress.md

During work:
4. Monitor context periodically
5. Update structured notes as you go

Evening:
6. Update progress.md with completed tasks
7. Check /context
8. Compact if > 60%
9. End session with clean context
```

### Per-Feature Workflow
```
Start feature:
1. Ensure context < 60%
2. Define feature in progress.md

During development:
3. Document decisions in decisions.md
4. Log bugs in bugs.md
5. Monitor context

Complete feature:
6. Update progress.md (mark complete)
7. Document final decisions
8. Compact with retention of what's next
```

## Advanced Techniques

### Selective Retention by Time
```
Retain:
- Everything from the last 2 hours of conversation
- Critical decisions from earlier today
- User preferences from any time

Discard:
- Tool outputs from >4 hours ago
- Resolved issues from yesterday
```

### Retention by Relevance
```
Retain:
- Anything related to current feature [X]
- Architectural patterns we're using
- Constraints and requirements

Discard:
- Work on feature [Y] (now complete)
- Exploration of alternative approaches
```

### Multi-Domain Projects
```
Retain:
- Frontend work (current focus)
- API contract between frontend/backend
- User authentication flow (touches both)

Discard:
- Backend implementation details (not current focus)
- Database migration output
```

## Remember

The goal of compaction is to:
- Keep context lean and focused
- Maintain important information
- Prevent hallucinations from context overload
- Give you control over what Claude remembers

Combined with structured notes (`claude.md`, `progress.md`, etc.) and memory (`#` command), compaction is a powerful tool for long-term project success.
