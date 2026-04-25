#!/usr/bin/env python3
"""Collect local image inputs into a deterministic JSON manifest."""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import mimetypes
from pathlib import Path
from typing import Iterable

IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".heif",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}


def _has_magic(value: str) -> bool:
    return any(ch in value for ch in "*?[")


def _expand_one(raw: str, recursive: bool) -> list[Path]:
    expanded = Path(raw).expanduser()
    candidates: list[Path] = []

    if _has_magic(raw):
        candidates.extend(Path(match).expanduser() for match in glob.glob(raw, recursive=True))
    elif expanded.is_dir():
        iterator = expanded.rglob("*") if recursive else expanded.iterdir()
        candidates.extend(path for path in iterator if path.is_file())
    else:
        candidates.append(expanded)

    return candidates


def collect_images(inputs: Iterable[str], recursive: bool, max_images: int | None = None) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()

    for raw in inputs:
        for candidate in _expand_one(raw, recursive=recursive):
            try:
                resolved = candidate.resolve(strict=True)
            except FileNotFoundError:
                continue
            if not resolved.is_file() or resolved.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(resolved)

    found.sort(key=lambda path: str(path).lower())
    if max_images is not None:
        found = found[:max_images]
    return found


def _sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def _dimensions(path: Path) -> dict[str, int] | None:
    try:
        from PIL import Image
    except ImportError:
        return None

    try:
        with Image.open(path) as image:
            return {"width": int(image.width), "height": int(image.height)}
    except Exception:
        return None


def build_manifest(inputs: list[str], images: list[Path], recursive: bool) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for index, path in enumerate(images, start=1):
        stat = path.stat()
        entry: dict[str, object] = {
            "id": f"{index:02d}",
            "path": str(path),
            "name": path.name,
            "extension": path.suffix.lower(),
            "bytes": stat.st_size,
            "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
            "sha256_16": _sha256_prefix(path),
        }
        dims = _dimensions(path)
        if dims:
            entry.update(dims)
        entries.append(entry)

    return {
        "created_utc": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "inputs": inputs,
        "recursive": recursive,
        "count": len(entries),
        "images": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect local image files into a JSON manifest.")
    parser.add_argument("inputs", nargs="+", help="Image files, directories, or glob patterns.")
    parser.add_argument("--out", required=True, help="Manifest JSON output path.")
    parser.add_argument("--no-recursive", action="store_true", help="Do not recurse into directories.")
    parser.add_argument("--max-images", type=int, help="Stop after this many sorted images.")
    args = parser.parse_args()

    if args.max_images is not None and args.max_images < 1:
        parser.error("--max-images must be greater than zero.")

    recursive = not args.no_recursive
    images = collect_images(args.inputs, recursive=recursive, max_images=args.max_images)
    if not images:
        parser.error("No supported image files found.")

    manifest = build_manifest(args.inputs, images, recursive=recursive)
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(images)} image(s) to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
