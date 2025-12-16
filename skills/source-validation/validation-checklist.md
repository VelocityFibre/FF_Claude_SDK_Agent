# Validation Checklist

## Overview

This checklist provides a systematic, step-by-step process for evaluating any new information against your sources of truth using first principles reasoning.

---

## The 5-Question Framework

Apply these five questions to every piece of new information:

---

## Question 1: Authority Check

**Purpose**: Determine source credibility and expertise

### Steps

1. **Identify the author/creator**
   - Individual name or organization?
   - Can you verify their identity?

2. **Check credentials**
   - What is their expertise in AI/Claude/coding?
   - Do they work at Anthropic?
   - Are they a recognized expert?
   - What's their track record?

3. **Determine source tier**
   - Is this Tier 1 (Anthropic official)?
   - Is this Tier 2 (verified expert)?
   - Is this Tier 3 (community)?
   - Is this Tier 4 (opinion/experimental)?

4. **Check publication venue**
   - Official documentation?
   - Research journal?
   - Personal blog?
   - Social media?

### Red Flags
- ❌ Anonymous or unverifiable author
- ❌ No relevant credentials
- ❌ Self-proclaimed "expert" without evidence
- ❌ No professional affiliation
- ❌ Contradicts known experts without explanation

### Green Flags
- ✅ Anthropic employee or official source
- ✅ Recognized AI researcher with publications
- ✅ Verifiable industry expert
- ✅ Multiple credentials in relevant field
- ✅ Cites other authoritative sources

### Output
```
Authority Assessment:
- Author: [Name/Organization]
- Credentials: [Expertise/Role]
- Source Tier: [1/2/3/4]
- Authority Level: [Highest/High/Medium/Low/Very Low]
- Rationale: [Why this rating]
```

---

## Question 2: Evidence Check

**Purpose**: Determine if claims are backed by data, research, or testing

### Steps

1. **Look for evidence type**
   - Research data?
   - Benchmarks/measurements?
   - Code examples?
   - Real-world testing?
   - Case studies?

2. **Check methodology**
   - How was this tested?
   - What was the sample size?
   - Were proper controls used?
   - Is methodology documented?
   - Can it be reproduced?

3. **Verify claims**
   - Are specific numbers provided?
   - Are results reproducible?
   - Are there citations to sources?
   - Is evidence objective or anecdotal?

4. **Check for peer review/validation**
   - Has this been peer-reviewed?
   - Have others validated the claims?
   - Are there independent confirmations?

### Red Flags
- ❌ "Trust me" or "in my experience" without data
- ❌ Vague claims without specifics
- ❌ No methodology described
- ❌ Cherry-picked examples
- ❌ Unreproducible results
- ❌ Conflicts with established research

### Green Flags
- ✅ Specific measurements and data
- ✅ Clear methodology
- ✅ Reproducible results
- ✅ Multiple independent confirmations
- ✅ Peer-reviewed or officially validated
- ✅ Citations to authoritative sources

### Output
```
Evidence Assessment:
- Evidence Type: [Research/Testing/Anecdotal/None]
- Methodology: [Described/Undescribed]
- Reproducible: [Yes/No/Unknown]
- Independent Validation: [Yes/No/Not Needed]
- Evidence Quality: [Strong/Moderate/Weak/None]
- Rationale: [Why this rating]
```

---

## Question 3: Consistency Check

**Purpose**: Verify alignment with established sources of truth

### Steps

1. **Check against Tier 1 sources**
   - Does it contradict Anthropic's documentation?
   - Does it align with Context Engineering principles?
   - Does it align with Agent Skills framework?
   - Is it consistent with Claude Code docs?

2. **Check against your Tier 2 docs**
   - Does it contradict `claude.md`?
   - Does it conflict with `CONTEXT_ENGINEERING_GUIDE.md`?
   - Does it conflict with `AGENT_SKILLS_GUIDE.md`?
   - Does it contradict `decisions.md`?

3. **Identify contradictions**
   - List specific contradictions
   - Assess severity (major vs minor)
   - Check if it's an update vs a contradiction

4. **Identify alignments**
   - List specific alignments
   - Note if it reinforces existing principles
   - Check if it extends without contradicting

### Red Flags
- ❌ Directly contradicts Tier 1 sources
- ❌ Conflicts with established best practices
- ❌ Ignores known limitations
- ❌ Contradicts your tested implementation
- ❌ No acknowledgment of conflicting views

