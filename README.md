# skills

Reusable skills, instructions, guidelines, and knowledge bundles for AI coding agents such as Claude Code, Codex, and similar agentic development tools.

This repository is a personal library of operating procedures. Each folder is meant to teach an agent **how to behave**, **what to read**, **what evidence to preserve**, and **how to execute a repeatable workflow**.

## What is in this repo?

This repo contains several kinds of material:

| Area                                         | Purpose                                                                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [`#INSTRUCTIONS`](./%23INSTRUCTIONS)         | Agent-specific instruction files, such as Claude Code and Codex configuration/instruction material.                                      |
| [`#KNOWLEDGE-SKILLS`](./%23KNOWLEDGE-SKILLS) | Knowledge bundles and zipped reference material that can be loaded alongside a skill.                                                    |
| [`GUIDELINES`](./GUIDELINES)                 | Standalone guidelines, examples, and operating notes that are useful across projects.                                                    |
| Skill folders                                | Reusable workflows. Most have a `SKILL.md` as the main entry point. Some include modules, scripts, templates, examples, or package docs. |
| [`LICENSE`](./LICENSE)                       | MIT license.                                                                                                                             |

The top-level skill folders include workflows for governance, concise execution, coding-agent behavior, development loops, review, benchmarking, scaffolding, context compression, version building, GitHub issue planning, visualization, and domain-specific agent workflows.

## How to read this repo

Start with the kind of thing you want the agent to do.

### 1. First: choose the operating mode

Before choosing a task-specific skill, decide how the agent should behave.

For most tasks, start with one of these:

1. [`cogniact-governor`](./cogniact-governor)
2. [`high-signal-mode`](./high-signal-mode)
3. [`core-coding-agent-behavior`](./core-coding-agent-behavior)

Use `cogniact-governor` when you want stronger governance, careful decisions, controlled execution, and higher discipline.

Use `high-signal-mode` when you want concise, high-density output with less chatter and more useful action.

Use `core-coding-agent-behavior` when the task involves code inspection, implementation, validation, or repository-safe execution.

A common default stack is:

```text
Use these skills in this order:

1. cogniact-governor as the top-level control and decision discipline.
2. high-signal-mode for concise, high-signal execution.
3. core-coding-agent-behavior for safe repository work.
4. The relevant task-specific skill.

Task:
[describe the task here]
```

### 2. For general agent setup

Read the agent-specific instruction files next:

* Claude Code: [`#INSTRUCTIONS/Claude`](./%23INSTRUCTIONS/Claude)
* Codex: [`#INSTRUCTIONS/Codex`](./%23INSTRUCTIONS/Codex)

Use these when you want to configure a coding agent’s default behavior before giving it a project-specific task.

### 3. For a reusable workflow

Open the relevant skill folder and read:

1. `README.md`, if present, for the human-facing overview.
2. `SKILL.md` for the agent-facing operating procedure.
3. Any `modules/`, `templates/`, `examples/`, or `scripts/` only when the `SKILL.md` or task requires them.

In most skill folders, `SKILL.md` is the file the agent should treat as the primary instruction source.

### 4. For project documentation workflows

Start with:

* [`project-scaffolding-and-docs/README.md`](./project-scaffolding-and-docs/README.md)
* [`project-scaffolding-and-docs/SKILL.md`](./project-scaffolding-and-docs/SKILL.md)
* [`project-scaffolding-and-docs/setup.md`](./project-scaffolding-and-docs/setup.md)

This skill is useful when starting or reorganizing a project’s durable documentation: `README`, `SPEC`, roadmap, release plans, engineering notes, changelog, and decision records.

### 5. For review/implementation loops

Start with:

* [`ai-dev-loop/README.md`](./ai-dev-loop/README.md)
* [`ai-dev-loop/SKILL.md`](./ai-dev-loop/SKILL.md)
* [`ai-dev-loop/QUICKSTART.md`](./ai-dev-loop/QUICKSTART.md)
* [`ai-dev-loop/INSTALLATION.md`](./ai-dev-loop/INSTALLATION.md)

This workflow separates review and implementation into durable phases and stores handoff state in a target project’s `.ai-dev-loop/` directory.

`ai-dev-loop` can also work with review and domain-specific skills, especially:

