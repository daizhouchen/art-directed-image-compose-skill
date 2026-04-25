# Art Direction Kernel

Use this before writing any final prompt. The goal is to make a designed image, not a packed inventory of source-photo contents.

## 1. Design Thesis

Write one sentence:

```text
Use <hero> to express <idea/emotion/function>, while <support/motif> provides <context/texture/proof>, in a <medium/style> suitable for <use>.
```

If the thesis cannot be written clearly, the image will likely become a pileup. Simplify the source set before continuing.

## 2. Element Roles

Assign every meaningful source element one role:

- `hero`: the primary visual anchor. Use exactly one.
- `support`: secondary elements that clarify the story or product. Use 0-3.
- `motif`: colors, textures, patterns, props, or shapes used indirectly.
- `discard`: anything that weakens hierarchy, duplicates another idea, or only appears because it was present in a source photo.

Prefer discarding over crowding. A discarded element is a design decision, not a loss.

## 3. Visual Hierarchy

Define the viewing order:

```text
First read: <single primary focal point>
Second read: <supporting context>
Third read: <detail, texture, or brand cue>
```

If the first read contains "and", the hierarchy is probably broken.

## 4. Composition Skeletons

Choose one skeleton and commit to it:

- Centered key visual: one hero centered, controlled negative space, high symmetry.
- Diagonal motion: hero and supports create directional energy across the frame.
- Thirds with negative space: hero on one third, copy or quiet space on the other.
- Foreground/midground/background: spatial depth with one clear focal plane.
- Editorial grid: disciplined blocks, image/copy rhythm, magazine-like restraint.
- Product-KV stage: hero on a controlled visual stage with crafted light and supporting cues.
- Poster stack: bold top/bottom text zones with one dominant central image.

Do not mix multiple skeletons unless the user explicitly asks for a chaotic collage.

## 5. Style Unification

Resolve conflicts before generation:

- Medium: choose one of photoreal, cinematic photo, 3D render, editorial design, flat graphic, painterly illustration, or mixed-media collage.
- Light: define one direction and one quality such as softbox left, noon sun, rim-lit studio, or diffused overcast.
- Color temperature: warm, cool, neutral, or deliberate warm/cool contrast.
- Perspective: align camera height, lens feel, and scale.
- Materials: decide which surfaces should be matte, glossy, translucent, metallic, fabric, paper, glass, or organic.
- Sharpness: decide whether the image is crisp commercial, soft atmospheric, or grainy editorial.

Reference photos with conflicting lighting or camera styles are raw material; the final design must make them belong to one world.

## 6. Color Strategy

Use a restricted palette:

```text
Primary color: <dominant field or subject color>
Secondary color: <supporting family>
Accent color: <small high-contrast signal>
Neutrals: <background and balance colors>
Saturation: <restrained / vivid / muted / high contrast>
```

Do not preserve every source color. Harmonize, reduce, and assign color jobs.

## 7. Typography Strategy

If text is required:

- Write exact text verbatim.
- Define placement, hierarchy, and approximate scale.
- Keep copy short enough for image generation.
- State that final production may need post-generation text cleanup.

If text is not required, explicitly say no text, no logos, no watermark.

## 8. Anti-Pileup Gate

Before final prompt, answer:

- Is there exactly one hero?
- Does every visible support element change the meaning or usefulness of the design?
- Are motif elements used as texture or atmosphere instead of extra focal points?
- Is there enough negative space or quiet area?
- Are lighting, perspective, and material treatment unified?
- Would removing any visible support make the image clearer? If yes, remove it.
- Does the prompt describe a designed composition rather than a list of objects?

If any answer fails, revise the brief before generating.

## 9. Design QA After Generation

Evaluate the output against:

- Thesis: does the image communicate the intended idea?
- Hierarchy: is the first read immediate and singular?
- Composition: does it follow the chosen skeleton?
- Integration: do elements share light, perspective, and material logic?
- Restraint: does it avoid source-photo pileup?
- Use fitness: does it fit the requested asset type and aspect ratio?
- Constraints: are required elements present and forbidden elements absent?

Only use a repair call when the failure is specific enough to prompt in one sentence.
