#!/usr/bin/env python3
"""
build_gallery.py — Walks assets/designs/ and generates gallery_data.js
Run from the project root: python tools/build_gallery.py
"""

import os
import re
import json

# Path setup — works from project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DESIGNS_DIR = os.path.join(PROJECT_ROOT, "assets", "designs")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "assets", "gallery_data.js")

# Map folder names to clean category labels
CATEGORY_MAP = {
    "Family": "Family",
    "Work": "Work",
    "Humor": "Humor",
    "Drinks": "Drinks",
    "Wedding": "Wedding",
    "Bachelorette": "Bachelorette",
    "Golf": "Golf",
    "Inspirational_Quotes": "Inspirational Quotes",
    "Family_Monograms": "Family Monograms",
    "Charcuterie": "Charcuterie",
    "Cutting_Boards_Kitchen": "Cutting Boards & Kitchen",
    "Seasonal_Holiday": "Seasonal & Holiday",
    "Home_Cozy": "Home & Cozy",
    "Fitness": "Fitness",
    "Maps": "Maps",
}

# Desired display order for categories
CATEGORY_ORDER = [
    "Family",
    "Work",
    "Humor",
    "Drinks",
    "Wedding",
    "Bachelorette",
    "Golf",
    "Inspirational Quotes",
    "Family Monograms",
    "Charcuterie",
    "Cutting Boards & Kitchen",
    "Seasonal & Holiday",
    "Home & Cozy",
    "Fitness",
    "Maps",
]


def humanize_filename(filename):
    """Turn a filename like 'Don_t_Ask_Just_Pour.svg' into 'Don't Ask Just Pour'."""
    name = os.path.splitext(filename)[0]

    # Handle SVG_ prefix (common in Coasters)
    name = re.sub(r"^SVG_", "", name)

    # Replace underscores with spaces
    name = name.replace("_", " ")

    # Insert spaces before uppercase letters in camelCase/PascalCase words
    # e.g., "Adultingtimeinsession" stays as-is but
    # "BackToTheGrind" becomes "Back To The Grind"
    # For run-together lowercase words, try to split on common patterns
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)

    # For all-lowercase run-together names, insert spaces before common words
    # This handles names like "Adultingtimeinsession" -> "Adulting Time In Session"
    common_words = [
        "time", "goes", "here", "the", "this", "that", "your", "you",
        "my", "me", "is", "in", "on", "to", "for", "and", "but", "or",
        "not", "no", "all", "because", "two", "people", "fell", "love",
        "another", "day", "completely", "ruined", "by", "back", "grind",
        "beer", "being", "colleague", "only", "gift", "need", "coworker",
        "bless", "home", "cheers", "pour", "decisions", "coffee", "wine",
        "with", "have", "drink", "just", "ask", "don", "mess", "up",
        "table", "good", "things", "happen", "over", "tea", "of",
        "best", "friends", "are", "ones", "where", "what", "when",
        "how", "happy", "life", "live", "laugh", "every", "moment",
        "matters", "step", "breathe", "will", "never", "always",
        "together", "forever", "family", "husband", "wife", "dad",
        "mom", "made", "from", "scratch", "season", "everything",
        "blessed", "grateful", "thankful", "sip", "happens",
    ]

    # Only attempt word-splitting on names that are a single long word (no spaces)
    if " " not in name.strip() and len(name) > 12:
        lower = name.lower()
        # Greedy match — try to split from the left
        result = []
        i = 0
        while i < len(lower):
            matched = False
            # Try longest match first (up to 12 chars)
            for length in range(min(12, len(lower) - i), 2, -1):
                word = lower[i:i + length]
                if word in common_words or (length >= 4 and word in common_words):
                    result.append(word)
                    i += length
                    matched = True
                    break
            if not matched:
                # Take characters until next recognized word
                j = i + 1
                while j < len(lower):
                    found = False
                    for length in range(min(12, len(lower) - j), 2, -1):
                        if lower[j:j + length] in common_words:
                            found = True
                            break
                    if found:
                        break
                    j += 1
                result.append(lower[i:j])
                i = j
        if len(result) > 1:
            name = " ".join(result)

    # Fix common contractions: "Don t" -> "Don't"
    name = re.sub(r"\bDon t\b", "Don't", name)
    name = re.sub(r"\bcan t\b", "can't", name, flags=re.IGNORECASE)
    name = re.sub(r"\bwon t\b", "won't", name, flags=re.IGNORECASE)
    name = re.sub(r"\bisn t\b", "isn't", name, flags=re.IGNORECASE)
    name = re.sub(r"\bdoesn t\b", "doesn't", name, flags=re.IGNORECASE)

    # Handle "design-01" style names — make them "Design 01"
    name = re.sub(r"^design[- ]?(\d+)$", r"Design \1", name, flags=re.IGNORECASE)

    # Handle bare numbers like "3" or "12"
    if re.match(r"^\d+$", name.strip()):
        name = f"Design {name.strip()}"

    # Handle filenames ending with -01, -02 etc (like "Monstera Leaf Coasters-03")
    name = re.sub(r"-(\d+)$", r" \1", name)

    # Clean up multiple spaces
    name = re.sub(r"\s+", " ", name).strip()

    # Title case
    name = name.title()

    # Fix small words that should be lowercase (except at start)
    small_words = {"A", "An", "The", "In", "On", "To", "For", "And", "But", "Or", "Of", "By", "Is"}
    words = name.split()
    for i in range(1, len(words)):
        if words[i] in small_words:
            words[i] = words[i].lower()
    name = " ".join(words)

    return name


