# Image Generation Integration

Use the built-in `image_gen` tool for final generation by default. It does not require `OPENAI_API_KEY` and is the correct path for normal design drafts. Use the existing system imagegen CLI only when the user explicitly asks for `gpt-image-2`, CLI/API/model controls, or direct file-path execution.

## Default Built-In Path

Default flow:

1. Inspect the contact sheet and selected original references with `view_image`.
2. Keep only references that have a role: hero, support, or motif.
3. Call the built-in `image_gen` tool with the final art-directed prompt.
4. If the image is project-bound, move or copy the selected output from `$CODEX_HOME/generated_images/...` into the workspace after generation.
5. If the result is only exploratory or preview-only, it may remain in the default generated-images location.

Built-in prompt requirements:

- Describe selected input images by role and visible traits, not only by filename.
- Make the anti-pileup rule explicit: one hero, restrained supports, motifs as atmosphere or texture.
- State what must not change when a reference image should preserve identity, product shape, or layout.
- State "no text" when typography is not required.
- If exact text is required, include it verbatim and warn in the completion report that final production may need text cleanup.

## Built-In Local Image Handling

The built-in tool works from images visible in the conversation context. For local files, inspect each selected source image with `view_image` before calling `image_gen`. Do not assume the built-in tool can consume arbitrary local paths directly.

For many input images, use the contact sheet for analysis and inspect only the final selected originals before generation. Avoid feeding a large contact sheet as the only reference when precise subject fidelity matters.

## Transparent Output

For simple transparent-image requests, stay on the built-in path first: generate the subject on a flat chroma-key background and remove it locally with the system imagegen chroma-key helper. Do not switch to CLI true transparency unless the user explicitly confirms the fallback.

## CLI Fallback

Use the existing system imagegen CLI only after the user explicitly asks for `gpt-image-2`, CLI/API/model controls, explicit quality/size controls, or file-path execution. This path requires `OPENAI_API_KEY`.

Command path:

```bash
IMAGE_GEN="${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py"
```

Preflight for real CLI generation:

```bash
test -n "$OPENAI_API_KEY"
```

If `OPENAI_API_KEY` is missing, write the prompt and run a dry-run command only. Do not claim a CLI-generated image exists.

CLI with reference images:

```bash
python "$IMAGE_GEN" edit \
  --model gpt-image-2 \
  --image <hero-or-support-01> \
  --image <support-or-motif-02> \
  --prompt-file <final-prompt.txt> \
  --quality high \
  --size 1536x1024 \
  --out <final-output.png>
```

CLI without direct references:

```bash
python "$IMAGE_GEN" generate \
  --model gpt-image-2 \
  --prompt-file <final-prompt.txt> \
  --quality high \
  --size 1536x1024 \
  --out <final-output.png>
```

## CLI gpt-image-2 Constraints

- Do not pass `--input-fidelity`; `gpt-image-2` always uses high fidelity for image inputs.
- Do not pass `--background transparent`; `gpt-image-2` does not support true transparent output.
- Do not silently switch to `gpt-image-1.5`, even for transparency.
- Use `quality=high` for final design drafts unless the user asks for fast drafts.
- Use flexible sizes that respect `gpt-image-2` constraints: max edge 3840 px, both edges multiples of 16, long-to-short ratio at most 3:1, total pixels between 655360 and 8294400.

Common sizes:

- Square: `1024x1024`, `1536x1536`
- Landscape: `1536x1024`, `1792x1024`, `1920x1088`, `3840x2160`
- Portrait: `1024x1536`, `1024x1792`, `1088x1920`, `2160x3840`

## Call Budget

Default: one final built-in `image_gen` call.

Use a second call only for a specific repair such as wrong hierarchy, missing required support, lighting mismatch, or aspect-ratio failure. Do not iterate by vague taste adjustments.

## Output Paths

Prefer project-local paths:

```text
output/art-directed-image-compose/<descriptive-name>.png
tmp/art-directed-image-compose/final-prompt.txt
tmp/art-directed-image-compose/manifest.json
tmp/art-directed-image-compose/contact-sheet.jpg
```

Do not overwrite existing final assets unless the user explicitly asks. Use versioned filenames when needed.
