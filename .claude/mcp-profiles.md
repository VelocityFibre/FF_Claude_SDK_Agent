# MCP Configuration Profiles

Instead of loading all MCPs at once, switch between focused profiles based on task type.

## Profile 1: Database Work
**Use when**: Working with Neon/Convex databases
```json
{
  "mcpServers": {
    "context7": { "enabled": true },
    "postgres-mcp": { "enabled": true },
    "github": { "enabled": false },
    "playwright-mcp": { "enabled": false }
  }
}
```

## Profile 2: Deployment & Testing
**Use when**: Running tests, deploying agents, checking VPS
```json
{
  "mcpServers": {
    "context7": { "enabled": true },
    "playwright-mcp": { "enabled": true },
    "github": { "enabled": true },
    "postgres-mcp": { "enabled": false }
  }
}
```

## Profile 3: Development
**Use when**: Writing code, refactoring, documentation
```json
{
  "mcpServers": {
    "context7": { "enabled": true },
    "github": { "enabled": true },
    "postgres-mcp": { "enabled": false },
    "playwright-mcp": { "enabled": false }
  }
}
```

## How to Switch Profiles

Manually edit `.claude/settings.local.json` or use Claude Code commands:
- "Enable postgres-mcp server"
- "Disable playwright-mcp server"

## Why This Works

- **Reduced Context**: Only 1-2 MCPs active at once
- **Faster Startup**: Fewer tools to load
- **Focused Tools**: Only tools relevant to current task
- **No Docker Desktop Required**: Works with any setup