def build_gallery_data():
    designs = []

    # Process root-level SVGs (like Live Laugh Love.svg)
    for filename in sorted(os.listdir(DESIGNS_DIR)):
        filepath = os.path.join(DESIGNS_DIR, filename)
        if os.path.isfile(filepath) and filename.lower().endswith(".svg"):
            if filename.lower() == "logo.svg":
                continue  # Skip business logo
            designs.append({
                "category": "Inspirational Quotes",
                "name": humanize_filename(filename),
                "file": f"assets/designs/{filename}",
            })

    # Process each category folder
    for folder_name in sorted(os.listdir(DESIGNS_DIR)):
        folder_path = os.path.join(DESIGNS_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue
        if folder_name not in CATEGORY_MAP:
            continue

        category = CATEGORY_MAP[folder_name]

        svg_files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".svg")
        ])

        for filename in svg_files:
            designs.append({
                "category": category,
                "name": humanize_filename(filename),
                "file": f"assets/designs/{folder_name}/{filename}",
            })

    # Sort by category order, then by name within each category
    def sort_key(item):
        cat = item["category"]
        try:
            idx = CATEGORY_ORDER.index(cat)
        except ValueError:
            idx = 999
        return (idx, item["name"].lower())

    designs.sort(key=sort_key)

    return designs


def main():
    designs = build_gallery_data()

    # Build category list with counts
    categories = {}
    for d in designs:
        cat = d["category"]
        categories[cat] = categories.get(cat, 0) + 1

    # Generate JS output
    js_lines = []
    js_lines.append("// Auto-generated by tools/build_gallery.py")
    js_lines.append("// Do not edit manually — run: python tools/build_gallery.py")
    js_lines.append("")
    js_lines.append(f"const GALLERY_DESIGNS = {json.dumps(designs, indent=2)};")
    js_lines.append("")

    # Also export category list for filter bar
    cat_list = []
    for cat in CATEGORY_ORDER:
        if cat in categories:
            cat_list.append({"name": cat, "count": categories[cat]})
    # Add any categories not in the predefined order
    for cat in categories:
        if cat not in CATEGORY_ORDER:
            cat_list.append({"name": cat, "count": categories[cat]})

    # Always include Maps even if empty
    if "Maps" not in categories:
        cat_list.append({"name": "Maps", "count": 0})

    js_lines.append(f"const GALLERY_CATEGORIES = {json.dumps(cat_list, indent=2)};")
    js_lines.append("")

    js_content = "\n".join(js_lines)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {OUTPUT_FILE}")
    print(f"Total designs: {len(designs)}")
    for cat_info in cat_list:
        print(f"  {cat_info['name']}: {cat_info['count']}")


if __name__ == "__main__":
    main()
