#!/usr/bin/env python3
"""
Image Batch Processing Tool
============================
Batch resize, compress, rename, watermark, and export manifest for images.

Usage:
  python img_batch.py resize --input ./photos --output ./resized --width 800
  python img_batch.py compress --input ./photos --output ./compressed --quality 75
  python img_batch.py rename-pattern --input ./photos --output ./renamed --pattern "product_{seq:03d}"
  python img_batch.py watermark-text --input ./photos --output ./watermarked --text "© MyShop"
  python img_batch.py export-manifest --input ./photos --output manifest.csv
"""

import argparse
import csv
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}


def get_images(input_dir: str) -> list[Path]:
    """Return sorted list of supported image files in input_dir."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    images = sorted(
        p for p in input_path.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not images:
        print(f"No supported images found in '{input_dir}'.", file=sys.stderr)
        sys.exit(1)
    return images


def ensure_dir(path: str) -> Path:
    """Create directory if it doesn't exist and return Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def resize_image(img: Image.Image, width: int) -> Image.Image:
    """Resize image to target width, preserving aspect ratio."""
    if img.width <= width:
        return img  # no upscale
    ratio = width / img.width
    height = max(1, int(img.height * ratio))
    return img.resize((width, height), Image.LANCZOS)


def compress_image(img: Image.Image, quality: int) -> Image.Image:
    """Return image ready for saving with given JPEG quality hint (no-op transform)."""
    # Actual compression happens at save time; this is a no-op transform.
    return img


def rename_pattern(name: str, pattern: str, seq: int) -> str:
    """Apply rename pattern with sequence number."""
    return pattern.replace("{seq}", str(seq))


def add_watermark(img: Image.Image, text: str, opacity: float = 0.4, font_size: int = 36) -> Image.Image:
    """Add semi-transparent text watermark to bottom-right corner."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    margin = 10
    x = img.width - tw - margin
    y = img.height - th - margin
    alpha = int(255 * opacity)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, alpha))
    return Image.alpha_composite(img, overlay)


def export_manifest(input_dir: str, output_csv: str) -> None:
    """Export CSV manifest: filename, width, height, size_bytes."""
    images = get_images(input_dir)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "width", "height", "size_bytes"])
        for img_path in images:
            with Image.open(img_path) as img:
                w, h = img.size
            size = img_path.stat().st_size
            writer.writerow([img_path.name, w, h, size])
    print(f"Manifest exported to {output_csv} ({len(images)} images)")


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_resize(args):
    images = get_images(args.input)
    out_dir = ensure_dir(args.output)
    for img_path in images:
        with Image.open(img_path) as img:
            resized = resize_image(img, args.width)
            out_path = out_dir / img_path.name
            save_image(resized, out_path, img_path.suffix.lower())
    print(f"Resized {len(images)} images to width {args.width}px → {args.output}")


def cmd_compress(args):
    images = get_images(args.input)
    out_dir = ensure_dir(args.output)
    for img_path in images:
        with Image.open(img_path) as img:
            compressed = compress_image(img, args.quality)
            out_path = out_dir / img_path.name
            save_image(compressed, out_path, img_path.suffix.lower(), quality=args.quality)
    print(f"Compressed {len(images)} images (quality={args.quality}) → {args.output}")


def cmd_rename_pattern(args):
    images = get_images(args.input)
    out_dir = ensure_dir(args.output)
    for idx, img_path in enumerate(images, start=args.start):
        new_name = rename_pattern(img_path.name, args.pattern, idx)
        ext = img_path.suffix
        base = new_name if new_name.endswith(ext) else new_name + ext
        out_path = out_dir / base
        img_path.rename(out_path)
    print(f"Renamed {len(images)} images with pattern '{args.pattern}' → {args.output}")


def cmd_watermark_text(args):
    images = get_images(args.input)
    out_dir = ensure_dir(args.output)
    for img_path in images:
        with Image.open(img_path) as img:
            watermarked = add_watermark(img, args.text, opacity=args.opacity, font_size=args.font_size)
            out_path = out_dir / img_path.name
            save_image(watermarked, out_path, img_path.suffix.lower())
    print(f"Watermarked {len(images)} images with text '{args.text}' → {args.output}")


def cmd_export_manifest(args):
    export_manifest(args.input, args.output)


def save_image(img: Image.Image, path: Path, ext: str, quality: int = 85) -> None:
    """Save image, converting RGBA to RGB for JPEG."""
    if ext in (".jpg", ".jpeg"):
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(path, "JPEG", quality=quality, optimize=True)
    elif ext == ".png":
        img.save(path, "PNG", optimize=True)
    elif ext == ".webp":
        img.save(path, "WEBP", quality=quality)
    else:
        img.save(path)


# ── Argument parser ───────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="img_batch",
        description="Batch image processing: resize, compress, rename, watermark, manifest.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # resize
    p_resize = sub.add_parser("resize", help="Resize images to target width")
    p_resize.add_argument("--input", required=True, help="Input directory")
    p_resize.add_argument("--output", required=True, help="Output directory")
    p_resize.add_argument("--width", type=int, default=800, help="Target width in pixels")

    # compress
    p_compress = sub.add_parser("compress", help="Compress images")
    p_compress.add_argument("--input", required=True, help="Input directory")
    p_compress.add_argument("--output", required=True, help="Output directory")
    p_compress.add_argument("--quality", type=int, default=75, help="JPEG quality (1-100)")

    # rename-pattern
    p_rename = sub.add_parser("rename-pattern", help="Rename images with pattern")
    p_rename.add_argument("--input", required=True, help="Input directory")
    p_rename.add_argument("--output", required=True, help="Output directory")
    p_rename.add_argument("--pattern", required=True, help="Pattern with {seq} placeholder, e.g. product_{seq:03d}")
    p_rename.add_argument("--start", type=int, default=1, help="Starting sequence number")

    # watermark-text
    p_wm = sub.add_parser("watermark-text", help="Add text watermark")
    p_wm.add_argument("--input", required=True, help="Input directory")
    p_wm.add_argument("--output", required=True, help="Output directory")
    p_wm.add_argument("--text", required=True, help="Watermark text")
    p_wm.add_argument("--opacity", type=float, default=0.4, help="Watermark opacity (0-1)")
    p_wm.add_argument("--font-size", type=int, default=36, help="Font size in pixels")

    # export-manifest
    p_manifest = sub.add_parser("export-manifest", help="Export CSV manifest")
    p_manifest.add_argument("--input", required=True, help="Input directory")
    p_manifest.add_argument("--output", default="manifest.csv", help="Output CSV file")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    commands = {
        "resize": cmd_resize,
        "compress": cmd_compress,
        "rename-pattern": cmd_rename_pattern,
        "watermark-text": cmd_watermark_text,
        "export-manifest": cmd_export_manifest,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()