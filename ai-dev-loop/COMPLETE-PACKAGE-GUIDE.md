# AI Development Loop — Complete Package Guide

## Overview

This is the **full original structure** of the AI Development Loop skill, including:

- The skill definition with complete rules and procedures
- The coordination directory structure (`.ai-dev-loop/`)
- Example review, response, and context records showing the R/K loop in action
- Development status and decision history

## What's Included

### Root Files

**`SKILL.md`** (23 KB)
- The complete skill definition for dual-role AI development
- Full reference documentation for R and K roles
- Context compression rules
- Quality gates, validation procedures, and failure handling
- Git discipline and commit patterns

**`README.md`**
- Overview of the coordination directory
- Roles and responsibilities
- Git requirements
- Context policy for R and K roles

**`status.md`**
- Current development status
- Latest R review and K response
- Approval state (spec review and implementation review)
- Completed items and next steps
- Active blockers

### Example Review/Response Records

These files show the skill being **improved by itself** through the R/K loop. They're examples of how the system works:

#### Round 1: Bootstrap
- **`reviews/`** - (no R review 0001; starts with K bootstrap)
- **`responses/0001-k-response.md`** - K bootstraps the coordination directory and addresses R's implicit concerns

#### Round 2: Role-Local Markdown & Context Compression
- **`reviews/0002-r-review.md`** - R identifies gaps: missing every-round markdown requirement, stale chat context risk, no context compression, ambiguous boundaries
- **`responses/0002-k-response.md`** - K resolves all findings: adds durable markdown requirement, role-local context rules, integrates context compressor, encodes circuit breaker defaults
- **`context/0002-context.md`** - Compact summary of goals, decisions, and next actions

#### Round 3: Direct Repository Asset Modification
- **`reviews/0003-r-review.md`** - R clarifies: K must edit actual repository source files, not just artifacts
- **`responses/0003-k-response.md`** - K adds the direct asset modification rule
- **`context/0003-context.md`** - Compact summary of this decision

### Directory Structure

```
.ai-dev-loop/
├── README.md                    # Coordination guide
├── SKILL.md                     # The skill definition
├── status.md                    # Current status and approval state
├── reviews/
│   ├── 0002-r-review.md        # R's second review
│   └── 0003-r-review.md        # R's third review
├── responses/
│   ├── 0001-k-response.md      # K's bootstrap response
│   ├── 0002-k-response.md      # K's response to R review 0002
│   └── 0003-k-response.md      # K's response to R review 0003
├── context/
│   ├── 0002-context.md         # Compact context after round 2
│   └── 0003-context.md         # Compact context after round 3
└── decisions/
    # (Empty in this version; would contain escalated decisions and blockers)
```

## How to Use This Package

### Option 1: Install as a Skill

1. Copy `SKILL.md` to your Claude Code skills directory:
   ```bash
   cp SKILL.md ~/.claude/skills/ai-dev-loop-SKILL.md
   ```

2. In a new project, activate the skill:
   ```bash
   claude --skill ai-dev-loop <project-path>
   ```

3. The skill will create its own `.ai-dev-loop/` directory and begin the R/K loop.

### Option 2: Use as a Template for Your Project

1. Copy the entire `.ai-dev-loop/` directory structure to your project root:
   ```bash
   cp -r .ai-dev-loop /path/to/your/project/
   ```

2. Update `status.md` with your project's current focus and specs.

3. Start the first R review of your project.

### Option 3: Extract and Install the Archive

```bash
tar -xzf ai-dev-loop-complete.tar.gz
cd .ai-dev-loop
# Review the examples or copy to your project
```

## Understanding the Examples

The included review/response records show how the skill improves itself. This demonstrates:

### How R Reviews Work

**`0002-r-review.md`** shows R:
- Reading the skill specification carefully
- Identifying gaps (missing markdown requirement, stale context risk)
- Rating severity and type
- Asking for specific changes
- Recording findings with references to exact locations

### How K Responds

**`0002-k-response.md`** shows K:
- Reading each finding completely
- Updating the spec to address the issues
- Recording what was changed and why
- Validating with manual review
- Committing changes locally

### Compact Context

**`0002-context.md`** and **`0003-context.md`** show the integrated Context Compressor:
- Goal and current state
- Key decisions made
- Files changed
- Validation summary
- Next action
- Any risks or blockers

## Key Concepts Demonstrated

### 1. Durable Markdown Records

Everything R and K decide is **recorded in committed markdown**. This creates an audit trail and prevents decisions from disappearing into chat history.

### 2. Role Separation

Even though this is one AI improving its own skill, **R and K maintain strict separation**:
- R's findings are in `reviews/`
- K's responses are in `responses/`
- Each has its own sections of `status.md`

