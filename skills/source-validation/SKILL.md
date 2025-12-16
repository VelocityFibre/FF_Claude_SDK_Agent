---
name: Source of Truth Validation
description: Systematic framework for evaluating new information against established sources of truth using first principles, bias detection, and evidence-based reasoning
---

# Source of Truth Validation Skill

## When to Use This Skill

Activate this skill when:
- Evaluating new AI coding practices, techniques, or patterns
- Assessing blog posts, tutorials, or community recommendations
- Considering changes to established workflows
- Reviewing transcripts, videos, or educational content
- Someone suggests "best practices" or new approaches
- Deciding whether to adopt/adapt/reject new information

## Core Purpose

This skill prevents:
- ❌ Adopting unverified practices
- ❌ Contradicting established principles
- ❌ Falling for cognitive biases
- ❌ Implementing ineffective patterns
- ❌ Wasting time on low-quality information

This skill ensures:
- ✅ Evidence-based decision making
- ✅ Consistency with authoritative sources
- ✅ Systematic evaluation process
- ✅ Documented reasoning
- ✅ Protection against bias

## Validation Framework (First Principles)

### Step 1: Source Classification

Classify the information source using the hierarchy in [source-hierarchy.md](source-hierarchy.md):

- **Tier 1**: Official Anthropic sources (ground truth)
- **Tier 2**: Verified expert sources
- **Tier 3**: Community-validated sources
- **Tier 4**: Experimental/opinion sources

### Step 2: Systematic Validation

Apply the 5-question framework from [validation-checklist.md](validation-checklist.md):

1. **Authority Check**: Who wrote this? What's their expertise?
2. **Evidence Check**: Is there data/research backing this?
3. **Consistency Check**: Does it contradict our sources of truth?
4. **Practical Check**: Can we implement this? What's the value?
5. **Recency Check**: Is it current with latest features?

### Step 3: Bias Detection

Screen for common cognitive biases using [bias-detection.md](bias-detection.md):

- Confirmation bias
- Novelty bias
- Authority bias
- Availability bias
- Sunk cost fallacy

### Step 4: Decision

Use the decision matrix from [decision-matrix.md](decision-matrix.md):

- ✅ **ADOPT**: Aligns fully, adds clear value
- ⚠️ **ADAPT**: Good idea, needs modification
- 🔍 **INVESTIGATE**: Promising, needs more validation
- ❌ **REJECT**: Contradicts sources of truth
- 📝 **ARCHIVE**: Not relevant now, save for later

## Quick Actions

### When User Shares New Content

1. **Identify source** (Tier 1-4)
2. **Apply validation checklist** (5 questions)
3. **Check for biases** (yours and the source's)
4. **Extract key claims/principles**
5. **Compare against sources of truth**
6. **Flag contradictions**
7. **Recommend decision** (Adopt/Adapt/Investigate/Reject/Archive)
8. **Document reasoning**

### When Evaluating AI Coding Practices

1. **Check if it's from Anthropic official sources** (Tier 1)
2. **If not, verify against Anthropic principles**
3. **Look for evidence/research backing**
4. **Test against established knowledge**:
   - `claude.md` (project rules)
   - `CONTEXT_ENGINEERING_GUIDE.md`
   - `AGENT_SKILLS_GUIDE.md`
   - `decisions.md`
5. **Assess practical value**
6. **Make recommendation**

### When User Asks "Should we use this?"

1. **Ask clarifying questions**:
   - Where did you find this?
   - What problem does it solve?
   - Why are you interested in it?
2. **Apply full validation framework**
3. **Provide reasoned recommendation**
4. **Suggest how to integrate if adopting**
5. **Document decision if implemented**

## Sources of Truth (Your Hierarchy)

### Tier 1: Ground Truth (Absolute Authority)
- Anthropic Context Engineering research paper
- Anthropic Agent Skills documentation
- Claude Code official documentation
- Anthropic API documentation

### Tier 2: Your Implementation Standards
- `claude.md` - Your project rules and preferences
- `CONTEXT_ENGINEERING_GUIDE.md` - Your context engineering standards
- `AGENT_SKILLS_GUIDE.md` - Your skills implementation standards
- `decisions.md` - Your documented architectural decisions

### Tier 3: External Validation
- New information must not contradict Tier 1
- New information should align with Tier 2
- Exceptions only with strong evidence and documented reasoning

## Validation Output Format

When evaluating content, provide:

```markdown
## Validation Report

### Source Information
- **Title**: [Content title]
- **Author**: [Who created it]
- **Source Tier**: [1-4]
- **Date**: [When published]
- **Type**: [Blog/Video/Paper/Tutorial/etc]

### Key Claims Extracted
1. [Claim 1]
2. [Claim 2]
3. [Claim 3]

### Validation Results

#### Authority Check
- [Assessment of source credibility]

#### Evidence Check
- [Assessment of backing research/data]

#### Consistency Check
- ✅ Aligns with: [List sources of truth]
- ⚠️ Partially conflicts with: [List conflicts]
- ❌ Contradicts: [List contradictions]

#### Practical Check
- **Value**: [What problem does it solve?]
- **Cost**: [Implementation effort]
- **Benefit**: [Expected improvement]

#### Recency Check
- [Is it current? Superseded?]

### Bias Assessment
- [Any detected biases in source or evaluation]

### Recommendation
- **Decision**: [ADOPT/ADAPT/INVESTIGATE/REJECT/ARCHIVE]
- **Reasoning**: [Why this decision]
- **Action Items**: [What to do next]
- **Integration Notes**: [How to implement if adopting]

### Documentation
- [Where to record this decision if adopting]
- [Updates needed to existing docs]
```

## Integration with Existing Workflow

### Before Adopting New Information

1. **Activate this skill**
2. **Run validation framework**
3. **Document in `decisions.md`** if adopting
4. **Update relevant guides** if changing standards
5. **Test in practice**
6. **Iterate based on results**

### Continuous Validation

- **Re-validate periodically** as sources of truth update
- **Document when Tier 1 sources change** (new Anthropic research)
- **Update implementation** when ground truth evolves
- **Maintain consistency** across all project documentation

## Success Metrics

This skill is working when:
- ✅ No contradictions between adopted practices and sources of truth
- ✅ Clear documented reasoning for all decisions
- ✅ Systematic evaluation process followed
- ✅ Biases identified and mitigated
- ✅ High-quality information adopted, low-quality rejected
- ✅ Confidence in implementation decisions

## Related Files

- [source-hierarchy.md](source-hierarchy.md) - Detailed source tier definitions
- [validation-checklist.md](validation-checklist.md) - Step-by-step validation process
- [decision-matrix.md](decision-matrix.md) - How to decide adopt/adapt/reject
- [bias-detection.md](bias-detection.md) - Common cognitive biases to watch for

## Notes

- This skill protects against misinformation and poor practices
- First principles thinking over cargo culting
- Evidence-based over opinion-based
- Systematic over ad-hoc
- Documented over assumed
- Question everything, validate systematically
