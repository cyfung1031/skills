---
name: github-issue-fix-planner
description: Analyze a GitHub issue and its related source-code repository to identify the likely failure boundary, infer the root cause, map the problem to relevant files, and produce practical code-fix suggestions with patch templates, regression tests, commit text, and PR-ready messaging.
Version: 1.0.0
---

## Purpose

Convert a GitHub issue and a related source-code repository into a practical, review-ready engineering proposal.

The output should help a contributor or maintainer move from:

```text
A user-visible bug report
```

to:

```text
A likely root cause, concrete source-code fix direction, test plan, commit message, and PR body
```

This skill is designed for generic GitHub issues across frontend, backend, CLI, browser, library, build, packaging, integration, and platform-specific projects.

---

# 1. Inputs

## Required

```text
Issue URL:
Source repository URL:
```

## Optional but useful

```text
Related issues:
Related PRs:
Affected version:
Known working version:
Known broken version:
Operating system:
Runtime / browser / framework:
Logs:
Stack trace:
Screenshots:
Minimal reproduction:
Local reproduction notes:
Expected behavior:
Actual behavior:
Known workaround:
User’s intended target repository:
```

## Important distinction

Sometimes the issue is filed in one repository, but the real fix belongs in another.

Always distinguish:

```text
Reporter repository:
Repository where symptom is observed:

Fix target repository:
Repository where source-code change should likely be made:

Downstream workaround:
A local mitigation in the affected app/project:

Upstream/root fix:
A fix in the component that actually owns the failing behavior:
```

---

# 2. Core Principle

Do not jump from symptom directly to patch.

First find the **failure boundary**.

The failure boundary is the earliest point where the system stops behaving as expected.

Ask:

```text
What action starts the flow?
Which code receives it?
Which rule/config/request/event/job is created?
Does registration succeed?
Does matching succeed?
Does validation succeed?
Does the selected action execute?
Does the result commit, render, persist, or return?
Where does expected behavior first become broken behavior?
```

The best code fix usually belongs at that boundary.

---

# 3. Investigation Workflow

## Step 1: Read the issue fully

Extract:

```text
Issue title:
Issue body:
Reproduction steps:
Expected behavior:
Actual behavior:
Affected versions:
Unaffected versions:
Affected platforms:
Labels:
Assignees:
Maintainer comments:
Reporter comments:
Related issues:
Related PRs:
Logs:
Screenshots:
Attachments:
Known workaround:
```

Then summarize:

```text
Symptom:
Trigger:
Expected:
Actual:
Environment:
Regression window:
Workaround:
Maintainer hints:
```

---

## Step 2: Separate facts from hypotheses

Use these categories.

```text
Confirmed:
Directly supported by issue text, comments, logs, tests, screenshots, or source code.

Likely:
Strongly suggested by the evidence and architecture.

Speculative:
Possible, but not proven without reproduction, build, or deeper source inspection.

Needs verification:
Requires running the project, executing tests, checking generated files, or confirming runtime state.
```

Never present speculative code changes as certain.

---

## Step 3: Identify the failing boundary

Classify the failing layer.

```text
UI event handling
Client-side routing
State management
API request construction
Server routing
Controller / handler logic
Validation
Authentication
Authorization
Permission checks
Configuration loading
Rule registration
Rule matching
Action execution
Redirect handling
Navigation handling
File handling
Download handling
Serialization
Parsing
Database persistence
Cache invalidation
Queue processing
Background job execution
Scheduler / timer behavior
Platform adapter
OS integration
Browser/runtime integration
Third-party dependency behavior
Build step
Packaging step
Release artifact generation
Feature flag / experiment gating
```

Write:

```text
Working path:
Failing path:
Difference:
Likely failing boundary:
```

A strong diagnosis explains both the broken behavior and any workaround.

---

## Step 4: Search the source repository

Search using issue-specific terms:

```text
API names
error messages
class names
function names
route names
file extensions
protocols
config keys
feature flags
permission names
test names
related issue IDs
known workaround APIs
platform names
```

Search broadly first, then narrow.

Useful search patterns:

```text
"<exact error message>"
"<API name>"
"<feature flag>"
"<route path>"
"<permission name>"
"<file extension>"
"<workaround function>"
"<affected component>"
```

---

## Step 5: Map source ownership

For each candidate file, record:

```text
File:
Relevant symbols:
Why this file matters:
Likely role:
Confidence:
```

Prioritize files containing decision points:

```text
allow / block
match / no match
validate / reject
redirect / continue
download / render
serialize / parse
enqueue / execute
commit / rollback
fallback / fail
```

---

## Step 6: Inspect repository contribution style

Before suggesting patches, inspect how the repository expects changes.

Look for:

