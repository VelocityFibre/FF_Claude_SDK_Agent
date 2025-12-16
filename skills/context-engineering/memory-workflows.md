# Memory Workflows

## Overview

The memory tool provides persistent storage for instructions that should survive across all sessions. Use memory for long-term preferences and compaction for short-term context management.

## Memory Types

### Project Memory
- **Scope**: Current project directory
- **Persistence**: All sessions in this project
- **Use for**: Project-specific rules, conventions, preferences
- **Storage**: `.claude/memory/project.md` or similar

### Session Memory
- **Scope**: Current conversation only
- **Persistence**: Cleared when session ends
- **Use for**: Temporary notes, current task context
- **Storage**: In-memory, not persisted

### Global Memory
- **Scope**: All Claude Code sessions
- **Persistence**: Permanent across all projects
- **Use for**: Universal preferences, coding style
- **Storage**: Global config directory

## Using the # Command

### Basic Syntax
```
# [Your instruction here]
```

When you press enter, Claude will ask which memory to store it in.

### Examples

**Code Style Preference**:
```
# Always use TypeScript for new files, never JavaScript
# Prefer functional components with hooks over class components
# Use named exports instead of default exports
```

**Testing Requirements**:
```
# Write unit tests for all utility functions
# Minimum 80% code coverage for new features
# Run tests before marking tasks complete
```

**Workflow Rules**:
```
# Check context usage before starting new major tasks
# Update progress.md after completing each significant task
# Warn me if context exceeds 70% before proceeding
# Use semantic commit messages following conventional commits spec
```

**Project Constraints**:
```
# Must support Node.js 18+ only
# Cannot use external API calls in this project
# Follow existing file naming convention: kebab-case for files
```

## What to Save in Memory

### ✅ Good Candidates for Memory

**Permanent Preferences**:
- Code style and formatting rules
- Testing approach and coverage goals
- Commit message conventions
- Documentation standards

**Project Context**:
- Tech stack and version requirements
- Architecture decisions that won't change
- Security or compliance requirements
- Performance constraints

**Workflow Instructions**:
- When to run tests
- How to handle errors
- Context management rules
- Update protocols for structured notes

**User-Specific**:
- Communication style preferences
- Verbosity level
- Preferred terminology
- Learning style

### ❌ Poor Candidates for Memory

**Temporary Information**:
- Current bugs (use bugs.md instead)
- Active tasks (use progress.md instead)
- Ongoing decisions (use decisions.md instead)
- Session-specific context

**Frequently Changing**:
- Work in progress
- Experimental approaches
- Debugging steps
- Exploratory code

**Already Documented**:
- Information in claude.md
- Content in structured notes
- README documentation

## Memory vs. Other Storage

| Storage Type | Use Case | Persistence | Scope |
|-------------|----------|-------------|-------|
| **Memory** | Long-term preferences | Permanent | Session/Project/Global |
| **claude.md** | Project documentation | Permanent | Project only |
| **Compaction retention** | Short-term context | Until next compact | Current session |
| **Structured notes** | State tracking | Permanent | Project only |
| **Context window** | Active work | Until compact | Current session |

## Memory Workflows

### Workflow 1: Project Setup
When starting a new project:

```
1. Create claude.md with project overview

2. Save permanent rules to memory:
   # Check context before starting major tasks
   # Update progress.md after completing tasks
   # Follow the established code patterns in this project

3. Document project specifics in claude.md

4. Begin development
```

### Workflow 2: Learning User Preferences
As you learn what the user wants:

```
User: "I prefer less verbose responses"
You: # User prefers concise, direct responses without preamble

User: "Always run tests before committing"
You: # Always run full test suite before marking tasks complete

User: "Use spaces, not tabs"
You: # Code style: Use 2 spaces for indentation, never tabs
```

### Workflow 3: Establishing Conventions
When patterns emerge:

```
After 3rd similar decision:
# Architecture: Use repository pattern for data access
# Testing: Mock external APIs, use real database in tests
# Error handling: Use custom error classes, not strings
```

### Workflow 4: Context Management
Set up automatic context awareness:

```
# Before starting any new task, check context usage with /context
# If context > 70%, warn user and recommend compaction
# If context > 85%, strongly recommend compacting before proceeding
```

## Best Practices

### 1. Be Specific
❌ Bad:
```
# Write good code
# Test everything
```

✅ Good:
```
# Use TypeScript strict mode for all new files
# Write unit tests for utilities, integration tests for API endpoints
```

### 2. Separate Concerns
- **Memory**: Permanent preferences
- **claude.md**: Project documentation
- **progress.md**: Current state
- **decisions.md**: Why choices were made

### 3. Review and Update
Periodically review memory:
```
# Show me what's in project memory
```

Remove outdated items:
```
# Remove the rule about using JavaScript (now using TypeScript)
```

### 4. Layer Your Storage
```
Global Memory:
└─ Universal coding preferences

Project Memory:
└─ Project-specific rules

claude.md:
└─ Project overview and guidelines

Structured Notes:
└─ Current state and progress
```

