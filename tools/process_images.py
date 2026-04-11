#!/usr/bin/env python3
"""
process_images.py — Process product photos for the After Six Engraving site.

Reads from the ASE Images source folder, auto-rotates, center-crops,
resizes, enhances, and saves to assets/images/products/.

Run from the project root: python tools/process_images.py
"""

import os
import sys
from PIL import Image, ImageOps, ImageEnhance

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(
    os.path.expanduser("~"),
    "iCloudDrive", "Laser", "ASE Images"
)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "assets", "images", "products")

# Output sizes
PRODUCT_SIZE = 800    # Square product cards
HERO_SIZE = 1600      # Large hero/feature images
JPEG_QUALITY = 88

# Filename mapping: source name -> output name
FILE_MAP = {
    "Hero image.png": ("hero", "hero"),
    "Catch all.jpg": ("catch-all", "product"),
    "Cutting Boards.jpg": ("cutting-boards", "product"),
    "Flasks.jpg": ("flasks", "product"),
    "Key Chains.jpg": ("key-chains", "product"),
    "Marble Coasters.jpg": ("marble-coasters", "product"),
    "Slate Coasters.jpg": ("slate-coasters", "product"),
    "Whisky glass.png": ("whisky-glass", "product"),
    "tumblers.jpg": ("tumblers", "product"),
    "IMG_4177.JPEG": ("photo-01", "product"),
    "IMG_4181.JPEG": ("photo-02", "product"),
    "IMG_4185.JPEG": ("photo-03", "product"),
    "IMG_4273.JPEG": ("photo-04", "product"),
    "IMG_4304.JPEG": ("photo-05", "product"),
    "IMG_4305.JPEG": ("photo-06", "product"),
    "IMG_4726.JPEG": ("photo-07", "product"),
    "Photoroom_20250910_174017.JPEG": ("photoroom-01", "product"),
    # Skip Logo.png — it's the business logo, not a product photo
}


def center_crop_square(img):
    """Center-crop to a square."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))


def center_crop_4_3(img):
    """Center-crop to 4:3 ratio (landscape)."""
    w, h = img.size
    target_ratio = 4 / 3

    current_ratio = w / h
    if current_ratio > target_ratio:
        # Too wide — crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        # Too tall — crop height
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


def process_image(source_path, output_name, img_type):
    """Process a single image: rotate, crop, resize, enhance, save."""
    print(f"  Processing: {os.path.basename(source_path)} -> {output_name}.jpg")

    # Open and auto-rotate based on EXIF
    img = Image.open(source_path)
    img = ImageOps.exif_transpose(img)

    # Convert to RGB (handles PNG with alpha, RGBA, etc.)
    if img.mode != "RGB":
        # Create white background for transparent images
        if img.mode in ("RGBA", "LA", "PA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "RGBA":
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img, mask=img.convert("RGBA").split()[3])
            img = background
        else:
            img = img.convert("RGB")

    # Crop based on type
    if img_type == "hero":
        # Hero: 4:3 landscape crop, save at hero size
        img_cropped = center_crop_4_3(img)
        img_large = img_cropped.copy()
        img_large.thumbnail((HERO_SIZE, HERO_SIZE), Image.LANCZOS)
        img_small = img_cropped.copy()
        img_small.thumbnail((PRODUCT_SIZE, PRODUCT_SIZE), Image.LANCZOS)
    else:
        # Product: square crop
        img_cropped = center_crop_square(img)
        img_large = img_cropped.copy()
        img_large.thumbnail((HERO_SIZE, HERO_SIZE), Image.LANCZOS)
        img_small = img_cropped.copy()
        img_small.thumbnail((PRODUCT_SIZE, PRODUCT_SIZE), Image.LANCZOS)

    # Enhance both sizes
    for version, suffix in [(img_small, ""), (img_large, "-large")]:
        # Auto-contrast with slight cutoff
        enhanced = ImageOps.autocontrast(version, cutoff=1.5)

        # Boost saturation slightly
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.15)

        # Slight brightness bump
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.02)

        # Save
        out_path = os.path.join(OUTPUT_DIR, f"{output_name}{suffix}.jpg")
        enhanced.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main():
    if not os.path.isdir(SOURCE_DIR):
        print(f"ERROR: Source directory not found: {SOURCE_DIR}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Source: {SOURCE_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print()

    processed = 0
    skipped = 0

    for source_name, (output_name, img_type) in FILE_MAP.items():
        source_path = os.path.join(SOURCE_DIR, source_name)
        if not os.path.isfile(source_path):
            print(f"  SKIP (not found): {source_name}")
            skipped += 1
            continue

        try:
            process_image(source_path, output_name, img_type)
            processed += 1
        except Exception as e:
            print(f"  ERROR processing {source_name}: {e}")
            skipped += 1

    print()
    print(f"Done. Processed: {processed}, Skipped: {skipped}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
