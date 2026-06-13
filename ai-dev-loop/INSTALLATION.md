# AI Development Loop Skill — Installation Guide

## Overview

The **AI Development Loop** skill enables Claude Code to manage autonomous software development through a dual-role review and implementation system. It establishes a durable workflow between two AI roles (Reviewer/Auditor and Implementer/Keeper) that can drive development without constant human intervention.

## Installation Steps

### Step 1: Copy the SKILL.md File

1. Download or locate `ai-dev-loop-SKILL.md`
2. Copy it to your Claude Code skills directory:
   
   **macOS/Linux:**
   ```bash
   ~/.claude/skills/ai-dev-loop-SKILL.md
   ```
   
   **Windows:**
   ```
   %USERPROFILE%\.claude\skills\ai-dev-loop-SKILL.md
   ```

3. Alternatively, if Claude Code has a skills management UI, upload the file through that interface.

### Step 2: Verify Installation

In Claude Code, run:
```bash
claude skills list
```

You should see `ai-dev-loop` listed among available skills.

### Step 3: Bootstrap Your Project

When you activate this skill in a project, Claude will automatically:

1. Check for existing `.ai-dev-loop/` coordination directory
2. Create the directory structure if needed:
   ```
   .ai-dev-loop/
     README.md
     reviews/
     responses/
     decisions/
     context/
     status.md
   ```
3. Initialize git (if not already a git repo)
4. Set up the first status file

## Using the Skill

### Quick Start

1. Activate the skill in Claude Code:
   ```bash
   claude --skill ai-dev-loop <your-project-path>
   ```

2. Provide your project context:
   - Specifications or requirements documents
   - Implementation roadmap or ticket list
   - Existing code (optional)

3. Claude will begin the R/K loop:
   - **R** reviews specs and plans
   - **K** responds to findings and implements changes
   - Both roles write durable markdown records
   - All changes are committed to git

### Example Workflow

```
User: "Review the user authentication spec and plan implementation"
           ↓
[R Review 0001: Creates review of auth spec → commits]
           ↓
[K Response 0001: Addresses findings, updates specs → commits]
           ↓
[R Review 0002: Re-reviews updated spec and implementation → commits]
           ↓
[K Response 0002: Implements remaining changes → commits]
           ↓
[R Approval: "Approved with notes"]
           ↓
Development continues to next item
```

### Key Directories and Files

**`.ai-dev-loop/reviews/`**
- Contains R's review findings, severity levels, and approval decisions
- Files: `NNNN-r-review.md` (e.g., `0001-r-review.md`)

**`.ai-dev-loop/responses/`**
- Contains K's responses, spec updates, implementation details, and validation results
- Files: `NNNN-k-response.md` (e.g., `0001-k-response.md`)

**`.ai-dev-loop/decisions/`**
- Contains decisions, circuit breaker notes, and human escalations
- Files: `NNNN-decision.md` or `NNNN-blocker.md`

**`.ai-dev-loop/status.md`**
- Single source of truth for current focus, approval state, and blockers
- Updated by both roles after each review or response

### Git Integration

The skill enforces strict git discipline:

- Every R review → commit
- Every K response → commit
- Every implementation change → commit
- Every test → commit

All changes are committed to the **current local branch**. You can review the entire development history:

```bash
git log --oneline -n 20
```

## Configuration

### Workspace Requirements

- **Git repository**: The skill requires git. It will initialize if needed.
- **Specs or roadmap**: Provide at least a basic roadmap, specification, or ticket list
- **Test infrastructure**: Recommended (npm test, pytest, cargo test, etc.)

### Optional Customization

You can customize the skill by:

1. **Using an existing coordination directory**: If your project already has an ADR, decision log, or review directory, document its location in `.ai-dev-loop/README.md`

2. **Custom commit prefixes**: The skill suggests `R:` and `K:` prefixes. You can modify these in your project workflow.

3. **Compressed context mode**: The skill defaults to compressed records (short, focused markdown). Disable this by asking Claude to use verbose mode (not recommended for token efficiency).

## Advanced Features

### Circuit Breaker

If the R/K loop diverges (too many rounds, repeated disagreements, or no progress), the skill triggers a circuit breaker:
- Creates `.ai-dev-loop/decisions/NNNN-blocker.md`
- Documents the decision needed
- Stops for human input

### Autonomous Clarification

K can resolve R's clarifications without human input by consulting:
- Project specs and roadmaps
- Implementation plans
- Existing code and tests
- README or developer documentation
- Prior R/K records

Only escalates to humans when the decision could cause safety, security, compliance, or data-loss risk.

### Quality Gates

Before R approval, the skill verifies:
- Specs and code align
- All findings are addressed (or explicitly deferred)
- Tests are added/updated
- Commands and results are recorded
- Implementation is on the actual repository working tree
- Git history is clean and traceable

## Troubleshooting

### "Cannot create .ai-dev-loop/ directory"
- Ensure the repository root is writable
- Check git permissions

### "Git commands failing"
- Verify git is installed and the project is a git repository
- Run `git status` to check for merge conflicts or detached HEAD

### "Too many R/K loops without approval"
- The skill will trigger a circuit breaker after 6 rounds
- Check the blocker file (`.ai-dev-loop/decisions/`) to understand the stuck point
- Escalate to the human with full context

### "Validation/test commands failing"
- K will document whether failures are from its changes or pre-existing
- R requires clean validation or explicit evidence that failures are unrelated before approving

## Support and Feedback

If you encounter issues or want to improve the skill:

1. Check the `.ai-dev-loop/` records for detailed R/K feedback
2. Review the git log to understand the development history
3. Consult the human escalation guide in the skill documentation

## Additional Resources

- **Skill SKILL.md**: Full reference documentation
- **.ai-dev-loop/README.md**: Generated project-specific coordination guide
- **.ai-dev-loop/status.md**: Current development status and approval state
- **Git history**: Run `git log --oneline` for the complete record of R/K decisions

---

**Version**: 1.0  
**Last Updated**: 2026-06-14