### 5. Don't Duplicate
If it's in `claude.md`, don't put it in memory too. Use memory for:
- Cross-project preferences
- User-specific instructions
- Workflow automation rules

## Common Memory Patterns

### Pattern 1: Context Awareness
```
# Check context with /context before starting new features
# Warn if context > 70%
# Recommend compaction if context > 60% and new feature is complex
```

### Pattern 2: Quality Gates
```
# Run tests before marking tasks complete
# Check for TypeScript errors before committing
# Verify no console.logs in production code
```

### Pattern 3: Documentation Updates
```
# Update progress.md after each completed task
# Document architectural decisions in decisions.md
# Log bugs in bugs.md when discovered
```

### Pattern 4: Communication Style
```
# User prefers concise responses
# Avoid preamble like "Let me help you with that"
# Include file:line references when discussing code
```

## Examples

### Example 1: Full Project Setup

**Global Memory**:
```
# Use TypeScript for all projects
# Prefer functional programming patterns
# Write clear, descriptive commit messages
```

**Project Memory**:
```
# This is a React 18 project using Vite
# Use TanStack Query for data fetching
# Minimum 80% test coverage required
# Check context before major tasks
# Update progress.md after completing tasks
```

**claude.md**:
```markdown
# My App

## Overview
Task management application...

## Tech Stack
- React 18, TypeScript, Vite
- TanStack Query, React Router

## Development Guidelines
[Specific to this project...]
```

### Example 2: Learning Preferences Over Time

**Session 1**:
```
User: "I like when you explain your reasoning"
You: # User appreciates explanations of decisions and reasoning
```

**Session 3**:
```
User: "Can you be more concise?"
You: # [Updates memory] User prefers concise responses with reasoning but no preamble
```

**Session 5**:
```
User: "Perfect, that's the right level of detail"
You: # [Confirms] User likes: brief answer + reasoning, no preamble/conclusion
```

### Example 3: Workflow Automation

**Initial Setup**:
```
# Check context usage before starting new major tasks
# Update progress.md after completing tasks
# Compact proactively at 60% context usage
```

**After First Compact**:
```
# [Adds] When compacting, retain: architectural decisions, active bugs, user preferences, current implementation approach
```

**After User Feedback**:
```
# [Adds] After compaction, verify context dropped to < 40%
```

## Troubleshooting

### "Memory instructions aren't being followed"
- Check that you saved to the right memory type (project vs global)
- Verify the instruction is still in memory
- Make sure instruction is specific and actionable
- Consider if it conflicts with claude.md or system prompt

### "I want to change a memory instruction"
```
# Update the instruction about [topic] to [new instruction]
```

Or remove and re-add:
```
# Remove instruction about [topic]
# [New instruction here]
```

### "How do I see what's in memory?"
```
# Show me what's currently saved in project memory
```

### "Should this be in memory or claude.md?"
Ask:
- Is it project-specific documentation? → claude.md
- Is it a permanent preference/rule? → memory
- Is it current state? → structured notes (progress.md, etc.)
- Is it active work? → context window

## Advanced Techniques

### Conditional Instructions
```
# When working on frontend: use React best practices
# When working on backend: prioritize security over convenience
# When writing tests: prefer integration tests for APIs, unit tests for utilities
```

### Contextual Workflows
```
# If context > 70% and task is complex: warn user and recommend compacting first
# If context > 85%: strongly urge compaction before proceeding
# If starting major feature: ensure context < 60%
```

### Progressive Enhancement
Start simple:
```
# Update progress.md after tasks
```

Add detail as needed:
```
# Update progress.md after completing each significant task
# Mark tasks as completed immediately, don't batch
# Add new tasks discovered during work
```

### Memory Templates

**For New Project**:
```
# Check context before starting major features
# Update progress.md after completing tasks
# Document decisions in decisions.md
# Log bugs in bugs.md when discovered
# Use [tech stack] for this project
# Minimum [X]% test coverage
```

**For Code Quality**:
```
# Run linter before marking complete
# Run tests before committing
# No console.logs in production
# Use TypeScript strict mode
# Prefer composition over inheritance
```

**For User Preferences**:
```
# User prefers [communication style]
# Explain [when to explain]
# Ask before [what needs confirmation]
# Use [terminology preferences]
```

## Integration with Skills

Skills can reference memory:

**In SKILL.md**:
```markdown
## Before Using This Skill

Check project memory for:
- Testing requirements
- Code style preferences
- Deployment constraints

Adjust skill behavior accordingly.
```

This allows skills to adapt to user preferences automatically.

## Summary

Memory is your long-term persistent storage for:
- ✅ Permanent preferences and rules
- ✅ Cross-session instructions
- ✅ User-specific customization
- ✅ Workflow automation

Use in combination with:
- **claude.md**: Project documentation
- **Structured notes**: Current state
- **Compaction**: Short-term context
- **Skills**: Reusable capabilities

The result: Claude that remembers what matters, adapts to your preferences, and maintains consistency across all sessions.
