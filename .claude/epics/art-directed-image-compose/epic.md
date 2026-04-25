---
name: art-directed-image-compose
status: completed
created: 2026-04-25T10:29:29Z
updated: 2026-04-25T10:41:56Z
progress: 100%
prd: .claude/prds/art-directed-image-compose.md
github: https://github.com/daizhouchen/art-directed-image-compose-skill/issues/1
---

# Epic: art-directed-image-compose

## Overview

Create and publish a Codex skill that converts local reference photos into art-directed design prompts and final `gpt-image-2` design drafts. The implementation combines CCPM traceability, deterministic image-input helpers, a concise skill workflow, and reference files that encode art-direction judgment.

## Architecture Decisions

- Install the executable skill in `/home/zcdai/.codex/skills/art-directed-image-compose`.
- Keep the repository snapshot in `/home/zcdai/image` for GitHub upload and CCPM traceability.
- Reuse the existing system `imagegen` CLI instead of writing another OpenAI image client.
- Use local scripts for deterministic input expansion and contact sheet generation.
- Store deeper art-direction guidance in references so `SKILL.md` remains concise.
- Treat `gpt-image-2` as mandatory for final generation and fail clearly when prerequisites are missing.

## Technical Approach

### Skill Files

- `SKILL.md`: trigger description, decision workflow, required outputs, and call-count policy.
- `references/art-direction-kernel.md`: visual hierarchy, selection, composition, color, lighting, style-unification, and QA rules.
- `references/design-brief-template.md`: reusable brief and final prompt structure.
- `references/imagegen-gpt-image-2.md`: exact integration guidance for the system imagegen CLI.
- `scripts/collect_image_inputs.py`: expand input paths into a manifest.
- `scripts/make_contact_sheet.py`: create a numbered contact sheet for visual review.

### Backend Services

No new service is required. Final generation is delegated to the existing local `imagegen` CLI.

### Infrastructure

Initialize a git repository in `/home/zcdai/image`, snapshot the skill implementation, create or use a GitHub repository through `gh`, push the branch, and create GitHub issues from the CCPM epic and tasks.

## Implementation Strategy

1. Create CCPM PRD, epic, and task files.
2. Initialize the skill with the system `skill-creator` initializer.
3. Replace the generated template with concise production instructions.
4. Add deterministic helper scripts and test them locally.
5. Add art-direction references that force role assignment and anti-pileup checks.
6. Validate the skill structure and run dry-run checks for the `gpt-image-2` command path.
7. Commit and upload the workspace snapshot to GitHub.
8. Sync the epic and task records to GitHub issues.

## Task Breakdown Preview

- 001: CCPM planning artifacts.
- 002: Skill scaffolding and metadata.
- 003: Image input helper scripts.
- 004: Art direction and prompt references.
- 005: Validation, git commit, and GitHub upload.

## Dependencies

- `skill-creator` initializer and validator.
- Existing `imagegen` CLI.
- `gh` authenticated as a GitHub user.
- Pillow for contact sheet tests.

## Success Criteria (Technical)

- All helper scripts run successfully on generated test images.
- `quick_validate.py` passes.
- `image_gen.py edit --model gpt-image-2 --dry-run` succeeds with generated test inputs.
- A git commit records the implementation.
- A GitHub repository exists and contains the pushed implementation.

## Estimated Effort

- Size: M
- Hours: 4

## Tasks Created

- [x] 2.md - Create CCPM planning artifacts (parallel: false)
- [x] 3.md - Initialize skill scaffolding and metadata (parallel: false)
- [x] 4.md - Implement image input helper scripts (parallel: true)
- [x] 5.md - Encode art direction and prompt references (parallel: true)
- [x] 6.md - Validate, commit, and upload to GitHub (parallel: false)

Total tasks: 5
Parallel tasks: 2
Sequential tasks: 3
Estimated total effort: 4 hours