* [`insightforge-reviewer`](./insightforge-reviewer) for deeper review, critique, synthesis, and quality evaluation.
* [`ponytail`](./ponytail) for specialized domain-specific work that needs to be run through a durable development loop.

### 6. For guidelines and supporting notes

Browse [`GUIDELINES`](./GUIDELINES) when you want standalone practices, examples, or policy-like guidance that can be copied into another agent setup.

## How to use a skill

A skill is usually used by loading or pasting its `SKILL.md` into the agent context, then giving the agent a concrete task.

Example prompt:

```text
Use the skill in project-scaffolding-and-docs/SKILL.md.

Task:
Review this repository’s current documentation and propose the minimum durable documentation set needed for a new contributor to start safely.
```

Another example:

```text
Use ai-dev-loop/SKILL.md.

Task:
Set up a review and implementation loop for this change. Keep all findings and validation evidence in project files, not only in chat.
```

For combined skills, give the agent a clear order:

```text
Use these skills in this order:

1. cogniact-governor as the top-level control layer.
2. high-signal-mode for concise execution.
3. core-coding-agent-behavior as the base repository behavior.
4. github-issue-fix-planner to investigate and plan the fix.
5. ai-dev-loop to implement, review, validate, and preserve evidence.
6. ai-dev-loop-sanitize-commits to clean the final commits.

Task:
Fix issue #123 without losing validation evidence.
```

## Installing or copying skills

This repo is not one single installable package. Treat it as a library.

### Copy a skill into an agent skill directory

Copy a whole skill folder, preserving its internal structure:

```bash
cp -R project-scaffolding-and-docs /path/to/agent/skills/
```

Then tell the agent to use that skill’s `SKILL.md`.

### Copy instructions into a project

For project-level agent instructions, copy or adapt files from `#INSTRUCTIONS`.

For example:

```bash
cp "#INSTRUCTIONS/Codex/AGENTS.md" /path/to/project/AGENTS.md
```

or, for Claude Code, copy/adapt:

```bash
cp "#INSTRUCTIONS/Claude/CLAUDE.md" /path/to/project/CLAUDE.md
```

Review the copied file before committing it, especially if the target project has different safety, test, privacy, or style requirements.

### Use skill-specific installers

Some skills include their own install or validation scripts. For example, `ai-dev-loop` includes installation and validation material under its folder.

Always read the skill’s own `README.md`, `INSTALLATION.md`, or `QUICKSTART.md` before running scripts.

## Recommended reading order for new users

If you are new to the repo, read in this order:

1. This `README.md`.
2. [`cogniact-governor`](./cogniact-governor), if you want governed, controlled execution.
3. [`high-signal-mode`](./high-signal-mode), if you want concise, high-density operation.
4. [`core-coding-agent-behavior`](./core-coding-agent-behavior), if the task involves code or repository changes.
5. The instruction folder for your agent:

   * `#INSTRUCTIONS/Claude` for Claude Code.
   * `#INSTRUCTIONS/Codex` for Codex.
6. One relevant task-specific skill folder.
7. That skill’s `README.md`, if present.
8. That skill’s `SKILL.md`.
9. Only then read deeper files such as `modules/`, `templates/`, `examples/`, or `scripts/`.

Avoid loading every file at once. Most skills are designed so the small entry point tells the agent when deeper material is necessary.

## Skill folder conventions

A typical skill folder may contain:

| File or folder          | Meaning                                                    |
| ----------------------- | ---------------------------------------------------------- |
| `SKILL.md`              | Main agent-facing operating instructions. Read this first. |
| `README.md`             | Human-facing overview, usage notes, and folder map.        |
| `modules/`              | Detailed procedures loaded only when needed.               |
| `templates/`            | Copyable project or workflow templates.                    |
| `examples/`             | Example state, records, prompts, or outputs.               |
| `scripts/`              | Helper scripts for installation, validation, or checks.    |
| `PACKAGE-MANIFEST.json` | Package inventory or checksums, when a skill is packaged.  |
| `VALIDATION-RESULTS.md` | Validation evidence for packaged skills.                   |

Not every skill has every file.

## How to choose a skill

Use the skill that matches the job you want the agent to perform.

Many skills can be combined. Use one or more **priority operating skills** first, then add the **primary task skill**, then add review, cleanup, or compression skills as needed.

