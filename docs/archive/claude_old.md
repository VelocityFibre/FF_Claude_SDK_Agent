# Claude Agent Project

## Project Overview
This is an AI agent development environment focused on implementing advanced context engineering techniques to maximize Claude Code's performance and reliability across long coding sessions.

## Purpose
To create a robust development workflow using Claude Code with:
- Effective context management
- Persistent memory systems
- Structured documentation
- Long-term project continuity

## Tech Stack
- **Runtime**: Node.js / Python (as needed)
- **AI Framework**: Claude Code (Sonnet 4.5)
- **Documentation**: Markdown
- **Version Control**: Git

## Architecture Principles

### Context Engineering
This project implements the five key context engineering principles:

1. **Compaction**: Proactive context window management
2. **Memory Tool**: Persistent instruction storage
3. **Structured Documentation**: claude.md as single source of truth
4. **Note-Taking**: progress.md, decisions.md, bugs.md for state tracking
5. **Sub-Agents**: (Optional) Specialized agents for complex tasks

### Agent Skills
This project uses **Agent Skills** to package reusable expertise:

- **Skills Directory**: `skills/` contains organized capabilities
- **Progressive Disclosure**: Skills loaded only when needed (3 levels: metadata → SKILL.md → linked files)
- **Context-Engineering Skill**: Pre-built skill for context management
- **Source-Validation Skill**: First principles validation of new information
- **Auto-Discovery**: Claude loads skill metadata at startup, full content on demand

### File Organization
```
/
├── claude.md                          # This file - project instructions
├── progress.md                        # Task tracking and next steps
├── decisions.md                       # Architectural decisions log
├── bugs.md                           # Bug tracking and resolutions
├── CONTEXT_ENGINEERING_GUIDE.md      # Implementation guide
├── AGENT_SKILLS_GUIDE.md             # Agent Skills implementation guide
├── skills/                           # Agent Skills directory
│   ├── context-engineering/          # Context engineering skill
│   │   ├── SKILL.md                  # Core skill (auto-discovered)
│   │   ├── compaction-guide.md       # Detailed compaction workflows
│   │   ├── memory-workflows.md       # Memory tool best practices
│   │   └── structured-notes.md       # Note-taking system
│   └── source-validation/            # Source validation skill
│       ├── SKILL.md                  # Core validation framework
│       ├── source-hierarchy.md       # Tier 1-4 source definitions
│       ├── validation-checklist.md   # 5-question validation process
│       ├── decision-matrix.md        # Adopt/adapt/investigate/reject/archive
│       └── bias-detection.md         # Cognitive bias identification
└── [project files]
```

## Development Guidelines

### Context Management Rules
- **Check context before major tasks**: Use `/context` command
- **Compact at 60-70%**: Don't wait for auto-compact at 92%
- **Monitor actively**: Regular context checks during long sessions
- **Preserve key information**: Always specify retention instructions when compacting

### Structured Note-Taking
**Claude must update these files automatically**:
- `progress.md`: After completing each significant task
- `decisions.md`: When making architectural or design decisions
- `bugs.md`: When discovering or resolving bugs

### Memory Usage
Store in project memory:
- Code style preferences
- Testing requirements
- Workflow conventions
- User-specific preferences
- Project constraints

### Code Quality Standards
- Write clear, maintainable code
- Follow established patterns in the codebase
- Document complex logic
- Test critical functionality
- Use meaningful variable and function names

### Commit Conventions
- Use semantic commit messages
- Reference issue numbers when applicable
- Keep commits atomic and focused
- Don't commit files with secrets

### Testing Requirements
- Write tests for new features when applicable
- Verify changes before marking tasks complete
- Document test coverage in progress.md

## Current Project State

### Active Development
- Setting up context engineering infrastructure
- Implementing structured documentation system
- Establishing best practices workflow

