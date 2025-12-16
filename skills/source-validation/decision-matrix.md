# Decision Matrix

## Overview

This matrix helps you make systematic decisions about new information after completing validation. Each decision (ADOPT/ADAPT/INVESTIGATE/REJECT/ARCHIVE) has clear criteria and action steps.

---

## The 5 Decisions

### ✅ ADOPT - Implement as-is

**When to Use**:
- All 5 validation questions pass strongly
- Source is Tier 1 or validated Tier 2
- Strong evidence backing
- Aligns fully with sources of truth
- Solves real problem with clear benefit
- Current and applicable
- Low risk, high reward

**Criteria Matrix**:
```
Authority:     Tier 1-2, High credibility
Evidence:      Strong, reproducible
Consistency:   Fully aligns with Tier 1 & 2
Practical:     High value, reasonable cost
Recency:       Current and applicable
```

**Action Steps**:
1. ✅ Implement the practice/pattern/technique
2. ✅ Document in `decisions.md`:
   - What was adopted
   - Source and validation results
   - Rationale for adoption
   - Integration notes
3. ✅ Update relevant guides if needed:
   - `claude.md` (if project-wide rule)
   - `CONTEXT_ENGINEERING_GUIDE.md` (if CE-related)
   - `AGENT_SKILLS_GUIDE.md` (if skills-related)
4. ✅ Test in practice
5. ✅ Monitor results
6. ✅ Iterate if needed

**Example**:
```markdown
## Adopted: Progressive Disclosure in Skills
- Source: Anthropic Agent Skills Documentation (Tier 1)
- Validation: All checks passed
- Rationale: Official framework, strong evidence, solves context bloat
- Integration: Built skills/ directory with SKILL.md pattern
- Result: Reduced context usage by ~40%
```

---

### ⚠️ ADAPT - Modify before implementing

**When to Use**:
- Core idea is sound but needs modification
- Source is Tier 2-3 with good evidence
- Mostly aligns with sources of truth
- Good fit with modifications
- Worth the effort to adapt

**Criteria Matrix**:
```
Authority:     Tier 2-3, Medium-High credibility
Evidence:      Moderate to Strong
Consistency:   Mostly aligns, minor conflicts
Practical:     High value IF adapted
Recency:       Current or easily updated
```

**Modification Reasons**:
- Adjust to fit your specific workflow
- Update for current Claude version
- Simplify overly complex approach
- Remove conflicting parts
- Extend to cover more use cases
- Combine with your existing patterns

**Action Steps**:
1. ⚠️ Identify what needs modification
2. ⚠️ Document original vs adapted version
3. ⚠️ Explain rationale for changes
4. ⚠️ Validate adapted version still makes sense
5. ⚠️ Implement adapted version
6. ⚠️ Document in `decisions.md`:
   - Original recommendation
   - Your adaptation
   - Why adapted
   - Results
7. ⚠️ Test thoroughly
8. ⚠️ Update guides if successful

**Example**:
```markdown
## Adapted: Context Compaction Threshold
- Source: Community discussion (Tier 3)
- Original: Compact at 50% context usage
- Validation: No Tier 1 source specified threshold
- Adaptation: Tested 50%, 60%, 70% thresholds
- Rationale: 60-70% provides best balance for our workflow
- Result: Adopted 60% recommendation, 70% warning in our guides
```

---

### 🔍 INVESTIGATE - Needs more validation

**When to Use**:
- Interesting idea but insufficient evidence
- Source is Tier 3-4 but seems promising
- Partially aligns, unclear if conflicts are deal-breakers
- Potential value but needs testing
- Novel approach worth exploring

**Criteria Matrix**:
```
Authority:     Tier 3-4, or unclear
Evidence:      Weak or anecdotal but logical
Consistency:   Unclear or partially conflicts
Practical:     Potentially valuable
Recency:       Needs verification
```

**Investigation Steps**:
1. 🔍 Document what needs investigation
2. 🔍 Define investigation plan:
   - What to test
   - How to test it
   - Success criteria
   - Time limit
3. 🔍 Search for additional evidence:
   - Tier 1-2 sources on topic
   - Research papers
   - Multiple independent confirmations
4. 🔍 Test in practice (if safe):
   - Small-scale experiment
   - Document results
   - Compare to current approach
5. 🔍 Set re-evaluation date
6. 🔍 Decision after investigation:
   - ADOPT if validated
   - ADAPT if needs modification
   - REJECT if disproven
   - Continue investigating if inconclusive

**Documentation**:
Create investigation entry in `decisions.md` or separate investigation notes:
```markdown
## Investigating: [Topic]
- Source: [Origin]
- Date Started: [Date]
- Hypothesis: [What we're testing]
- Investigation Plan: [Steps]
- Success Criteria: [How we'll know]
- Re-evaluate: [Date]
- Status: [In Progress/Concluded]
- Results: [Findings]
- Final Decision: [TBD/ADOPT/ADAPT/REJECT]
```

