# Source Hierarchy

## Overview

This document defines the authoritative hierarchy of information sources for AI coding with Claude Code. When evaluating new information, always check which tier it belongs to.

---

## Tier 1: Ground Truth (Absolute Authority)

These are your **primary sources of truth**. Information from these sources is considered authoritative and correct by default.

### Official Anthropic Research & Documentation

**1. Anthropic Research Papers**
- Context Engineering for AI Agents
- Agent Skills Framework
- Constitutional AI papers
- Model capability research
- **URL Pattern**: `anthropic.com/research/*`
- **Authority**: Highest - direct from Anthropic research team

**2. Claude Code Official Documentation**
- Official Claude Code docs
- Command reference
- Feature documentation
- Best practices guides
- **URL Pattern**: `docs.claude.com/claude-code/*`
- **Authority**: Highest - official product documentation

**3. Anthropic API Documentation**
- API reference
- Model specifications
- Token limits and context windows
- Feature capabilities
- **URL Pattern**: `docs.anthropic.com/*`
- **Authority**: Highest - official API documentation

**4. Anthropic Official Blog**
- Product announcements
- Feature releases
- Research summaries
- Engineering at Anthropic posts
- **URL Pattern**: `anthropic.com/news/*`, `anthropic.com/engineering/*`
- **Authority**: Highest - official company communication

### Validation for Tier 1

- ✅ Accept as authoritative
- ✅ Use to validate all other tiers
- ✅ Update your implementation when Tier 1 changes
- ⚠️ If Tier 1 sources conflict, use most recent or ask for clarification

---

## Tier 2: Verified Expert Sources

These sources have credibility but should be **validated against Tier 1** before adoption.

### Anthropic Employees & Researchers

**1. Anthropic Employee Talks/Presentations**
- Conference presentations by Anthropic staff
- Workshop materials from Anthropic team
- Technical talks by engineers
- **Verification**: Check speaker works at Anthropic
- **Authority**: High - internal expertise

**2. Anthropic Employee Blog Posts**
- Personal blogs by Anthropic researchers
- Technical writeups by Anthropic engineers
- **Verification**: Verify employment, check if opinions are personal vs official
- **Authority**: High, but distinguish opinion from policy

### Peer-Reviewed Research

**3. Academic Papers Citing Anthropic**
- Research papers building on Anthropic work
- Peer-reviewed studies using Claude
- Academic analysis of AI agent patterns
- **Verification**: Check peer review, citations, methodology
- **Authority**: Medium-High - validated by peers

### Official Example Repositories

**4. Anthropic Official Cookbooks/Examples**
- anthropic-cookbook GitHub repository
- Official example code
- Reference implementations
- **URL Pattern**: `github.com/anthropics/*`
- **Authority**: High - official examples

### Validation for Tier 2

- ✅ Verify against Tier 1 sources
- ✅ Check for evidence and research backing
- ⚠️ Distinguish opinion from fact
- ⚠️ Verify author credentials
- ❌ Reject if contradicts Tier 1

---

## Tier 3: Community-Validated Sources

These sources represent **community wisdom** but require careful validation.

### Established Developer Community

**1. High-Quality Technical Blogs**
- Blogs by recognized AI developers
- Technical writeups with code examples
- Well-researched tutorials
- **Verification**: Check author expertise, look for evidence
- **Authority**: Medium - depends on author and content quality

**2. Open-Source Claude Projects**
- Popular GitHub projects using Claude
- Well-maintained agent frameworks
- Community tools with good adoption
- **Verification**: Check stars, activity, code quality, tests
- **Authority**: Medium - validated by community usage

**3. Developer Forum Discussions**
- Anthropic Discord community
- Claude Code GitHub discussions
- Stack Overflow Claude-tagged questions
- **Verification**: Check upvotes, multiple confirmations, test in practice
- **Authority**: Medium-Low - varies by contributor

**4. Technical YouTube Channels**
- Educational content on AI coding
- Claude Code tutorials
- Agent development patterns
- **Verification**: Check channel credibility, viewer feedback, test recommendations
- **Authority**: Medium-Low - educational but may contain errors

### Validation for Tier 3

- ⚠️ Validate carefully against Tier 1 & 2
- ⚠️ Look for multiple independent confirmations
- ⚠️ Test in practice before adopting
- ⚠️ Check if information is current
- ❌ Reject if unverified or contradicts higher tiers

---

## Tier 4: Experimental/Opinion Sources

These sources are **opinions or experiments** and require extensive validation before consideration.

### Individual Opinions & Experiments

**1. Personal Blog Posts**
- Individual developer opinions
- "Here's what worked for me" posts
- Experimental approaches
- **Verification**: Treat as hypothesis, test thoroughly
- **Authority**: Low - personal experience

**2. Social Media Posts**
- Twitter/X threads
- LinkedIn posts
- Reddit comments
- **Verification**: Verify claims independently
- **Authority**: Very Low - often incomplete or incorrect

**3. Unverified Tutorials**
- Random blog tutorials
- Medium posts without evidence
- "Quick tips" without research
- **Verification**: Test thoroughly, look for evidence
- **Authority**: Very Low - may be outdated or wrong

**4. AI-Generated Content**
- ChatGPT explanations
- AI-written blog posts
- Synthetic tutorials
- **Verification**: Verify every claim independently
- **Authority**: Very Low - may hallucinate

### Validation for Tier 4

- 🔍 Treat as hypotheses to investigate
- 🔍 Require strong evidence before considering
- 🔍 Must align with Tier 1-2 to be considered
- 🔍 Test extensively in practice
- ❌ Default to reject unless proven valuable
- 📝 Archive interesting ideas for later investigation

---

