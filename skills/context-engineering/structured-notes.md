# Structured Notes System

## Overview

Structured note-taking keeps project state persistent outside the context window, enabling continuity across sessions and reducing context overhead.

## Core Files

### claude.md - Master Instructions
**Purpose**: Single source of truth for project

**Location**: Project root

**Auto-loaded**: Yes (every session start)

**Contents**:
- Project overview and purpose
- Tech stack and architecture
- Development guidelines
- Code style and conventions
- Testing requirements
- Instructions for Claude

**Example Structure**:
```markdown
---
# Project Name

## Overview
[What this project does]

## Tech Stack
- Frontend: [...]
- Backend: [...]
- Database: [...]

## Architecture
[Key decisions]

## Development Guidelines
### Code Style
[Standards]

### Testing
[Requirements]

### Naming Conventions
[Rules]

## Instructions for Claude
[How Claude should work on this project]
---
```

### progress.md - Task Tracking
**Purpose**: Track what's done, in progress, and next

**Update frequency**: After each significant task

**Contents**:
- Completed tasks (with dates)
- Current work in progress
- Next steps (organized by timeline)
- Session notes

**Example Structure**:
```markdown
# Project Progress

## Completed Tasks
### 2025-10-21: Feature X
- [x] Implemented authentication
- [x] Added user dashboard
- [x] Wrote tests (85% coverage)

## In Progress
- [ ] Payment integration (70% complete)

## Next Steps
### Immediate
- [ ] Complete payment integration
- [ ] Test error scenarios

### Short-term
- [ ] Email notifications
- [ ] Admin panel

### Long-term
- [ ] Mobile app
- [ ] API v2

## Notes
[Current context, blockers, etc.]
```

### decisions.md - Architectural Log
**Purpose**: Record why decisions were made

**Update frequency**: When making significant decisions

**Contents**:
- Decision description
- Rationale
- Impact on project
- Alternatives considered
- Date and context

**Example Structure**:
```markdown
# Architectural Decisions

## 2025-10-21: Chose PostgreSQL over MongoDB

**Decision**: Use PostgreSQL for data storage

**Rationale**:
- Need complex relational queries
- ACID compliance required
- Team expertise with SQL

**Impact**:
- Better data integrity
- Required migration scripts
- Slightly more complex schema changes

**Alternatives Considered**:
- MongoDB: Too limited for our query needs
- MySQL: Less advanced features than PostgreSQL

---

## [Next decision...]
```

### bugs.md - Issue Tracking
**Purpose**: Log bugs, workarounds, and resolutions

**Update frequency**: When bugs discovered or resolved

**Contents**:
- Active bugs with severity
- Reproduction steps
- Workarounds
- Resolved bugs archive

**Example Structure**:
```markdown
# Known Bugs and Issues

## Active Bugs

### Bug #1: Login timeout on slow connections
- **Severity**: Medium
- **Discovered**: 2025-10-21
- **Reproduction**:
  1. Throttle to 3G
  2. Attempt login
  3. Times out after 5s
- **Workaround**: Increased timeout to 10s temporarily
- **Status**: Investigating root cause

## Resolved Bugs

### Bug #5: Memory leak in WebSocket
- **Resolution**: Added cleanup in useEffect
- **Root Cause**: Missing return function
- **Resolved**: 2025-10-18
- **Commit**: abc123f
```

## File Naming and Organization

### Standard Structure
```
project-root/
├── claude.md              # Master instructions (required)
├── progress.md            # Task tracking
├── decisions.md           # Decision log
├── bugs.md               # Bug tracking
├── skills/               # Agent Skills
│   └── context-engineering/
│       └── SKILL.md
└── [your project files]
```

### Alternative Organization
```
project-root/
├── .claude/
│   ├── claude.md
│   ├── progress.md
│   ├── decisions.md
│   ├── bugs.md
│   └── skills/
└── [your project files]
```

Both work - choose based on preference.

## Auto-Update Workflow

### Claude's Responsibilities

**After completing a task**:
1. Update `progress.md`:
   - Move task from "In Progress" to "Completed"
   - Add completion date
   - Note any blockers or learnings

**When making architectural decision**:
1. Update `decisions.md`:
   - Add new entry with date
   - Document rationale and impact
   - Note alternatives considered

**When discovering/fixing bug**:
1. Update `bugs.md`:
   - Add new bug to "Active Bugs" or
   - Move resolved bug to "Resolved Bugs"
   - Include all relevant details

### User's Responsibilities

**Review periodically**:
- Check `progress.md` for accuracy
- Verify `decisions.md` captures rationale
- Confirm `bugs.md` is up to date

**Update `claude.md` when**:
- Project direction changes
- New conventions established
- Tech stack evolves
- Instructions need clarification

## Integration with Memory

### Division of Labor

**claude.md**: Project documentation
```markdown
## Tech Stack
- React 18
- TypeScript
- Vite

## Code Style
- Use functional components
- Prefer named exports
```

**Memory**: Persistent instructions
```
# Update progress.md after completing tasks
# Document decisions in decisions.md
# Check context before major features
```

**Structured Notes**: Current state
```markdown
## In Progress
- [ ] Implementing authentication
```

**Context Window**: Active work
```
[Current conversation and tool outputs]
```

## Progressive Disclosure in Structured Notes

### Reference by Name

Claude can reference files without loading them:
```
"According to decisions.md, we chose PostgreSQL for..."
```

### Load on Demand