**Example**:
```markdown
## Investigation: 50% Compaction Threshold
- Source: Discord community member (Tier 3)
- Claim: Compacting at 50% prevents all hallucinations
- Status: Testing for 2 weeks
- Method: Comparing 50% vs 60% compaction in practice
- Success Criteria: Measurable reduction in hallucinations
- Results (Week 1): No significant difference observed
- Results (Week 2): 50% creates unnecessary interruptions
- Final Decision: REJECT - 60% remains optimal
```

---

### ❌ REJECT - Do not implement

**When to Use**:
- Contradicts Tier 1 sources
- No evidence or weak evidence
- Fails multiple validation questions
- High risk, low reward
- Outdated or superseded
- Doesn't solve real problem
- Not worth the effort

**Criteria Matrix**:
```
Authority:     Low credibility or Tier 4
Evidence:      Weak, none, or contradictory
Consistency:   Contradicts Tier 1/2
Practical:     Low value or high cost
Recency:       Outdated or superseded
```

**Rejection Reasons**:
- **Contradicts Ground Truth**: Conflicts with Tier 1 sources
- **No Evidence**: Unsubstantiated claims
- **Outdated**: Superseded by newer information
- **Impractical**: Cost outweighs benefit
- **Irrelevant**: Doesn't apply to your use case
- **Risky**: Potential for harm with no clear benefit

**Action Steps**:
1. ❌ Do not implement
2. ❌ Document rejection (optional but recommended):
   - What was rejected
   - Why it was rejected
   - What validation failed
3. ❌ Note in `decisions.md` if significant:
   - Prevents reconsidering later
   - Documents your reasoning
   - Helps others understand your choices

**Documentation Template**:
```markdown
## Rejected: [Topic]
- Source: [Origin]
- Tier: [1-4]
- Rejection Reason: [Primary reason]
- Validation Failures:
  - Authority: [Why failed]
  - Evidence: [Why failed]
  - Consistency: [Why failed]
  - Practical: [Why failed]
  - Recency: [Why failed]
- Rationale: [Detailed explanation]
```

**Example**:
```markdown
## Rejected: "Always use compaction at 90%"
- Source: Random blog post (Tier 4)
- Rejection Reason: Contradicts Anthropic guidance and defeats purpose
- Validation Failures:
  - Authority: Unknown blogger, no credentials
  - Evidence: No data, just opinion
  - Consistency: Contradicts proactive compaction principle
  - Practical: Waits too long, risks auto-compact
  - Recency: Doesn't account for new features
- Rationale: Waiting until 90% removes control and is reactive, not proactive. Our tested 60-70% approach is superior.
```

---

### 📝 ARCHIVE - Save for later

**When to Use**:
- Interesting but not currently relevant
- Solves a problem you don't have yet
- Good idea but no capacity to implement now
- Might be useful in future context
- Worth remembering but not acting on now

**Criteria Matrix**:
```
Authority:     Any tier
Evidence:      Any level
Consistency:   Not conflicting
Practical:     Not applicable now, but might be later
Recency:       Current enough to save
```

**Archive Reasons**:
- **Future Feature**: Relevant when you build X
- **Different Context**: Useful for different project type
- **Capacity**: Good idea, but no time/resources now
- **Dependency**: Need something else first
- **Exploration**: Interesting for future research

**Action Steps**:
1. 📝 Create archive entry
2. 📝 Document:
   - What it is
   - Why it's interesting
   - When it might be relevant
   - Where to find more info
3. 📝 Set review date (optional)
4. 📝 Tag for easy retrieval

**Archive Location Options**:
- `decisions.md` (Archive section)
- Separate `archive.md` file
- Note-taking system outside project
- Bookmarks with tags

**Documentation Template**:
```markdown
## Archived: [Topic]
- Source: [Origin + URL]
- Date Archived: [Date]
- Why Interesting: [Value proposition]
- Why Not Now: [Reason for archiving]
- Relevant When: [Future condition]
- Review Date: [Optional future date]
- Tags: [For search/retrieval]
```

**Example**:
```markdown
## Archived: Sub-Agent Multi-Project Coordination
- Source: Anthropic cookbook example (Tier 2)
- Date Archived: 2025-10-21
- Why Interesting: Coordinate multiple agents across different projects
- Why Not Now: Currently single project, not needed yet
- Relevant When: If we expand to multi-project development
- Review Date: Q2 2026
- Tags: #sub-agents #multi-project #scaling
```

---

## Decision Flowchart