### Priority operating skills

These should be considered first.

| Skill                                                        | Use when you need                                                                                                                 |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| [`cogniact-governor`](./cogniact-governor)                   | Top-level governance, decision discipline, controlled execution, stronger process boundaries, and safer handling of complex work. |
| [`high-signal-mode`](./high-signal-mode)                     | Concise, high-density output with less noise, fewer unnecessary explanations, and more direct execution.                          |
| [`core-coding-agent-behavior`](./core-coding-agent-behavior) | General coding-agent behavior, disciplined repo inspection, implementation hygiene, validation, and safe execution.               |

Common combinations:

| Goal                            | Combine                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------- |
| Default disciplined workflow    | `cogniact-governor` + `high-signal-mode`                                     |
| Safe coding work                | `cogniact-governor` + `core-coding-agent-behavior`                           |
| Concise but careful coding work | `cogniact-governor` + `high-signal-mode` + `core-coding-agent-behavior`      |
| High-stakes repository task     | `cogniact-governor` + `core-coding-agent-behavior` + the relevant task skill |
| Fast, low-noise review          | `high-signal-mode` + the relevant review skill                               |

### Development loops and implementation workflows

Use these when the task involves planning, implementing, reviewing, validating, or cleaning up code changes.

| Skill                                                            | Use when you need                                                                                                               |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [`ai-dev-loop`](./ai-dev-loop)                                   | A durable review/implementation loop with separate review and implementation phases, persistent state, and validation evidence. |
| [`ai-dev-loop-sanitize-commits`](./ai-dev-loop-sanitize-commits) | Cleanup, sanitize, or prepare commits produced during an AI development loop.                                                   |
| [`github-issue-fix-planner`](./github-issue-fix-planner)         | Turn a GitHub issue into an implementation plan, investigation path, or fix strategy.                                           |
| [`project-scaffolding-and-docs`](./project-scaffolding-and-docs) | Create or reorganize durable project documentation such as README, SPEC, roadmap, changelog, and contributor guidance.          |

Common combinations:

| Goal                                      | Combine                                                                     |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| Governed implementation loop              | `cogniact-governor` + `ai-dev-loop`                                         |
| Concise implementation loop               | `high-signal-mode` + `ai-dev-loop`                                          |
| Safe issue fix                            | `cogniact-governor` + `github-issue-fix-planner` + `ai-dev-loop`            |
| Issue fix with deep review                | `github-issue-fix-planner` + `ai-dev-loop` + `insightforge-reviewer`        |
| Specialized/domain workflow inside a loop | `ponytail` + `ai-dev-loop`                                                  |
| Specialized/domain workflow with review   | `ponytail` + `ai-dev-loop` + `insightforge-reviewer`                        |
| Implement, review, then clean commits     | `ai-dev-loop` + `ai-dev-loop-sanitize-commits`                              |
| Start a new project with durable docs     | `project-scaffolding-and-docs` + `core-coding-agent-behavior`               |
| Turn an issue into docs and code changes  | `github-issue-fix-planner` + `project-scaffolding-and-docs` + `ai-dev-loop` |

### Review, readability, and quality improvement

Use these when the main output is critique, evaluation, comparison, or refinement.

| Skill                                                            | Use when you need                                                                           |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`advisory-suggestions`](./advisory-suggestions)                 | Advisory comments, suggestions, and improvement notes rather than direct implementation.    |
| [`agent-readability-review`](./agent-readability-review)         | Review agent-produced output for clarity, readability, usefulness, and user-facing quality. |
| [`insightforge-reviewer`](./insightforge-reviewer)               | Deeper insight-oriented review, critique, synthesis, evaluation, and improvement planning.  |
| [`best-version-builder`](./best-version-builder)                 | Compare multiple versions and build the strongest final version.                            |
| [`variant-best-version-builder`](./variant-best-version-builder) | Generate, compare, and merge variants into a best version.                                  |

Common combinations:

