#!/usr/bin/env python3
"""Tests for img_batch.py"""

import csv
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: Pillow is required.", file=sys.stderr)
    sys.exit(1)

SCRIPT = Path(__file__).parent.parent / "img_batch.py"


def make_test_image(directory: str, name: str, size: tuple = (400, 300), color: str = "red") -> Path:
    """Create a small test image."""
    d = Path(directory)
    d.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), name, fill="white")
    path = d / name
    img.save(path)
    return path


def run_cmd(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def test_resize():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        out = os.path.join(tmp, "out")
        make_test_image(inp, "a.jpg", size=(1200, 800), color="blue")
        make_test_image(inp, "b.png", size=(600, 400), color="green")
        result = run_cmd(["resize", "--input", inp, "--output", out, "--width", "400"])
        assert result.returncode == 0, f"resize failed: {result.stderr}"
        assert (Path(out) / "a.jpg").exists()
        assert (Path(out) / "b.png").exists()
        with Image.open(Path(out) / "a.jpg") as img:
            assert img.width == 400, f"Expected width 400, got {img.width}"
        # b.png is 600px wide — should be resized down
        with Image.open(Path(out) / "b.png") as img:
            assert img.width == 400, f"Expected width 400, got {img.width}"
    print("  ✓ resize")


def test_compress():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        out = os.path.join(tmp, "out")
        make_test_image(inp, "photo.jpg", size=(800, 600), color="purple")
        result = run_cmd(["compress", "--input", inp, "--output", out, "--quality", "50"])
        assert result.returncode == 0, f"compress failed: {result.stderr}"
        assert (Path(out) / "photo.jpg").exists()
    print("  ✓ compress")


def test_rename_pattern():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        out = os.path.join(tmp, "out")
        make_test_image(inp, "x1.jpg", color="cyan")
        make_test_image(inp, "x2.jpg", color="magenta")
        # Copy to out first (rename moves files)
        import shutil
        shutil.copytree(inp, out, dirs_exist_ok=True)
        result = run_cmd(["rename-pattern", "--input", out, "--output", out, "--pattern", "item_{seq}"])
        assert result.returncode == 0, f"rename failed: {result.stderr}"
        assert (Path(out) / "item_1.jpg").exists()
        assert (Path(out) / "item_2.jpg").exists()
    print("  ✓ rename-pattern")


def test_watermark_text():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        out = os.path.join(tmp, "out")
        make_test_image(inp, "pic.jpg", size=(500, 400), color="orange")
        result = run_cmd(["watermark-text", "--input", inp, "--output", out, "--text", "© Shop"])
        assert result.returncode == 0, f"watermark failed: {result.stderr}"
        assert (Path(out) / "pic.jpg").exists()
    print("  ✓ watermark-text")


def test_export_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        manifest = os.path.join(tmp, "manifest.csv")
        make_test_image(inp, "a.jpg", size=(100, 80), color="red")
        make_test_image(inp, "b.png", size=(200, 150), color="blue")
        result = run_cmd(["export-manifest", "--input", inp, "--output", manifest])
        assert result.returncode == 0, f"manifest failed: {result.stderr}"
        with open(manifest, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        names = {r["filename"] for r in rows}
        assert "a.jpg" in names
        assert "b.png" in names
    print("  ✓ export-manifest")


def test_resize_no_upscale():
    """Images smaller than target width should not be upscaled."""
    with tempfile.TemporaryDirectory() as tmp:
        inp = os.path.join(tmp, "inp")
        out = os.path.join(tmp, "out")
        make_test_image(inp, "tiny.jpg", size=(200, 150), color="yellow")
        result = run_cmd(["resize", "--input", inp, "--output", out, "--width", "800"])
        assert result.returncode == 0
        with Image.open(Path(out) / "tiny.jpg") as img:
            assert img.width == 200, f"Should not upscale: got {img.width}"
    print("  ✓ resize-no-upscale")


if __name__ == "__main__":
    tests = [test_resize, test_compress, test_rename_pattern, test_watermark_text, test_export_manifest, test_resize_no_upscale]
    failed = 0
    for t in tests:
        try:
            t()
        except Exception as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(1 if failed else 0)