```text
CONTRIBUTING.md
PR template
issue template
test directory structure
existing tests for the same component
feature flags
build files
generated files
patch directories
source override directories
platform-specific adapters
lint rules
formatting conventions
error-handling conventions
naming conventions
```

For forked, vendored, or patched repositories, determine whether the fix belongs in:

```text
direct source file
patch file
overlay file
wrapper layer
generated file source
platform adapter
upstream dependency
downstream workaround
```

Do not assume direct source edits are acceptable if the repository uses patch generation, vendoring, or overlays.

---

## Step 7: Compare similar working code

Find nearby working examples.

Search for:

```text
similar API usage
similar validation logic
similar permission check
similar route handler
similar redirect logic
similar platform adapter
similar fallback behavior
similar test fixture
```

Record:

```text
Existing pattern:
Where used:
How the failing path differs:
What should be reused:
```

Prefer fixes that follow established local patterns.

---

# 4. Root-Cause Rules

A useful root cause should explain:

```text
Why the symptom happens
Why expected behavior does not happen
Why the workaround works
Why only certain versions/platforms/configurations are affected
Which source layer owns the behavior
Why the proposed patch fixes the failing layer
```

Use cautious phrasing:

```text
The likely root cause is...
The failure boundary suggests...
The strongest candidate is...
This should be verified by...
```

Avoid overclaiming:

```text
This is definitely caused by...
The only possible cause is...
```

unless logs, source code, or tests prove it.

---

# 5. Fix Design Rules

A practical fix should be:

```text
narrow
reviewable
testable
consistent with existing architecture
safe for unrelated behavior
easy to revert
covered by regression tests
```

Avoid broad fixes:

```text
Disable validation globally
Allow all callers
Ignore all errors
Catch and suppress exceptions without logging
Bypass authorization
Remove feature gating
Skip security checks
Change unrelated public behavior
```

Prefer guarded fixes:

```text
Allow only trusted callers
Allow only owned targets
Retry only idempotent operations
Fallback only for known failing platform/version/configuration
Preserve validation for unrelated cases
Preserve existing security checks
Log unexpected fallback usage
Add explicit tests for both allow and reject cases
```

---

# 6. Patch Confidence Labels

Use these labels for each patch.

```text
High confidence:
The file and branch are clearly responsible, and the change follows existing code patterns.

Medium confidence:
The file is likely responsible, but exact insertion point requires local source inspection.

Low confidence:
The patch is a directional pseudocode proposal requiring maintainer validation.

Needs verification:
Requires build, runtime reproduction, generated-code update, or test execution before submission.
```

---

# 7. Patch Set Format

Each patch suggestion should include:

```text
Patch number:
Name:
File:
Purpose:
Insertion point:
Suggested diff or pseudocode:
Why it fixes the issue:
Risks:
Test coverage:
Confidence:
```

When exact line numbers are unknown, describe insertion points by logic:

```text
Place before the branch that returns BLOCK/REJECT.
Place after parsing and before validation.
Place where a matched rule is converted into an action.
Place before fallback/error/download creation.
Place inside the affected platform adapter.
Place next to the existing working pattern.
```

---

# 8. Test Design

Always propose at least two tests.

## Positive regression test

Proves the reported case now works.

```text
Test name:
Setup:
Action:
Expected result:
Why it fails before patch:
Why it passes after patch:
```

## Negative safety test

Proves unrelated invalid or blocked behavior remains blocked.

```text
Test name:
Setup:
Action:
Expected result:
Why this matters:
```

Optional additional tests:

```text
Compatibility test:
Known working path still works.

Platform test:
Affected platform-specific behavior is covered.

Regression-window test:
Known fixed/broken version behavior is captured where feasible.

Unit test:
Decision logic is covered directly.

Integration test:
Full user-visible flow is covered.
```

---

# 9. Final Response Template

Use this structure when producing the engineering package.

---

## Root-cause issue title

```text
<clear title focused on the failing boundary>
```

---

## Root-cause issue description

```markdown
### Summary

<user-visible failure>

### Expected behavior

<expected result>

### Actual behavior

<actual result>

### Reproduction

1. <step>
2. <step>
3. <step>

### Impact

<affected users/workflows>

### Confirmed observations

- <fact>
- <fact>
- <fact>

### Likely failing boundary

<where behavior diverges>

### Suggested fix direction

<high-level implementation direction>
```

---

## Confirmed observations

```markdown
- <confirmed observation>
- <confirmed observation>
- <confirmed observation>
```

---

## Likely root cause

````markdown
The issue appears to be caused by <component/layer> incorrectly handling
<operation/edge case>.

Failing path:

```text
<input/action>
  -> <intermediate step>
  -> <broken step>
````

Working path:

```text
<input/action>
  -> <alternative step>
  -> <success>
