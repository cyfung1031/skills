# AI Development Loop Coordination

This directory is the durable coordination area for the dual-role software development loop.

## Location

The coordination directory is located at the workspace root as `.ai-dev-loop/`.

## Roles

- R records reviews, audits, approval status, and clarification needs in `reviews/`.
- K records responses, spec updates, implementation notes, and validation results in `responses/`.
- Durable decisions and human-escalation blockers are recorded in `decisions/`.
- Compact role-local state summaries are recorded in `context/`.

## Git Requirement

Normal operation requires local git commits on the current working branch. If the workspace is not already a git repository, initialize git at the workspace root during bootstrap.

## Context Policy

R and K must reload state from durable files and git history each turn. Chat context is not authoritative unless copied into committed `.ai-dev-loop/` markdown.
