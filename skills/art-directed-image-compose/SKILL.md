---
name: art-directed-image-compose
description: Art-directed image composition from local reference photos with final gpt-image-2 generation. Use when Codex needs to take one or more local image paths, directories, or globs; extract visual elements; choose what to keep or discard; create a coherent design direction; avoid collage-like pileups; and generate a final polished raster design draft with the existing imagegen gpt-image-2 CLI.
---

# Art Directed Image Compose

Turn local reference photos into a complete design draft by doing art direction before image generation. Treat the photos as source material, not a checklist of objects that must all appear.

## Required Workflow

1. Expand inputs with `scripts/collect_image_inputs.py`.
2. For multiple images, create a contact sheet with `scripts/make_contact_sheet.py`.
3. Inspect the original image(s) or contact sheet with `view_image`.
4. Read `references/art-direction-kernel.md` before writing the final design direction.
5. Assign every meaningful source element one role: `hero`, `support`, `motif`, or `discard`.
6. Write 2-3 text-only design directions when the request is broad; select the strongest default if the user does not choose.
7. Read `references/design-brief-template.md` to produce the final brief and prompt.
8. Read `references/imagegen-gpt-image-2.md` before final generation.
9. Generate the final image with the existing system imagegen CLI using `--model gpt-image-2`.
10. Run the design QA checklist before reporting completion.

## Input Collection

Use the bundled script for files, directories, and glob expressions:

```bash
python /home/zcdai/.codex/skills/art-directed-image-compose/scripts/collect_image_inputs.py \
  "path/or/glob" \
  --out tmp/art-directed-image-compose/manifest.json
```

For many images:

```bash
python /home/zcdai/.codex/skills/art-directed-image-compose/scripts/make_contact_sheet.py \
  --manifest tmp/art-directed-image-compose/manifest.json \
  --out tmp/art-directed-image-compose/contact-sheet.jpg
```

If there are more than 16 source images, do not pass all originals into `gpt-image-2`. Use the manifest and contact sheet for analysis, then choose only the hero/support/motif images that materially affect the final design.

## Art Direction Rules

Do not write the final prompt until these are explicit:

- Design thesis: one sentence describing the visual idea.
- Element roles: exactly one primary `hero`; few `support`; optional `motif`; intentional `discard`.
- Visual hierarchy: first read, second read, third read.
- Composition skeleton: one named structure such as centered key visual, diagonal motion, thirds with negative space, foreground/midground/background, editorial grid, or product-KV stage.
- Unification plan: lighting, color temperature, material treatment, perspective, sharpness, and rendering medium.
- Anti-pileup check: remove any element that has no visual job.

Use `references/art-direction-kernel.md` for the detailed design rubric.

## Generation Call Policy

Default to one final `gpt-image-2` call. Do not spend image calls on analysis.

Allowed call budget:

- Normal task: 1 final image call.
- Complex commercial visual: optional 1 exploration call, 1 final call, and 1 targeted repair call.
- More than that: explain what new information each extra call will produce before continuing.

If `OPENAI_API_KEY` is missing, prepare the prompt and dry-run command but do not claim that a final `gpt-image-2` image was generated.

## Final GPT Image Command Shape

Use `edit` with one or more selected image references when source fidelity matters:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py" edit \
  --model gpt-image-2 \
  --image selected-reference-01.jpg \
  --image selected-reference-02.jpg \
  --prompt-file tmp/art-directed-image-compose/final-prompt.txt \
  --quality high \
  --size 1536x1024 \
  --out output/art-directed-image-compose/final-design.png
```

Use `generate` only when the photos were used purely for analysis and should not be direct image inputs.

Never pass `--input-fidelity` with `gpt-image-2`. Never pass `--background transparent` with `gpt-image-2`. Do not silently switch to another image model.

## Completion Report

Report:

- Final output path, or dry-run status if no API key was available.
- Input manifest path and contact sheet path when created.
- Selected hero/support/motif/discard decisions.
- Final prompt file path or final prompt text.
- Design QA result: hierarchy, composition, unification, anti-pileup, and constraints.
