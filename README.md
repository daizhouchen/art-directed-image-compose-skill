# Art Directed Image Compose Skill

`art-directed-image-compose` is a Codex skill for turning local reference photos into a polished, art-directed design draft. It expands image paths, reviews the source material, assigns visual roles, builds a design brief, and generates the final raster image with the built-in `image_gen` tool by default.

The skill is designed to avoid reference-image pileups. It forces one hero, restrained support elements, a clear composition skeleton, palette and lighting decisions, and a design QA pass before completion.

## What It Does

- Accepts local image files, directories, or glob patterns.
- Creates a JSON image manifest.
- Creates a numbered contact sheet for multi-image review.
- Extracts source elements and assigns each to `hero`, `support`, `motif`, or `discard`.
- Builds an art-directed prompt with hierarchy, composition, style, palette, lighting, and anti-clutter rules.
- Uses built-in `image_gen` by default, so normal use does not require `OPENAI_API_KEY`.
- Keeps a CLI fallback for explicit `gpt-image-2` / API / model-control requests.

## Install

Clone this repository:

```bash
git clone https://github.com/daizhouchen/art-directed-image-compose-skill.git
cd art-directed-image-compose-skill
```

Install the skill into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -a skills/art-directed-image-compose "${CODEX_HOME:-$HOME/.codex}/skills/"
```

If an older copy already exists, replace it:

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/art-directed-image-compose"
cp -a skills/art-directed-image-compose "${CODEX_HOME:-$HOME/.codex}/skills/"
```

For local development, you can symlink instead of copying:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -sfn "$PWD/skills/art-directed-image-compose" "${CODEX_HOME:-$HOME/.codex}/skills/art-directed-image-compose"
```

## Dependencies

Required:

- Codex with skill support.
- Python 3.
- Pillow for contact sheet generation.

Install Pillow if needed:

```bash
python -m pip install pillow
```

Optional:

- `OPENAI_API_KEY` only if you explicitly use the CLI fallback for `gpt-image-2` / API / model controls.

## Usage

Invoke the skill from Codex:

```text
$art-directed-image-compose 用 /path/to/photos 里的参考图做一张高级产品 KV，主视觉要明确，避免堆砌。
```

Examples:

```text
$art-directed-image-compose 根据 ./pic 里的照片，提取可用元素，做一张社媒海报设计稿。
```

```text
$art-directed-image-compose 用 "~/Downloads/brand/*.jpg" 做一个主视觉设计，保留一个核心主体，其它只作为氛围和材质参考。
```

The default workflow uses built-in `image_gen`, so you do not need to configure an API key for normal generation.

## Helper Scripts

Collect image inputs into a manifest:

```bash
python skills/art-directed-image-compose/scripts/collect_image_inputs.py \
  "./pic" \
  --out tmp/art-directed-image-compose/manifest.json
```

Create a numbered contact sheet:

```bash
python skills/art-directed-image-compose/scripts/make_contact_sheet.py \
  --manifest tmp/art-directed-image-compose/manifest.json \
  --out tmp/art-directed-image-compose/contact-sheet.jpg
```

## CLI Fallback

The skill defaults to built-in `image_gen`. Use the CLI fallback only when you explicitly need `gpt-image-2`, API execution, model/quality/size controls, or direct file-path execution.

CLI fallback requires:

```bash
export OPENAI_API_KEY="your_api_key"
```

Then use the existing system imagegen CLI as documented in:

```text
skills/art-directed-image-compose/references/imagegen-generation.md
```

## Validate

Run the skill validator:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  skills/art-directed-image-compose
```

Compile the helper scripts:

```bash
python -m py_compile \
  skills/art-directed-image-compose/scripts/collect_image_inputs.py \
  skills/art-directed-image-compose/scripts/make_contact_sheet.py
```

## Repository Layout

```text
skills/art-directed-image-compose/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── art-direction-kernel.md
│   ├── design-brief-template.md
│   └── imagegen-generation.md
└── scripts/
    ├── collect_image_inputs.py
    └── make_contact_sheet.py
```

CCPM planning artifacts live under `.claude/`.