### Completed Setup
- ✅ CONTEXT_ENGINEERING_GUIDE.md created
- ✅ AGENT_SKILLS_GUIDE.md created
- ✅ claude.md established
- ✅ Project structure defined
- ✅ Created progress.md, decisions.md, bugs.md files
- ✅ Built Context Engineering skill (skills/context-engineering/)
- ✅ Built Source of Truth Validation skill (skills/source-validation/)

### Next Steps
- Use Source of Truth Validation skill to evaluate new information
- Add key instructions to project memory using `#` command
- Establish compaction schedule
- Build additional skills as needed
- Begin main project development

## Instructions for Claude

### Every Session Start
1. Read this claude.md file (automatic)
2. Check `/context` for available space
3. Review `progress.md` for current state
4. Understand recent decisions from `decisions.md`
5. Check `bugs.md` for known issues

### During Development
1. Update `progress.md` after completing tasks
2. Document architectural decisions in `decisions.md`
3. Log bugs/issues in `bugs.md` when discovered
4. Monitor context usage regularly
5. Reference past decisions before making new ones

### Before Major Changes
1. Check context usage with `/context`
2. Compact if above 60% with retention instructions
3. Update this claude.md if project direction changes
4. Review relevant decisions from `decisions.md`

### Context Warning Protocol
Before starting any new task:
- If context > 70%: Warn user and suggest compaction
- If context > 85%: Strongly recommend compaction before proceeding
- If task is complex: Ensure adequate context space (recommend < 60%)

### Compaction Instructions Template
When compacting, retain:
- All architectural decisions from recent work
- Current bugs and their workarounds
- User preferences for code style and workflow
- Current implementation approach for active features
- Project constraints and requirements

### Communication Style
- Be concise and direct
- Avoid unnecessary preamble
- Focus on completing tasks
- Ask clarifying questions when needed
- Provide context references (file:line) when relevant

## Project-Specific Preferences

### Coding Style
- Use clear, descriptive names
- Prefer readability over cleverness
- Comment complex logic
- Follow DRY principles
- Keep functions focused and small

### Documentation
- Update docs alongside code changes
- Use markdown for all documentation
- Keep README current
- Document breaking changes

### Workflow
- Check context regularly
- Update structured notes automatically
- Compact proactively
- Test before completion
- Commit with semantic messages

## Knowledge Base

### Context Engineering Resources
- Anthropic's Context Engineering Paper
- Anthropic's Agent Skills Documentation
- Claude Code Documentation
- CONTEXT_ENGINEERING_GUIDE.md in this project
- AGENT_SKILLS_GUIDE.md in this project

### Key Concepts
- **200K Context Window**: Sonnet 4.5 feature with intelligent context management
- **Context Editing**: Automatic trimming of old tool calls (built-in to Sonnet 4.5)
- **File-Based Memory**: Uses file names/paths as just-in-time references
- **Structured Notes**: External persistence outside context window
- **Agent Skills**: Organized folders with SKILL.md for domain expertise
- **Progressive Disclosure**: Load context in 3 levels (metadata → SKILL.md → linked files)
- **Sub-Agents**: Isolated contexts for specialized tasks

## Success Metrics

The context engineering implementation is successful when:
- ✅ No unexpected auto-compacts
- ✅ New sessions start with full project context
- ✅ Minimal instruction repetition across sessions
- ✅ Consistent code patterns and decisions
- ✅ Few hallucinations or context loss
- ✅ Fast, high-quality task completion
- ✅ Structured notes are maintained automatically

## Maintenance Schedule

### Regular Maintenance
- **Every session**: Update progress.md, check context
- **After features**: Update decisions.md, compact if needed
- **Weekly**: Review and update claude.md
- **Monthly**: Archive old entries, clean up notes

### File Maintenance
- Archive completed tasks from progress.md
- Keep decisions.md chronological and relevant
- Move resolved bugs to "Resolved" section in bugs.md
- Update claude.md when project evolves

## Notes

This project serves as both:
1. A practical implementation of context engineering techniques
2. A template for future projects using Claude Code

The structured approach ensures that Claude maintains project understanding across sessions, reduces hallucinations, and delivers consistent high-quality results.
