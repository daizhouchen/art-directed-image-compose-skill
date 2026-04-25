# gpt-image-2 Integration

Use the existing system imagegen CLI. Do not create another OpenAI image script for this skill.

## Preflight

Check whether `OPENAI_API_KEY` exists before a real generation:

```bash
test -n "$OPENAI_API_KEY"
```

If it is missing, write the prompt and run a dry-run command only. Do not claim a final generated image exists.

## Command Path

```bash
IMAGE_GEN="${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py"
```

## Final Generation With Reference Images

Use `edit` when the references should influence source fidelity. Pass only selected images that serve hero, support, or motif roles. Keep the list to 16 or fewer.

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

## Final Generation Without Direct References

Use `generate` only when the user wants the photos analyzed but not directly used as image references.

```bash
python "$IMAGE_GEN" generate \
  --model gpt-image-2 \
  --prompt-file <final-prompt.txt> \
  --quality high \
  --size 1536x1024 \
  --out <final-output.png>
```

## gpt-image-2 Constraints

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

Default: one final `gpt-image-2` call.

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