```
New Information
    ↓
Apply 5-Question Validation
    ↓
┌─────────────────────────────────┐
│ How many questions pass?        │
└─────────────────────────────────┘
    ↓
    ├─ All 5 Pass Strongly
    │  └→ ✅ ADOPT
    │
    ├─ 3-4 Pass, Minor Issues
    │  └→ ⚠️ ADAPT
    │
    ├─ 2-3 Pass, Promising but Unclear
    │  └→ 🔍 INVESTIGATE
    │
    ├─ 0-2 Pass, Major Issues
    │  └→ ❌ REJECT
    │
    └─ Passes but Not Relevant Now
       └→ 📝 ARCHIVE
```

---

## Special Cases

### Case 1: Tier 1 Source Contradicts Your Implementation

**Scenario**: Anthropic releases new guidance that contradicts your current practice

**Decision**: ✅ **ADOPT (Update)**

**Reasoning**:
- Tier 1 is ground truth
- Your implementation must align
- Likely improvement based on new research

**Action**:
1. Review new Tier 1 guidance thoroughly
2. Document what changed and why
3. Update your Tier 2 documentation
4. Test new approach
5. Document results in `decisions.md`

**Example**:
```markdown
## Updated: Compaction Strategy Based on New Research
- Source: Anthropic "Context Engineering v2" (Tier 1)
- Previous: 60-70% threshold
- New: 50-60% threshold with improved retention
- Rationale: New research shows better results
- Action: Updated CONTEXT_ENGINEERING_GUIDE.md
- Result: Testing new thresholds
```

### Case 2: Tier 1 Sources Conflict

**Scenario**: Two Anthropic sources seem to contradict

**Decision**: 🔍 **INVESTIGATE**

**Action**:
1. Re-read both sources carefully
2. Check publication dates (newer usually wins)
3. Look for clarifications/updates
4. Check if they address different contexts
5. Ask for clarification if still unclear
6. Document your resolution

### Case 3: Community vs Your Testing

**Scenario**: Tier 3 community says X, but your testing shows Y

**Decision**: Trust your testing (Your Tier 2 wins)

**Reasoning**:
- Your testing is evidence-based
- Your context is specific to your needs
- Community advice may not fit your use case

**Action**:
1. Document your testing results
2. Note the community recommendation
3. Explain why your approach works better
4. Stay open to re-testing if new evidence emerges

### Case 4: Multiple Tier 3 Sources Agree

**Scenario**: Multiple independent Tier 3 sources recommend same thing

**Decision**: 🔍 **INVESTIGATE → Likely ADOPT/ADAPT**

**Reasoning**:
- Multiple confirmations increase credibility
- Community validation matters
- Worth testing even if not Tier 1

**Action**:
1. Verify independence (not copying each other)
2. Test the recommendation
3. Validate against Tier 1 principles
4. Adopt if testing confirms value

---

## Decision Documentation Template

For significant decisions, document in `decisions.md`:

```markdown
## [Decision]: [Topic]
**Date**: [YYYY-MM-DD]

### Source Information
- **Origin**: [Where you found this]
- **Tier**: [1/2/3/4]
- **URL**: [If available]

### Validation Summary
- **Authority**: [Pass/Fail + brief note]
- **Evidence**: [Pass/Fail + brief note]
- **Consistency**: [Pass/Fail + brief note]
- **Practical**: [Pass/Fail + brief note]
- **Recency**: [Pass/Fail + brief note]

### Decision: [ADOPT/ADAPT/INVESTIGATE/REJECT/ARCHIVE]

### Rationale
[Detailed explanation of why this decision was made]

### Action Taken
- [Specific actions if ADOPT/ADAPT]
- [Investigation plan if INVESTIGATE]
- [Archive notes if ARCHIVE]

### Results (if applicable)
- [Outcomes after implementation/testing]

### Updates (if any)
- [Date]: [What changed and why]
```

---

## Quick Reference Table

| Decision | Authority | Evidence | Consistency | Practical | Recency | Action |
|----------|-----------|----------|-------------|-----------|---------|--------|
| **ADOPT** | High | Strong | Aligns | High Value | Current | Implement as-is |
| **ADAPT** | Med-High | Moderate | Mostly | Good IF adapted | Current | Modify then implement |
| **INVESTIGATE** | Medium | Weak | Unclear | Potential | Verify | Test before deciding |
| **REJECT** | Low | Weak/None | Conflicts | Low Value | Outdated | Do not implement |
| **ARCHIVE** | Any | Any | No conflict | Not now | Current | Save for later |

---

## Summary

**Five Decisions**:
- ✅ **ADOPT**: All checks pass, implement as-is
- ⚠️ **ADAPT**: Good idea, modify to fit
- 🔍 **INVESTIGATE**: Promising, test first
- ❌ **REJECT**: Fails validation, don't use
- 📝 **ARCHIVE**: Interesting, save for later

**Key Principle**: Systematic evaluation leads to confident, documented decisions that maintain consistency with your sources of truth while remaining open to valuable improvements.
