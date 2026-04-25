---
name: art-directed-image-compose
description: Create a Codex skill that turns local reference photos into art-directed design drafts with final gpt-image-2 generation.
status: active
created: 2026-04-25T10:29:29Z
---

# PRD: art-directed-image-compose

## Executive Summary

Create a reusable Codex skill named `art-directed-image-compose` that accepts one or more local photo paths, extracts usable visual elements, turns them into an art-directed design brief, and uses `gpt-image-2` for the final generated design draft. The skill must internalize art direction so it avoids visual pileups and produces complete, intentional design compositions.

## Problem Statement

Reference-photo image generation often fails by copying too many elements, mixing incompatible styles, or producing collage-like results. The skill needs to behave like an art director before it behaves like an image generator: it must rank elements, choose a visual hierarchy, define composition and unification strategy, and only then call `gpt-image-2`.

## User Stories

- As a user, I can provide a file, directory, or glob of photos and get a polished design draft based on the useful visual elements.
  - Acceptance criteria: the skill expands paths, filters image files, creates a manifest, and handles directories containing multiple photos.
- As a user, I can rely on the skill to choose what matters instead of forcing every source element into the output.
  - Acceptance criteria: the skill assigns each element to `hero`, `support`, `motif`, or `discard` before writing the final prompt.
- As a user, I can get a design result with coherent art direction.
  - Acceptance criteria: the skill defines design thesis, hierarchy, composition, palette, lighting, materials, and style unification before generation.
- As a user, I can control cost and iteration count.
  - Acceptance criteria: the skill defaults to one final `gpt-image-2` generation and asks or explains before extra exploration passes.
- As a user, I can inspect what was generated and why.
  - Acceptance criteria: the skill reports final prompt, input image mapping, output path, and design QA notes.

## Functional Requirements

- Support image inputs from files, directories, and glob expressions.
- Generate a JSON manifest of discovered input images.
- Generate a numbered contact sheet for multi-image review.
- Provide an art direction kernel that forces visual hierarchy, element selection, composition, color, lighting, and anti-pileup checks.
- Provide a design brief template for final prompt construction.
- Use the existing system `imagegen` CLI for final `gpt-image-2` generation.
- Preserve `gpt-image-2` constraints: no `input_fidelity`, no `background=transparent`, and no silent downgrade to another model.
- Limit final generation calls by default.
- Validate the skill with the system skill validator and executable script tests.

## Non-Functional Requirements

- Keep `SKILL.md` concise and move detailed art-direction rules into references.
- Use deterministic helper scripts for path expansion and contact sheet creation.
- Do not overwrite user assets by default.
- Keep manual intervention minimal; make reasonable defaults when the user does not specify a format, size, or destination.
- Produce clear failure messages for missing inputs, unsupported files, missing Pillow, or absent `OPENAI_API_KEY`.

## Success Criteria

- `quick_validate.py` passes for `/home/zcdai/.codex/skills/art-directed-image-compose`.
- `collect_image_inputs.py` correctly expands a test directory and writes valid JSON.
- `make_contact_sheet.py` creates a numbered sheet from the manifest.
- The skill documentation includes a final `gpt-image-2` command path using the existing imagegen CLI.
- The art direction kernel includes explicit anti-pileup checks and element role assignment.
- The GitHub repository contains the CCPM artifacts and skill implementation snapshot.

## Constraints & Assumptions

- The skill is installed under `/home/zcdai/.codex/skills` so Codex can auto-discover it.
- Final image generation uses `gpt-image-2` through `/home/zcdai/.codex/skills/.system/imagegen/scripts/image_gen.py`.
- Actual final image generation requires `OPENAI_API_KEY`; validation can use dry-run and local script tests without consuming image calls.
- The current workspace `/home/zcdai/image` starts without a git repository, so upload requires initializing a repository or creating a new GitHub repository.

## Out of Scope

- Training a custom model.
- Building a web UI.
- Guaranteeing exact text rendering inside generated images.
- Native transparent output with `gpt-image-2`; transparent output requires the existing imagegen fallback policy.
- Unlimited design iteration or automatic large batch generation.

## Dependencies

- Existing system `imagegen` skill and its `scripts/image_gen.py` CLI.
- Python 3.
- Pillow for contact sheet generation.
- GitHub CLI authentication for upload.
