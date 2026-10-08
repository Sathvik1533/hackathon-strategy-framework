#!/usr/bin/env python3
"""
Extract Archify SVGs and render high-resolution transparent PNG assets for brag video.
"""

import os
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = REPO_ROOT / "brag-output" / "work"
WORK_DIR.mkdir(parents=True, exist_ok=True)

DIAGRAMS = {
    "topology": REPO_ROOT / "docs/architecture/system-architecture.html",
    "circuit_breaker": REPO_ROOT / "docs/architecture/circuit-breaker.lifecycle.html",
    "dataflow": REPO_ROOT / "docs/architecture/inter-layer-dataflow.html",
    "sequence": REPO_ROOT / "docs/architecture/request-execution.sequence.html",
    "polyglot": REPO_ROOT / "docs/architecture/polyglot-bridge.architecture.html",
    "autobot": REPO_ROOT / "docs/architecture/autobot-squad.workflow.html",
    "gamification": REPO_ROOT / "docs/architecture/gamification-quest.workflow.html",
}


def extract_and_render():
    print("🎨 Extracting & rendering Archify SVG blueprints for video composition...")
    for key, path in DIAGRAMS.items():
        if not path.exists():
            print(f"❌ Missing file: {path}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        m = re.search(r"(<svg[^>]*>.*?</svg>)", content, re.DOTALL)
        if not m:
            print(f"❌ No SVG found in {path.name}")
            continue

        svg_text = m.group(1)
        if "xmlns=" not in svg_text:
            svg_text = svg_text.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ')

        # Inject dark theme CSS override if needed so diagram text is bright and crisp
        svg_file = WORK_DIR / f"{key}.svg"
        png_file = WORK_DIR / f"{key}.png"

        with open(svg_file, "w", encoding="utf-8") as out:
            out.write(svg_text)

        # Convert using rsvg-convert (width 1400px for sharp downscaling onto 1920x1080 canvas)
        cmd = ["/opt/homebrew/bin/rsvg-convert", "-w", "1400", str(svg_file), "-o", str(png_file)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  ✔ Rendered {key}.png ({os.path.getsize(png_file):,} bytes)")
        else:
            print(f"  ❌ Error rendering {key}: {res.stderr}")


if __name__ == "__main__":
    extract_and_render()