Only read files when details needed:
```
"Let me check decisions.md for the database choice..."
[Reads file]
"We chose PostgreSQL because..."
```

### Keep Notes Concise

Each file should be skimmable:
- Use clear headers
- Bullet points over paragraphs
- Dates for chronology
- Brief summaries

## Best Practices

### 1. Update Immediately
Don't batch updates. Update notes right after:
- Completing a task
- Making a decision
- Discovering/fixing a bug

### 2. Be Consistent
Use the same format for all entries:
- Dates in YYYY-MM-DD format
- Severity levels defined
- Headings consistent

### 3. Keep Current
- Archive old completed tasks
- Mark resolved bugs separately
- Remove outdated decisions

### 4. Cross-Reference
Link between files when relevant:
```markdown
# In decisions.md
See Bug #3 in bugs.md for context on why we made this decision.

# In progress.md
This task addresses the decision in decisions.md from 2025-10-15.
```

### 5. Use Templates
Maintain consistent structure with templates (included in each file).

## Maintenance Schedule

### Daily
- Update `progress.md` after tasks
- Check for new bugs to log

### Weekly
- Review `progress.md` and archive old tasks
- Ensure `decisions.md` is current
- Move resolved bugs to archive in `bugs.md`

### Monthly
- Review and update `claude.md`
- Clean up old entries
- Verify all cross-references

### Quarterly
- Major review of all files
- Archive historical data
- Update templates if needed

## Advanced Patterns

### Hierarchical Progress Tracking
```markdown
# progress.md

## Epic: User Authentication

### Completed
- [x] Basic login/logout (2025-10-15)
- [x] JWT implementation (2025-10-16)

### In Progress
- [ ] OAuth integration (60% complete)

### Next
- [ ] Two-factor authentication
- [ ] Password reset flow
```

### Decision Dependencies
```markdown
# decisions.md

## 2025-10-21: Microservices Architecture

**Dependencies**:
- Builds on "Chose Kubernetes" (2025-10-10)
- Requires "API Gateway Pattern" (2025-10-15)
- Supersedes "Monolith Architecture" (2025-09-01)
```

### Bug Patterns
```markdown
# bugs.md

## Patterns Observed

### Pattern: Race Conditions in useEffect
- Occurred in: Bug #3, Bug #7, Bug #12
- Root cause: Missing cleanup functions
- Prevention: Always return cleanup from useEffect
- Related decision: decisions.md 2025-10-20
```

### Progress Metrics
```markdown
# progress.md

## Velocity Tracking

### This Week
- Completed: 12 tasks
- In Progress: 3 tasks
- Avg completion time: 2.5 hours

### Blockers
- Waiting on API access (3 days)
- Design review pending (2 days)
```

## Troubleshooting

### "Claude isn't updating the files"
- Remind Claude of the auto-update protocol
- Add to memory: `# Update progress.md after completing tasks`
- Reference this in `claude.md`

### "Files are getting too large"
- Archive old entries to separate files
- Keep main file for recent items only
- Example: `progress-2025-Q3.md` for archive

### "Inconsistent formatting"
- Create templates in each file
- Reference templates in `claude.md`
- Review periodically and fix inconsistencies

### "Information in multiple places"
- Define clear boundaries:
  - `claude.md`: What and how
  - `progress.md`: Current state
  - `decisions.md`: Why
  - `bugs.md`: Issues
- Avoid duplication
- Cross-reference instead

## Examples

### Example 1: Complete Workflow

**Task**: Implement user authentication

**Before starting**:
```markdown
# progress.md
## In Progress
- [ ] Implement user authentication
```

**During work**:
```markdown
# decisions.md
## 2025-10-21: Chose JWT over Sessions
[Decision details...]
```

```markdown
# bugs.md
## Active Bugs
### Bug #1: Token expiration too short
[Bug details...]
```

**After completion**:
```markdown
# progress.md
## Completed Tasks
### 2025-10-21: Authentication
- [x] Implement user authentication
  - JWT token generation
  - Login/logout endpoints
  - Protected route middleware
  - Tests (90% coverage)
```

```markdown
# bugs.md
## Resolved Bugs
### Bug #1: Token expiration too short
- **Resolution**: Changed from 1h to 24h with refresh tokens
```

### Example 2: Long-term Project

**Month 1** (claude.md):
```markdown
## Tech Stack
- React 18
- Express
- PostgreSQL
```

**Month 3** (decisions.md):
```markdown
## 2025-12-15: Migrating to GraphQL
**Decision**: Replacing REST with GraphQL
**Rationale**: Reduce over-fetching...
```

**Month 3** (claude.md updated):
```markdown
## Tech Stack
- React 18
- Express with Apollo Server
- PostgreSQL
- GraphQL
```

**Month 6** (progress.md):
```markdown
## Completed Tasks
### Q1 2026
- [x] Full REST to GraphQL migration
- [x] Updated all frontend queries
- [x] Deprecated REST endpoints
```

## Summary

Structured notes provide:
- ✅ Persistence outside context window
- ✅ Continuity across sessions
- ✅ Progressive disclosure (load on demand)
- ✅ Historical record
- ✅ Reduced context overhead

Core files:
- **claude.md**: What/how (project instructions)
- **progress.md**: Where (current state)
- **decisions.md**: Why (rationale)
- **bugs.md**: Issues (problems and solutions)

Combined with memory and compaction, structured notes create a complete context engineering system that keeps Claude consistent, informed, and effective across any length of project.