```

This suggests the fix should be applied in <file/component>, where
<decision/action> is made.

````

---

## Files to inspect or change

```text
<path 1>
Reason: <why relevant>
Confidence: <high/medium/low>

<path 2>
Reason: <why relevant>
Confidence: <high/medium/low>

<path 3>
Reason: <why relevant>
Confidence: <high/medium/low>
````

---

## Patch set

### Patch 1: <name>

File:

```text
<path>
```

Purpose:

```text
<why this patch exists>
```

Insertion point:

```text
<where to place it>
```

Suggested change:

```diff
<diff or pseudocode>
```

Why this fixes the issue:

```text
<explanation>
```

Risks:

```text
<possible side effects>
```

Confidence:

```text
<high/medium/low/needs verification>
```

---

### Patch 2: <name>

File:

```text
<path>
```

Purpose:

```text
<why this patch exists>
```

Insertion point:

```text
<where to place it>
```

Suggested change:

```diff
<diff or pseudocode>
```

Why this fixes the issue:

```text
<explanation>
```

Risks:

```text
<possible side effects>
```

Confidence:

```text
<high/medium/low/needs verification>
```

---

## Regression tests

### Positive test

```text
Name:
<test name>

Setup:
<fixture/setup>

Action:
<operation>

Expected:
<expected result>

Fails before patch because:
<reason>

Passes after patch because:
<reason>
```

### Negative test

```text
Name:
<test name>

Setup:
<fixture/setup>

Action:
<operation>

Expected:
<blocked/unchanged behavior>

Why this matters:
<security or compatibility reason>
```

---

## Commit title

```text
<imperative title, preferably under 72 chars>
```

---

## Commit message

```text
<commit title>

<why the change is needed>

<what the change does>

<why the change is safe/narrow>

<tests added>
```

---

## PR title

```text
<PR title>
```

---

## PR body

```markdown
## Summary

<what this fixes>

## Root cause

<likely root cause>

## Fix

<what changed>

## Safety

<why this does not broaden unrelated behavior>

## Test plan

- <test>
- <test>
- <manual verification>

## Related issues

- <issue URL>
```

---

## Confidence and uncertainty

```markdown
### High confidence

- <items directly supported by evidence>

### Medium confidence

- <items inferred from source structure>

### Needs verification

- <items requiring local reproduction, build, or test run>
```

---

# 10. Review Checklist

Before finalizing, verify:

```text
The root cause explains the symptom.
The root cause explains the workaround.
The failure boundary is explicit.
The target files are tied to the failure boundary.
The repository’s patch/contribution style is respected.
The patch is narrow.
The patch does not disable unrelated validation/security.
The positive test fails before the patch.
The positive test passes after the patch.
The negative test protects existing behavior.
The commit title is imperative.
The PR body is understandable to maintainers.
Uncertain parts are labeled.
```

---

# 11. Anti-Patterns

Avoid:

```text
Summarizing the issue without source-code fix suggestions.
Suggesting only a downstream workaround when the user asked for root fix.
Giving a broad fix that weakens validation/security.
Inventing exact line numbers without source evidence.
Ignoring issue comments that already narrow the failure.
Ignoring existing repository patch style.
Failing to distinguish confirmed facts from hypotheses.
Producing a PR message without tests.
Overfitting a generic bug to one downstream app.
Assuming the issue repo and fix repo are the same.
```

---

# 12. Revision History

## v1.1.0

Added:

```text
explicit failure-boundary analysis
reporter repo vs fix target repo distinction
repository patch-style inspection
confidence labels for files and patches
positive and negative regression test requirements
safer patch design rules
clear final response contract
stronger separation of facts, likely causes, and speculation
support for fork/downstream/upstream source layouts
anti-pattern checklist
```

## v1.2.0

Added:

```text
source ownership mapping
working-path vs failing-path comparison
decision-point prioritization
logic-based insertion points when exact line numbers are unknown
test failure/pass rationale
```

## v1.3.0

Added:

```text
repository contribution-style inspection before patching
explicit handling for generated files, overlays, forks, and vendored code
patch confidence labels
optional compatibility, platform, unit, and integration tests
```

## v1.4.0

Added:

```text
converged final output contract
clearer input distinction between reporter repo and fix repo
stronger safety language for guarded fixes
cleaner review checklist
more general bug-layer taxonomy
reduced project-specific assumptions
```

---

# 13. Convergence Note

This version is intentionally generic. Further useful improvements would usually be domain-specific, such as separate variants for:

```text
browser engine bugs
React frontend bugs
backend API bugs
database migration bugs
compiler/toolchain bugs
mobile platform bugs
security-sensitive auth bugs
CI/build failures
```

For a general GitHub issue-to-code-fix skill, v1.4.0 has reached a practical point of diminishing returns.
