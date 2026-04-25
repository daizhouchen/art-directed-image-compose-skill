# Design Brief Template

Use this template after inspecting the images and applying the art direction kernel.

## Element Audit

```text
Inputs:
- 01 <filename>: <visual summary>
- 02 <filename>: <visual summary>

Element roles:
- Hero: <one selected subject/source and why>
- Support: <0-3 elements and their visual job>
- Motif: <colors/textures/shapes used indirectly>
- Discard: <elements intentionally excluded and why>
```

## Design Direction Options

When the user gives a broad request, propose 2-3 text-only directions:

```text
Direction A - <name>
Thesis: <one sentence>
Composition: <skeleton>
Palette/light: <strategy>
Why it works: <short rationale>

Direction B - <name>
...
```

If the user does not choose, select the most coherent direction and state the reason briefly.

## Final Brief

```text
Asset type: <poster / KV / product visual / concept art / social graphic / packaging / other>
Aspect ratio and size: <for example 1536x1024 or 1024x1536>
Design thesis: <one sentence>
Hero: <single primary visual>
Support elements: <short list>
Motifs: <textures/colors/forms used indirectly>
Composition skeleton: <one named skeleton>
Visual hierarchy: first read <x>; second read <y>; third read <z>
Style/medium: <one coherent medium>
Lighting: <direction, quality, contrast>
Color palette: <primary, secondary, accent, neutrals>
Materials and surface treatment: <unification details>
Typography: <exact text and placement, or "no text">
Constraints: <must keep / must avoid>
Discarded source details: <what not to include>
Anti-pileup rule: one hero, restrained supports, no object inventory, no collage unless requested
```

## Final Prompt

Use a compact but explicit final prompt:

```text
Create a polished <asset type> using the supplied reference images as source material.

Design thesis: <thesis>.
Use <hero> as the single dominant hero subject. Include only <support elements> as restrained secondary context. Use <motifs> indirectly for color, texture, or atmosphere. Do not include discarded source details.

Composition: <chosen skeleton and layout details>. The first read is <hero>; the second read is <support>; the third read is <detail/motif>. Preserve negative space and avoid visual clutter.

Style and unification: <medium>, <lighting>, <palette>, <materials>, <perspective/camera>. Make all elements feel designed into one coherent world rather than pasted together.

Text: <exact text or no text>.
Constraints: <must-have and must-avoid list>.
Avoid: collage-like pileup, multiple competing focal points, mismatched lighting, mismatched scale, noisy background, extra objects, watermark, unintended text.
```

## Repair Prompt

Use one targeted repair if needed:

```text
Keep the overall design, composition, hero subject, palette, and style. Fix only this issue: <specific issue>. Do not add new elements or change the visual hierarchy.
```
