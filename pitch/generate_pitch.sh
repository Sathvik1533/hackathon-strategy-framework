#!/bin/bash
set -e

echo "🎨 Compiling Marp presentation pitch deck..."
marp pitch/pitch.marp.md -o pitch/presentation.html
echo "✔ Generated standalone interactive HTML: pitch/presentation.html"

if command -v chromium >/dev/null 2>&1 || [ -d "/Applications/Google Chrome.app" ]; then
  marp --pdf pitch/pitch.marp.md -o pitch/pitch_deck.pdf
  echo "✔ Generated PDF deck: pitch/pitch_deck.pdf"
fi