## Your Implementation Standards (Tier 2 Status)

Your documented decisions and guides have **Tier 2 authority** for your project:

### Project Documentation

**1. `claude.md`**
- Your project rules and preferences
- Established conventions
- Project-specific requirements
- **Authority**: High for this project
- **Scope**: Project-level decisions

**2. `CONTEXT_ENGINEERING_GUIDE.md`**
- Your implementation of Anthropic principles
- Tested workflows and patterns
- Documented best practices
- **Authority**: High - based on Tier 1 sources
- **Validation**: Must stay consistent with Tier 1

**3. `AGENT_SKILLS_GUIDE.md`**
- Your skills implementation standards
- Tested skill patterns
- Documented workflows
- **Authority**: High - based on Tier 1 sources
- **Validation**: Must stay consistent with Tier 1

**4. `decisions.md`**
- Your architectural decisions
- Documented rationale
- Lessons learned
- **Authority**: High for this project
- **Scope**: Project context and history

### Important Notes

- These docs have **Tier 2 authority** because they implement Tier 1 principles
- They must **remain consistent** with Tier 1 sources
- When Tier 1 updates, these docs should be **reviewed and updated**
- They represent **your tested implementation**, not universal truth

---

## Decision Rules

### When Sources Conflict

**Tier 1 vs Tier 1**:
- Use most recent source
- Check for updates/corrections
- Ask for clarification if needed

**Tier 1 vs Tier 2/3/4**:
- Tier 1 wins always
- Update lower tier or reject it

**Tier 2 vs Tier 3/4**:
- Prefer Tier 2
- Consider Tier 3/4 only if strong evidence supports it

**Your Docs vs External Tier 2**:
- Your docs win for your project (you've tested it)
- Consider external Tier 2 for improvements
- Document if you change based on external input

### When to Update Sources of Truth

**Tier 1 Updates**:
- ✅ Anthropic releases new research/docs
- ✅ Claude Code adds new features
- ✅ API capabilities change
- ✅ Official guidance evolves

**Tier 2 Updates (Your Docs)**:
- ✅ When Tier 1 sources change
- ✅ When you discover better practices through testing
- ✅ When project requirements evolve
- ✅ When you document new architectural decisions

### What to Do When Sources Update

1. **Monitor Tier 1 sources** for changes
2. **Review your implementation** (Tier 2 docs)
3. **Update if needed** to maintain consistency
4. **Document changes** in `decisions.md`
5. **Test updated practices** in your workflow
6. **Archive outdated information** (don't delete, mark as superseded)

---

## Examples

### Example 1: Evaluating a Blog Post

**Scenario**: You find a blog post titled "10 Claude Code Tips"

**Evaluation**:
1. **Source Tier**: Tier 3 or 4 (depends on author)
2. **Check author**: Known AI developer? → Tier 3. Unknown? → Tier 4
3. **Validate each tip**:
   - Does it cite Tier 1 sources? ✅
   - Does it contradict your Tier 2 docs? Check
   - Is there evidence it works? Test it
4. **Decision**: Adopt specific tips that validate, reject unsupported claims

### Example 2: Anthropic Releases New Research

**Scenario**: Anthropic publishes "Advanced Agent Patterns" paper

**Evaluation**:
1. **Source Tier**: Tier 1 (official research)
2. **Authority**: Highest - accept as ground truth
3. **Action**:
   - Review your Tier 2 docs
   - Update guides if new patterns are recommended
   - Document changes in `decisions.md`
   - Test new patterns in practice

### Example 3: Community Forum Suggestion

**Scenario**: Someone on Discord says "Always compact at 50% context"

**Evaluation**:
1. **Source Tier**: Tier 3/4 (community opinion)
2. **Validate**:
   - Check Tier 1: Anthropic says auto-compact at 92%
   - Check Tier 2: Your guide says 60-70%
   - Evidence for 50%? None provided
3. **Reasoning**: More conservative than your tested 60-70%, but not invalid
4. **Decision**: INVESTIGATE - test if 50% provides better results
5. **If proven**: Update your Tier 2 docs with findings

### Example 4: AI-Generated Tutorial

**Scenario**: ChatGPT gives you "Claude Code best practices"

**Evaluation**:
1. **Source Tier**: Tier 4 (AI-generated, may hallucinate)
2. **Validate each claim**:
   - Check against Tier 1 sources
   - Test in practice
   - Look for evidence
3. **Likely outcome**: Some valid (copied from Tier 1), some invalid (hallucinated)
4. **Decision**: Verify each claim independently, reject unverified

---

## Maintaining Source Hierarchy

### Regular Reviews

**Monthly**:
- Check for new Tier 1 publications
- Review if your Tier 2 docs still align
- Update outdated information

**Quarterly**:
- Deep review of all sources of truth
- Archive superseded information
- Document major changes

**When Claude Updates**:
- Review Tier 1 documentation for changes
- Test if your workflows still work
- Update guides if needed

### Documentation

When you adopt information:
- **Document source tier** in `decisions.md`
- **Reference original source** (URL, date)
- **Note validation process** used
- **Record testing results** if applicable

---

## Summary

**Hierarchy**:
```
Tier 1: Anthropic Official → Ground Truth
Tier 2: Verified Experts + Your Tested Docs → High Authority
Tier 3: Community-Validated → Medium Authority (validate carefully)
Tier 4: Experimental/Opinion → Low Authority (extensive validation required)
```

**Rules**:
- Higher tier always wins in conflicts
- Your docs are Tier 2, must align with Tier 1
- Validate Tier 3/4 against Tier 1/2 before adopting
- Document all decisions and sources
- Update when ground truth evolves

**Goal**: Evidence-based, systematic, bias-resistant knowledge validation.
