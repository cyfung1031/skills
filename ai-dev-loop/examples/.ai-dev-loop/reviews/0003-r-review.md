# R Review 0003: Direct repository asset modification rule

## Scope

Reviewed user clarification: when K is ready to write code or modify project source files after an approved spec, K should directly modify actual source code files in the repository workspace and make the local Git commit.

## Summary

Changes requested. The skill must explicitly prefer direct repository working-tree modification over detached artifact staging once the relevant spec or plan is approved.

## Findings

### Finding R-0003-01: Implementation target must be the real repository workspace

- Severity: High
- Type: Process issue
- Location: Core Principles; Role K; Phase 2 Implementation; Quality Gates
- Details: The skill previously required local commits but did not explicitly state whether K should edit the actual repository source files or stage changes in generated artifacts first. The user clarified the correct behavior is direct modification of repository source files followed by a local commit.
- Required action: Add a direct asset modification rule: after approved spec/plan, K modifies actual repo files in place, validates the real working tree, and commits locally on the same branch. Artifact-only staging or detached copies are not the implementation target unless explicitly required.

## Clarifications Needed

None. User answered yes to direct modification.

## Approval Status

Changes requested.

## Next Expected K Action

Update `SKILL.md`, mirror it to `.ai-dev-loop/SKILL.md`, update status/context, and commit the changes locally.