### Green Flags
- ✅ Aligns with Tier 1 sources
- ✅ Extends principles without contradicting
- ✅ Acknowledges and addresses conflicts
- ✅ Consistent with your implementation
- ✅ Builds on established foundation

### Output
```
Consistency Assessment:
- Tier 1 Alignment: [Full/Partial/None/Contradicts]
  - Contradictions: [List]
  - Alignments: [List]

- Tier 2 Alignment (Your Docs): [Full/Partial/None/Contradicts]
  - Contradictions: [List]
  - Alignments: [List]

- Overall Consistency: [Consistent/Partially Consistent/Inconsistent]
- Rationale: [Why this rating]
```

---

## Question 4: Practical Check

**Purpose**: Assess real-world value and implementation feasibility

### Steps

1. **Identify the problem it solves**
   - What problem does this address?
   - Is it a real problem you have?
   - How significant is the problem?
   - Are there existing solutions?

2. **Assess implementation cost**
   - How much effort to implement?
   - What's the learning curve?
   - Does it require breaking changes?
   - What's the risk of implementation?

3. **Estimate expected benefit**
   - What specific improvements are expected?
   - Are benefits measurable?
   - What's the magnitude of improvement?
   - Are benefits worth the cost?

4. **Check for trade-offs**
   - What do you give up?
   - Are there downsides?
   - Does it add complexity?
   - Does it create new problems?

5. **Assess fit with your workflow**
   - Does it fit your current setup?
   - Does it require other changes?
   - Is it compatible with your tools?
   - Will it integrate smoothly?

### Red Flags
- ❌ Solution looking for a problem
- ❌ High cost, unclear benefit
- ❌ Requires major breaking changes
- ❌ Adds significant complexity
- ❌ Doesn't fit your workflow
- ❌ Benefits are vague or unmeasurable

### Green Flags
- ✅ Solves a real, current problem
- ✅ Clear, measurable benefits
- ✅ Reasonable implementation effort
- ✅ Integrates with existing workflow
- ✅ Benefits clearly outweigh costs
- ✅ Low risk, high reward

### Output
```
Practical Assessment:
- Problem Addressed: [Description]
- Problem Severity: [High/Medium/Low/Not Applicable]
- Implementation Effort: [High/Medium/Low]
- Expected Benefit: [Specific improvements]
- Benefit Magnitude: [High/Medium/Low]
- Trade-offs: [List]
- Cost/Benefit Ratio: [Favorable/Neutral/Unfavorable]
- Workflow Fit: [Excellent/Good/Poor]
- Rationale: [Why this rating]
```

---

## Question 5: Recency Check

**Purpose**: Ensure information is current and not outdated

### Steps

1. **Check publication date**
   - When was this published?
   - How old is the information?

2. **Check Claude/API version**
   - What version of Claude does this reference?
   - Is it current with latest model?
   - Are features still available?

3. **Look for updates/corrections**
   - Has this been updated?
   - Are there corrections or errata?
   - Has the author retracted anything?

4. **Check if superseded**
   - Has newer information replaced this?
   - Have Tier 1 sources updated since?
   - Are there more recent best practices?

5. **Verify current applicability**
   - Does this still apply?
   - Have capabilities changed?
   - Are limits different now?

### Red Flags
- ❌ References old Claude versions (pre-3.5)
- ❌ Outdated context window limits
- ❌ Describes deprecated features
- ❌ Published before major updates
- ❌ Author has posted updates/corrections
- ❌ Superseded by official guidance

### Green Flags
- ✅ Recently published (within 6 months)
- ✅ References current Claude version
- ✅ Acknowledges recent updates
- ✅ Aligns with latest features
- ✅ Author confirms still valid
- ✅ No newer conflicting information

### Output
```
Recency Assessment:
- Publication Date: [Date]
- Age: [Time since publication]
- Claude Version Referenced: [Version]
- Current as of: [Date checked]
- Updates/Corrections: [Yes/No, details]
- Superseded By: [Newer source or N/A]
- Still Applicable: [Yes/No/Partially]
- Rationale: [Why this rating]
```

---

## Complete Validation Template

Use this template for full evaluation:

