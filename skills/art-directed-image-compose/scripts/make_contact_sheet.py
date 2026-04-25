#!/usr/bin/env python3
"""Create a numbered contact sheet from image inputs or a manifest."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from collect_image_inputs import collect_images


def _load_manifest(path: Path) -> list[tuple[str, Path, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    images = data.get("images", [])
    items: list[tuple[str, Path, str]] = []
    for index, item in enumerate(images, start=1):
        image_id = str(item.get("id") or f"{index:02d}")
        image_path = Path(str(item["path"])).expanduser()
        label = str(item.get("name") or image_path.name)
        items.append((image_id, image_path, label))
    return items


def _load_inputs(inputs: list[str], recursive: bool) -> list[tuple[str, Path, str]]:
    images = collect_images(inputs, recursive=recursive)
    return [(f"{index:02d}", path, path.name) for index, path in enumerate(images, start=1)]


def _fit_text(value: str, max_chars: int = 34) -> str:
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 1] + "..."


def make_contact_sheet(
    items: list[tuple[str, Path, str]],
    out: Path,
    columns: int,
    thumb_size: int,
    padding: int,
    label_height: int,
    background: str,
    quality: int,
) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageOps
    except ImportError as exc:
        raise SystemExit("Pillow is required for contact sheets. Install it with: python -m pip install pillow") from exc

    if not items:
        raise SystemExit("No images available for contact sheet.")

    columns = max(1, min(columns, len(items)))
    rows = math.ceil(len(items) / columns)
    tile_w = thumb_size + padding * 2
    tile_h = thumb_size + label_height + padding * 3
    sheet = Image.new("RGB", (columns * tile_w, rows * tile_h), background)
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, (image_id, image_path, label) in enumerate(items):
        row, col = divmod(index, columns)
        x0 = col * tile_w
        y0 = row * tile_h
        frame = (x0 + padding, y0 + padding, x0 + padding + thumb_size, y0 + padding + thumb_size)

        try:
            with Image.open(image_path) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")
                image.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
                thumb = Image.new("RGB", (thumb_size, thumb_size), "white")
                paste_x = (thumb_size - image.width) // 2
                paste_y = (thumb_size - image.height) // 2
                thumb.paste(image, (paste_x, paste_y))
        except Exception:
            thumb = Image.new("RGB", (thumb_size, thumb_size), "#eeeeee")

        sheet.paste(thumb, (frame[0], frame[1]))
        draw.rectangle(frame, outline="#cccccc", width=1)
        text = f"{image_id}  {_fit_text(label)}"
        draw.text((x0 + padding, y0 + thumb_size + padding * 2), text, fill="#111111", font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    suffix = out.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        sheet.save(out, quality=quality, optimize=True)
    else:
        sheet.save(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a numbered contact sheet for image review.")
    parser.add_argument("inputs", nargs="*", help="Image files, directories, or glob patterns.")
    parser.add_argument("--manifest", help="Manifest JSON from collect_image_inputs.py.")
    parser.add_argument("--out", required=True, help="Contact sheet output path.")
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--thumb-size", type=int, default=220)
    parser.add_argument("--padding", type=int, default=12)
    parser.add_argument("--label-height", type=int, default=28)
    parser.add_argument("--background", default="white")
    parser.add_argument("--quality", type=int, default=92)
    parser.add_argument("--no-recursive", action="store_true")
    parser.add_argument("--max-images", type=int)
    args = parser.parse_args()

    if args.manifest:
        items = _load_manifest(Path(args.manifest).expanduser())
    elif args.inputs:
        items = _load_inputs(args.inputs, recursive=not args.no_recursive)
    else:
        parser.error("Provide --manifest or at least one input path.")

    if args.max_images is not None:
        if args.max_images < 1:
            parser.error("--max-images must be greater than zero.")
        items = items[: args.max_images]

    make_contact_sheet(
        items=items,
        out=Path(args.out).expanduser(),
        columns=args.columns,
        thumb_size=args.thumb_size,
        padding=args.padding,
        label_height=args.label_height,
        background=args.background,
        quality=args.quality,
    )
    print(f"Wrote contact sheet to {Path(args.out).expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
