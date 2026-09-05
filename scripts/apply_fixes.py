#!/usr/bin/env python3
"""
Apply three a11y / perf fixes to the PipeFish Labs site:
  1. Extract inline <style> block -> assets/css/main.css
  2. Bump --text-dim from #7F8EA3 to #9AAABF (WCAG AA on all dark surfaces)
  3. Add keyboard arrow-key navigation to .demo-tabs
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
html_path = root / "index.html"
css_path  = root / "assets" / "css" / "main.css"
css_path.parent.mkdir(parents=True, exist_ok=True)

html = html_path.read_text(encoding="utf-8")

# ── 1. Extract inline CSS ──────────────────────────────────────────────────
style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
if not style_match:
    sys.exit("ERROR: no <style> block found in index.html")

css_raw = style_match.group(1)

# ── 2. WCAG contrast fix ───────────────────────────────────────────────────
css_raw = css_raw.replace(
    "--text-dim:      #7F8EA3;",
    "--text-dim:      #9AAABF; /* WCAG AA: bumped from #7F8EA3 */"
)

# ── 3a. Add :focus-visible ring for keyboard users ─────────────────────────
css_raw = css_raw.replace(
    ".demo-tab:hover, .demo-tab.active {",
    (
        ".demo-tab:focus-visible { outline: 2px solid var(--cyan); outline-offset: 3px; }\n"
        "    .demo-tab:hover, .demo-tab.active {"
    )
)

# Strip the 4-space indent that was used inside <style> so the file is clean
lines   = css_raw.split("\n")
cleaned = [(l[4:] if l.startswith("    ") else l) for l in lines]
css_path.write_text("\n".join(cleaned), encoding="utf-8")
print(f"[1] CSS written  -> {css_path.relative_to(root)}  ({css_path.stat().st_size:,} bytes)")

# ── Replace <style>...</style> with <link> tag ─────────────────────────────
link_tag = '  <link rel="stylesheet" href="/assets/css/main.css">'
html = re.sub(r"\s*<style>.*?</style>", "\n" + link_tag, html, flags=re.DOTALL)
print(f"[2] Inline <style> replaced with <link> tag")

# ── 3b. Arrow-key / Home / End navigation for demo tabs ───────────────────
arrow_nav = r"""
// ── Demo tab keyboard navigation (arrow keys, Home, End) ──────────────────
document.addEventListener('DOMContentLoaded', function () {
  var container = document.querySelector('.demo-tabs');
  if (!container) return;
  container.addEventListener('keydown', function (e) {
    var tabs = Array.from(container.querySelectorAll('.demo-tab'));
    var idx  = tabs.indexOf(document.activeElement);
    if (idx === -1) return;
    var next = -1;
    if      (e.key === 'ArrowRight' || e.key === 'ArrowDown')  next = (idx + 1) % tabs.length;
    else if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')    next = (idx - 1 + tabs.length) % tabs.length;
    else if (e.key === 'Home')                                  next = 0;
    else if (e.key === 'End')                                   next = tabs.length - 1;
    else return;
    e.preventDefault();
    tabs[next].focus();
    tabs[next].click();
  });
});
"""

if "function resetDemoGraph()" not in html:
    sys.exit("ERROR: could not find resetDemoGraph anchor in index.html")

html = html.replace("function resetDemoGraph() {", arrow_nav + "\nfunction resetDemoGraph() {")
print(f"[3] Arrow-key navigation JS injected before resetDemoGraph()")

html_path.write_text(html, encoding="utf-8")
print(f"\nDone. index.html updated ({html_path.stat().st_size:,} bytes)")