```markdown
# Validation Report: [Content Title]

## Source Information
- **Title**: [Full title]
- **Author**: [Name/Organization]
- **URL**: [Link if available]
- **Date**: [Publication date]
- **Type**: [Blog/Video/Paper/Tutorial/Documentation]

---

## Question 1: Authority Check
- **Author**: [Name/Organization]
- **Credentials**: [Expertise/Role]
- **Source Tier**: [1/2/3/4]
- **Authority Level**: [Rating]
- **Rationale**: [Why]

---

## Question 2: Evidence Check
- **Evidence Type**: [Research/Testing/Anecdotal/None]
- **Methodology**: [Described/Undescribed]
- **Reproducible**: [Yes/No]
- **Evidence Quality**: [Strong/Moderate/Weak/None]
- **Rationale**: [Why]

---

## Question 3: Consistency Check
### Tier 1 Alignment: [Rating]
- **Contradictions**: [List or "None"]
- **Alignments**: [List or "None"]

### Tier 2 Alignment: [Rating]
- **Contradictions**: [List or "None"]
- **Alignments**: [List or "None"]

**Overall Consistency**: [Consistent/Partial/Inconsistent]
**Rationale**: [Why]

---

## Question 4: Practical Check
- **Problem Addressed**: [Description]
- **Problem Severity**: [High/Medium/Low]
- **Implementation Effort**: [High/Medium/Low]
- **Expected Benefit**: [Specific improvements]
- **Cost/Benefit**: [Favorable/Neutral/Unfavorable]
- **Workflow Fit**: [Excellent/Good/Poor]
- **Rationale**: [Why]

---

## Question 5: Recency Check
- **Publication Date**: [Date]
- **Claude Version**: [Version referenced]
- **Still Applicable**: [Yes/No/Partially]
- **Superseded By**: [Source or N/A]
- **Rationale**: [Why]

---

## Key Claims Extracted
1. [Claim 1]
2. [Claim 2]
3. [Claim 3]
[Continue as needed]

---

## Bias Assessment
- **Detected Biases**: [In source or in evaluation]
- **Mitigation**: [How addressed]

---

## Final Recommendation

**Decision**: [ADOPT / ADAPT / INVESTIGATE / REJECT / ARCHIVE]

**Reasoning**:
[Detailed explanation of why this decision was made based on the 5 questions]

**Action Items** (if ADOPT/ADAPT):
- [ ] [Specific actions to take]
- [ ] [Integration steps]
- [ ] [Testing requirements]
- [ ] [Documentation updates]

**Documentation** (if ADOPT):
- Update `decisions.md` with: [What to document]
- Update [relevant guide] with: [What to add]

**Archive Reason** (if ARCHIVE):
[Why saving for later]

**Rejection Reason** (if REJECT):
[Why not adopting]

---

## Follow-up
- **Re-evaluation Date**: [If INVESTIGATE]
- **Testing Period**: [If ADOPT/ADAPT]
- **Success Criteria**: [How to measure]
```

---

## Quick Reference Decision Tree

```
1. Authority Check → Tier 1?
   ├─ Yes → Proceed, high trust
   └─ No → Continue validation carefully

2. Evidence Check → Strong evidence?
   ├─ Yes → Continue
   └─ No → Flag for investigation or reject

3. Consistency Check → Aligns with Tier 1?
   ├─ Yes → Continue
   ├─ Partial → Investigate contradiction
   └─ No → Likely reject (unless updating Tier 1)

4. Practical Check → Solves real problem?
   ├─ Yes → Cost < Benefit?
   │  ├─ Yes → Continue
   │  └─ No → Reject
   └─ No → Reject or archive

5. Recency Check → Still current?
   ├─ Yes → Make final decision
   └─ No → Find updated source or reject

Final Decision:
├─ All checks pass → ADOPT
├─ Most pass, needs tweaks → ADAPT
├─ Promising but unclear → INVESTIGATE
├─ Fails checks → REJECT
└─ Interesting but not now → ARCHIVE
```

---

## Tips for Effective Validation

### Be Systematic
- Don't skip questions
- Document each assessment
- Use the template
- Track your reasoning

### Be Objective
- Check for biases (yours and source's)
- Separate facts from opinions
- Look for evidence
- Question assumptions

### Be Thorough
- Read entire source, not just summary
- Check linked references
- Look for contradictions
- Test claims when possible

### Be Practical
- Consider implementation reality
- Assess actual value
- Think about maintenance
- Evaluate trade-offs

### Document Everything
- Record your validation
- Note sources checked
- Save reasoning
- Update when re-evaluated

---

## Summary

**The 5 Questions**:
1. **Authority**: Who says this and why should I trust them?
2. **Evidence**: What proof backs this up?
3. **Consistency**: Does this align with what I know to be true?
4. **Practical**: Does this solve a real problem worth solving?
5. **Recency**: Is this still current and applicable?

**Result**: Systematic, bias-resistant, evidence-based evaluation of any new information.
