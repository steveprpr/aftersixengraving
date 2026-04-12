#!/usr/bin/env python3
"""
remove_backgrounds.py — Remove backgrounds from product photos using rembg.

Reads product images from assets/images/products/, removes backgrounds,
and saves processed versions back to the same folder with a '-nobg' suffix.

Requirements:
    pip install rembg Pillow onnxruntime

Run from the project root: python tools/remove_backgrounds.py

If rembg is not installed, the script will print instructions and exit.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
IMAGES_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products")

# Product images to process (skip hero, photo-*, and photoroom images)
TARGET_FILES = [
    "tumblers.jpg",
    "cutting-boards.jpg",
    "slate-coasters.jpg",
    "marble-coasters.jpg",
    "catch-all.jpg",
    "flasks.jpg",
    "whisky-glass.jpg",
    "key-chains.jpg",
]


def check_dependencies():
    """Check that rembg and Pillow are installed."""
    try:
        import rembg  # noqa: F401
        from PIL import Image  # noqa: F401
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print()
        print("Install required packages:")
        print("  pip install rembg Pillow onnxruntime")
        print()
        print("Note: First run downloads the AI model (~170 MB).")
        return False


def remove_background(input_path, output_path):
    """Remove background from a single image and save as PNG with transparency."""
    from rembg import remove
    from PIL import Image

    img = Image.open(input_path)
    result = remove(img)

    # Save as PNG to preserve transparency
    result.save(output_path, "PNG", optimize=True)


def main():
    if not check_dependencies():
        sys.exit(1)

    if not os.path.isdir(IMAGES_DIR):
        print(f"ERROR: Images directory not found: {IMAGES_DIR}")
        sys.exit(1)

    print(f"Source/Output: {IMAGES_DIR}")
    print()

    processed = 0
    skipped = 0

    for filename in TARGET_FILES:
        input_path = os.path.join(IMAGES_DIR, filename)

        if not os.path.isfile(input_path):
            print(f"  SKIP (not found): {filename}")
            skipped += 1
            continue

        # Output as PNG with -nobg suffix
        name_base = os.path.splitext(filename)[0]
        output_path = os.path.join(IMAGES_DIR, f"{name_base}-nobg.png")

        # Skip if already processed
        if os.path.isfile(output_path):
            print(f"  SKIP (already exists): {name_base}-nobg.png")
            skipped += 1
            continue

        try:
            print(f"  Processing: {filename} -> {name_base}-nobg.png ...")
            remove_background(input_path, output_path)
            processed += 1
            print(f"    Done.")
        except Exception as e:
            print(f"  ERROR processing {filename}: {e}")
            skipped += 1

    print()
    print(f"Finished. Processed: {processed}, Skipped: {skipped}")
    print(f"Output: {IMAGES_DIR}")
    if processed > 0:
        print()
        print("Background-removed images saved as *-nobg.png files.")
        print("To use them on the site, update image src attributes in HTML.")


if __name__ == "__main__":
    main()
