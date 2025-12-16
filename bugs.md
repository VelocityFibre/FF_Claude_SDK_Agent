# Known Bugs and Issues

This file tracks bugs, issues, and their resolutions. Move items to "Resolved" section when fixed.

---

## Active Bugs

*No active bugs currently*

---

## Resolved Bugs

*No resolved bugs yet*

---

## Bug Entry Template

When logging a bug, use this format:

### Bug #N: [Brief Description]
- **Severity**: Critical / High / Medium / Low
- **Discovered**: YYYY-MM-DD
- **Reproduction Steps**:
  1. Step one
  2. Step two
  3. Expected vs actual behavior
- **Workaround**: [Temporary solution if available]
- **Status**: Investigating / In Progress / Blocked / Resolved
- **Assignee**: [Who's working on it]
- **Related Files**: [Affected files with line numbers]
- **Error Messages**:
  ```
  [Paste relevant error messages]
  ```

---

## Resolution Template

When resolving, move to "Resolved Bugs" section with this format:

### Bug #N: [Brief Description]
- **Resolution**: [How it was fixed]
- **Root Cause**: [Why it happened]
- **Resolved**: YYYY-MM-DD
- **Commit**: [Commit hash if applicable]
- **Changes Made**:
  - File1.ts:123 - [Change description]
  - File2.ts:456 - [Change description]
- **Testing**: [How the fix was verified]
- **Prevention**: [Steps to prevent similar bugs]

---

## Notes

### Bug Severity Guidelines
- **Critical**: System down, data loss, security vulnerability
- **High**: Major feature broken, affects many users, no workaround
- **Medium**: Feature impaired, workaround exists, affects some users
- **Low**: Minor issue, cosmetic, affects few users

### Best Practices
- Log bugs as soon as discovered
- Include reproduction steps
- Reference file locations (file:line format)
- Document workarounds immediately
- Update status as investigation progresses
- Move to resolved section (don't delete)
- Link related bugs if applicable

### When to Create a Bug Entry
- Unexpected behavior or errors
- Performance issues
- UI/UX problems
- Integration failures
- Data inconsistencies
- Security concerns

### Integration with Development
- Check this file before starting work
- Reference bug numbers in commits
- Update status during development
- Test fixes thoroughly before resolving
- Document in decisions.md if architecture changed