| Goal                                    | Combine                                                     |
| --------------------------------------- | ----------------------------------------------------------- |
| Governed review                         | `cogniact-governor` + `insightforge-reviewer`               |
| Concise review                          | `high-signal-mode` + `agent-readability-review`             |
| Review-only advisory pass               | `advisory-suggestions` + `agent-readability-review`         |
| Deep review inside a development loop   | `ai-dev-loop` + `insightforge-reviewer`                     |
| Improve a draft or agent answer         | `agent-readability-review` + `best-version-builder`         |
| Compare several alternatives            | `variant-best-version-builder` + `best-version-builder`     |
| Produce a polished final recommendation | `insightforge-reviewer` + `best-version-builder`            |
| Review code-facing docs for humans      | `project-scaffolding-and-docs` + `agent-readability-review` |

### Context, memory, and information compression

Use these when the challenge is too much context, long-running work, or preserving important state.

| Skill                                        | Use when you need                                                                                                                                  |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`context-compressor`](./context-compressor) | Compress long context into a smaller, high-signal handoff while preserving important facts, decisions, risks, validation evidence, and next steps. |

Common combinations:

| Goal                                       | Combine                                                    |
| ------------------------------------------ | ---------------------------------------------------------- |
| Continue a long development session        | `context-compressor` + `ai-dev-loop`                       |
| Continue a governed long session           | `cogniact-governor` + `context-compressor` + `ai-dev-loop` |
| Summarize a large repo investigation       | `context-compressor` + `core-coding-agent-behavior`        |
| Preserve decisions from a planning session | `context-compressor` + `project-scaffolding-and-docs`      |
| Compress before deep review                | `context-compressor` + `insightforge-reviewer`             |

### Benchmarks, datasets, and evaluation cases

Use these when building or evaluating benchmark tasks, test cases, datasets, or reality-grounded examples.

| Skill                                                      | Use when you need                                                                           |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`benchmark-dataset-builder`](./benchmark-dataset-builder) | Build benchmark datasets, task sets, or evaluation examples.                                |
| [`realitybench-caseforge`](./realitybench-caseforge)       | Create realistic benchmark cases, likely with emphasis on grounded, real-world task design. |

Common combinations:

| Goal                                          | Combine                                                                                                 |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Build an evaluation dataset                   | `benchmark-dataset-builder` + `realitybench-caseforge`                                                  |
| Govern benchmark construction                 | `cogniact-governor` + `benchmark-dataset-builder`                                                       |
| Concise benchmark iteration                   | `high-signal-mode` + `benchmark-dataset-builder`                                                        |
| Design realistic coding-agent benchmark tasks | `realitybench-caseforge` + `core-coding-agent-behavior`                                                 |
| Review benchmark quality                      | `benchmark-dataset-builder` + `insightforge-reviewer`                                                   |
| Build, review, and compress benchmark work    | `benchmark-dataset-builder` + `realitybench-caseforge` + `insightforge-reviewer` + `context-compressor` |

### Visualization and domain-specific generation

Use these when the task is specialized rather than general coding or review.

| Skill                                            | Use when you need                                                                                       |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [`mythos-visualization`](./mythos-visualization) | Mythos, story-world, concept, or visualization-oriented work.                                           |
| [`ponytail`](./ponytail)                         | Specialized workflow or domain-specific skill. Read its `SKILL.md` first to understand when it applies. |

Common combinations:

| Goal                                               | Combine                                              |
| -------------------------------------------------- | ---------------------------------------------------- |
| Visual/conceptual output with review               | `mythos-visualization` + `insightforge-reviewer`     |
| Governed visual/conceptual output                  | `cogniact-governor` + `mythos-visualization`         |
| Concise visual/conceptual output                   | `high-signal-mode` + `mythos-visualization`          |
| Domain-specific task with safer execution          | `ponytail` + `core-coding-agent-behavior`            |
| Domain-specific task inside an implementation loop | `ponytail` + `ai-dev-loop`                           |
| Domain-specific task with deep review              | `ponytail` + `ai-dev-loop` + `insightforge-reviewer` |
| Specialized output that needs polishing            | `ponytail` + `agent-readability-review`              |

### Meta-material: instructions, knowledge, and guidelines

These are not ordinary skill folders, but they are useful when setting up or supporting skills.

| Area                                         | Use when you need                                                                                                                  |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [`#INSTRUCTIONS`](./%23INSTRUCTIONS)         | Agent-specific setup instructions, such as Claude Code or Codex instructions. Read this before using skills with a specific agent. |
| [`#KNOWLEDGE-SKILLS`](./%23KNOWLEDGE-SKILLS) | Supporting knowledge bundles or packaged reference material. Use only when a skill or task needs that extra context.               |
| [`GUIDELINES`](./GUIDELINES)                 | General reusable guidelines, examples, and operating notes that can support multiple skills.                                       |