This keeps the process clear and auditable.

### 3. Local Git Commits

Every meaningful change is committed:
```
R: audit specs for role-local markdown
K: respond to role-local markdown review
K: update SKILL.md with context compression rules
R: approve role-local markdown and context compression
```

You can see the full history:
```bash
git log --oneline -n 10
```

### 4. Compressed Communication

The `context/` files show how to keep records brief and focused:
- State the goal
- Record decisions
- List changed files
- Summarize validation
- Identify next action
- Note any risks

This reduces token usage without losing information.

### 5. Escalation When Needed

If R and K disagree or need human guidance, they write a blocker file and stop. They don't keep arguing indefinitely.

## Installing for Claude Code

### Prerequisites

- Claude Code installed
- Git available in your development environment
- A project with specifications, implementation plans, or roadmaps

### Installation Steps

1. **Copy the skill file:**
   ```bash
   cp SKILL.md ~/.claude/skills/ai-dev-loop-SKILL.md
   ```

2. **Initialize your project with the skill:**
   ```bash
   cd /path/to/your/project
   claude --skill ai-dev-loop .
   ```

3. **Provide project context:**
   - Include your specs, roadmap, or tickets
   - Point Claude to the relevant files
   - Optionally copy the example `.ai-dev-loop/` structure

4. **Start the first R review:**
   ```
   User: "Please audit our API specification and implementation plan"
   ```

Claude will:
- Create R's first review
- Commit it to git
- Continue the R/K loop autonomously
- Create all necessary markdown records

## What to Expect

### First Round (R Review 1)
R audits your specs and plans, identifies risks, gaps, and assumptions.

### Second Round (K Response 1)
K addresses R's findings by updating specs, adding clarifications, or preparing implementation.

### Subsequent Rounds
R re-reviews, K refines, until R approves.

### Then: Implementation
Once specs are approved, K proceeds with actual code implementation while maintaining the review loop.

## Customization

### Rename the Skill
If installing with a different name:
```bash
cp SKILL.md ~/.claude/skills/my-ai-dev-loop-SKILL.md
```

### Use a Custom Coordination Directory
If your project already has an ADR or decision log directory, update `.ai-dev-loop/README.md` to point to it.

### Adjust Context Compression
The skill defaults to compressed markdown. You can request verbose mode, but compressed is recommended for token efficiency.

### Circuit Breaker Thresholds
Default is 6 rounds per item before escalating. You can adjust in `SKILL.md` if needed.

## Troubleshooting

### "Cannot find the skill"
- Verify the file is in `~/.claude/skills/`
- Check the filename matches what you're trying to load
- Restart Claude Code

### "Git not initialized"
- The skill will create `.git` automatically if it can
- If git isn't available, the skill will create a blocker

### "Too many review rounds"
- Check `.ai-dev-loop/decisions/` for blocker notes
- Read the last R review and K response
- Escalate the stuck decision to a human

### "Changes not committed"
- Verify you're on the correct branch: `git branch`
- Check git status: `git status --short`
- Review the last few commits: `git log --oneline -n 5`

## File Manifest

All files needed to run the skill:

### Installation
```
SKILL.md                 — The skill definition
README.md                — Coordination guide
status.md                — Current status
```

### Examples (for reference)
```
reviews/0002-r-review.md         — Example R review
reviews/0003-r-review.md         — Example R review

responses/0001-k-response.md     — Example K response
responses/0002-k-response.md     — Example K response
responses/0003-k-response.md     — Example K response

context/0002-context.md          — Example compact context
context/0003-context.md          — Example compact context

decisions/                        — (Empty; would contain blockers)
```

### Optional
```
ai-dev-loop-complete.tar.gz      — Full compressed archive
ai-dev-loop-SKILL.md             — Alternate naming for the skill
INSTALLATION.md                  — Installation guide
```

## Next Steps

1. **Choose your installation method** (skill in `.claude/skills/` or project template)
2. **Provide your project context** (specs, roadmap, code)
3. **Start the first R review** (ask Claude to audit your specs)
4. **Watch the R/K loop** (check `.ai-dev-loop/` for records)
5. **Let it run autonomously** (R and K handle the review cycle)
6. **Intervene only when escalated** (circuit breaker or human decision needed)

---

**Ready to use?** Start with:
```bash
cp SKILL.md ~/.claude/skills/ai-dev-loop-SKILL.md
```

Then run:
```bash
claude --skill ai-dev-loop /path/to/project
```

**Questions?** Check the example reviews and responses to understand the process flow.

---

**Version**: 1.0  
**Complete Package** — Includes skill definition, coordination files, example records, and guides  
**Created**: 2026-06-14
