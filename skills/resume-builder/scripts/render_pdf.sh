#!/usr/bin/env bash
# Print an HTML file to PDF with headless Chrome and report the page count.
# Usage: render_pdf.sh IN.html OUT.pdf
set -euo pipefail
in="$1"; out="$2"
chrome="${CHROME:-}"
if [ -z "$chrome" ]; then
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome chromium chromium-browser; do
    if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then chrome="$c"; break; fi
  done
fi
[ -n "$chrome" ] || { echo "Chrome not found; set CHROME=/path/to/chrome" >&2; exit 2; }
profile="$(mktemp -d)"
"$chrome" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
  --user-data-dir="$profile" --print-to-pdf="$out" "file://$(cd "$(dirname "$in")" && pwd)/$(basename "$in")" 2>/dev/null
rm -rf "${profile:?}"
pages=$(python3 -c "import re,sys;print(len(re.findall(rb'/Type\s*/Page[^s]',open(sys.argv[1],'rb').read())))" "$out")
echo "$out: $pages page(s)"
[ "$pages" = "1" ] || { echo "Not one page: tighten wording (keep body text at 11pt or larger)." >&2; exit 1; }