Common combinations:

| Goal                                   | Combine                               |
| -------------------------------------- | ------------------------------------- |
| Configure an agent before skill use    | `#INSTRUCTIONS` + the chosen skill    |
| Add background knowledge to a workflow | chosen skill + `#KNOWLEDGE-SKILLS`    |
| Add broad operating guidance           | chosen skill + `GUIDELINES`           |
| Govern an agent setup                  | `#INSTRUCTIONS` + `cogniact-governor` |
| Configure concise operation            | `#INSTRUCTIONS` + `high-signal-mode`  |

### Quick selection guide

| Starting point                                               | Best first choice                                        |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| “I want governed, controlled execution.”                     | `cogniact-governor`                                      |
| “I want concise, high-density execution.”                    | `high-signal-mode`                                       |
| “I want the agent to code safely.”                           | `core-coding-agent-behavior`                             |
| “I want a full review/implementation loop.”                  | `ai-dev-loop`                                            |
| “I want deep review inside the development loop.”            | `ai-dev-loop` + `insightforge-reviewer`                  |
| “I want a specialized workflow inside the development loop.” | `ponytail` + `ai-dev-loop`                               |
| “I have a GitHub issue to fix.”                              | `github-issue-fix-planner`                               |
| “I need project docs.”                                       | `project-scaffolding-and-docs`                           |
| “I need to compress a long session.”                         | `context-compressor`                                     |
| “I need better wording or readability.”                      | `agent-readability-review`                               |
| “I need advisory comments only.”                             | `advisory-suggestions`                                   |
| “I need to compare multiple outputs.”                        | `best-version-builder` or `variant-best-version-builder` |
| “I need a benchmark dataset.”                                | `benchmark-dataset-builder`                              |
| “I need realistic benchmark cases.”                          | `realitybench-caseforge`                                 |
| “I need visual/conceptual generation.”                       | `mythos-visualization`                                   |
| “I am unsure what a specialized skill does.”                 | Open that folder and read its `SKILL.md` first.          |

### How to combine skills

When combining skills, give the agent a clear priority order.

Recommended pattern:

```text
Use these skills in this order:

1. cogniact-governor as the top-level governance and decision-control layer.
2. high-signal-mode to keep execution concise and high-signal.
3. core-coding-agent-behavior if the task touches code or a repository.
4. The primary task skill.
5. Any review, cleanup, or compression skill needed for the task.

Task:
[describe the task here]
```

As a rule of thumb:

* Put `cogniact-governor` first when quality, control, or risk matters.
* Put `high-signal-mode` early when you want less noise and more direct output.
* Use `core-coding-agent-behavior` before code or repository work.
* Use **one primary task skill**.
* Add `ai-dev-loop` when work needs durable implementation/review state.
* Add `insightforge-reviewer` when deep review is needed.
* Add `ponytail` when that specialized workflow is relevant.
* Add `context-compressor` when the work becomes long or complex.
* Avoid loading unrelated skills just because they are available.

## Suggested workflows

### Workflow: Governed concise default

Use this when you want strong control and low-noise execution.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode

Task:
Proceed with governed, concise execution. Ask only necessary questions, preserve important evidence, and keep output high-signal.
```

### Workflow: Safe coding task

Use this when asking an agent to inspect, change, and validate code.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. core-coding-agent-behavior

Task:
Inspect the repository, identify the smallest safe change for the requested feature, implement it, run relevant checks, and summarize the evidence.
```

For longer tasks, add:

```text
Also use ai-dev-loop to preserve review and implementation state.
```

### Workflow: GitHub issue fix

Use this when starting from an issue number or bug report.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. core-coding-agent-behavior
4. github-issue-fix-planner
5. ai-dev-loop
6. insightforge-reviewer
7. ai-dev-loop-sanitize-commits

