#!/usr/bin/env python3
"""Generate 5 sample placeholder images for testing."""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)

SAMPLES = [
    ("product_001.jpg", (1200, 800), "#3498db", "Product A — Blue Widget"),
    ("product_002.jpg", (1920, 1080), "#2ecc71", "Product B — Green Gadget"),
    ("product_003.png", (800, 600), "#e74c3c", "Product C — Red Gizmo"),
    ("product_004.jpg", (1600, 1200), "#9b59b6", "Product D — Purple Thing"),
    ("product_005.webp", (1024, 768), "#f39c12", "Product E — Orange Doohickey"),
]


def generate_samples(output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for filename, size, color, label in SAMPLES:
        img = Image.new("RGB", size, color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        except (OSError, IOError):
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (size[0] - tw) // 2
        y = (size[1] - th) // 2
        draw.text((x, y), label, font=font, fill="white")
        img.save(out / filename)
        print(f"  Created {filename} ({size[0]}x{size[1]})")
    print(f"Generated {len(SAMPLES)} sample images in {output_dir}")


if __name__ == "__main__":
    generate_samples("samples")