Task:
Plan and implement the fix for GitHub issue #123. Keep investigation notes, review findings, validation commands, deep review notes, and final commit cleanup evidence.
```

### Workflow: AI development loop with deep review

Use this when implementation quality matters and you want a stronger reviewer in the loop.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. core-coding-agent-behavior
4. ai-dev-loop
5. insightforge-reviewer

Task:
Run a durable implementation and review loop. Use insightforge-reviewer for deeper critique, risks, missed cases, and final quality assessment.
```

### Workflow: Ponytail inside an AI development loop

Use this when the specialized `ponytail` workflow should be executed through a durable implementation/review process.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. ponytail
4. ai-dev-loop
5. insightforge-reviewer

Task:
Apply the ponytail workflow, preserve implementation and review state with ai-dev-loop, and use insightforge-reviewer for final critique and quality review.
```

### Workflow: Documentation refresh

Use this when creating or improving project docs.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. project-scaffolding-and-docs
4. agent-readability-review
5. best-version-builder

Task:
Refresh the project README, contributor onboarding path, and durable documentation map for new contributors.
```

### Workflow: Benchmark creation

Use this when creating test or benchmark cases.

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. benchmark-dataset-builder
4. realitybench-caseforge
5. insightforge-reviewer

Task:
Create realistic benchmark cases with clear task definitions, expected evidence, scoring notes, and failure modes.
```

### Workflow: Long session handoff

Use this when a task has become too large for the current context.

```text
Use these skills in this order:

1. high-signal-mode
2. context-compressor

Task:
Compress the current session into a handoff that preserves decisions, constraints, completed work, validation evidence, open risks, and next actions.
```

For long coding sessions, use:

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. core-coding-agent-behavior
4. ai-dev-loop
5. context-compressor

Task:
Continue the feature implementation while preserving all decisions, risks, and validation evidence.
```

## How to add a new skill

When adding a new skill folder, prefer this minimum structure:

```text
new-skill-name/
  SKILL.md
  README.md
```

Use `SKILL.md` for the agent-facing behavior and `README.md` for the human-facing overview.

A good `SKILL.md` should explain:

* when to use the skill
* when not to use the skill
* required inputs
* operating procedure
* expected outputs
* validation or evidence requirements
* safety or privacy constraints
* which deeper files to read, if any

A good skill `README.md` should explain:

* what the skill is for
* how to invoke it
* what files are included
* examples of good prompts
* how to test or validate it
* how it combines with other skills

## How to maintain this repo

When editing a skill:

1. Update `SKILL.md` if the agent behavior changes.
2. Update `README.md` if the human-facing usage changes.
3. Update templates/examples if the expected output shape changes.
4. Run any validation scripts included in that skill folder.
5. Keep links and file paths accurate after renames.
6. Prefer small, focused changes over broad rewrites.

When adding package files, manifests, generated docs, or validation results, make sure they are reproducible or clearly labeled as generated.

## Privacy and safety

Do not paste private customer data, proprietary source code, credentials, internal URLs, or unreleased product details into a reusable skill unless the destination is private and appropriate for that information.

When turning a project-specific workflow into a reusable skill:

* Replace concrete names with placeholders.
* Replace exact paths with generic examples.
* Remove customer reports, screenshots, credentials, and private logs.
* Keep the lesson, but sanitize the source.

## Troubleshooting

### The agent ignores the skill

Make sure the prompt explicitly names the skill file:

```text
Use project-scaffolding-and-docs/SKILL.md.
```

If the skill has modules, tell the agent to read the module only when the `SKILL.md` says it is relevant.

### The agent reads too much

Do not ask it to load the whole repository. Start with the priority operating skills, then one task-specific skill.

Good:

```text
Use these skills in this order:

1. cogniact-governor
2. high-signal-mode
3. ai-dev-loop

Task:
Run the implementation loop for this change.
```

Avoid:

```text
Read every file in this repo and use all of it.
```

### The agent mixes incompatible instructions

Give a priority order:

```text
Use cogniact-governor as the top-level control layer.
Use high-signal-mode for concise output.
Use core-coding-agent-behavior only for repository-safe coding behavior.
Use ai-dev-loop only for implementation and review state.
Use insightforge-reviewer only for deep review and final quality assessment.
```

### The copied skill is missing dependencies

If a `SKILL.md` references `modules/`, `templates/`, `examples/`, or `scripts/`, copy those files along with the skill folder.

## License

MIT. See [`LICENSE`](./LICENSE).
