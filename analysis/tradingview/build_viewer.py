"""Build an offline report and machine-readable UI inventory from local artifacts.

Requires the Python markdown package for regeneration. The generated HTML needs
no server, JavaScript libraries, network connection, or Python environment.
Captured target HTML is never executed or embedded into this report.
"""

import html
import hashlib
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent


def inventory(index):
    lookup = {r["id"]: r for r in index}
    selections = [
        ("chart_types", "E02", "chart-types"),
        ("intervals", "E02", "intervals"),
        ("trend_tools", "E03", "trend-tools"),
        ("fibonacci_gann", "E10", "fibonacci-state"),
        ("patterns", "E10", "patterns-state"),
        ("forecast_measure", "E10", "measurements-state"),
        ("shapes", "E10", "shapes-state"),
        ("annotations", "E10", "annotations-state"),
        ("magnets", "E10", "magnets-state"),
        ("main_menu", "E17", "menu-state"),
        ("snapshots", "E17", "snapshot-state"),
    ]
    groups = []
    for name, run, step_id in selections:
        step = next(s for s in lookup[run]["steps"] if s["step_id"] == step_id)
        text = (ROOT / step["files"]["accessibility"]).read_text()
        offset = text.rfind("  - treegrid:")
        menu = text[offset:] if offset >= 0 else text
        rows = []
        for line in menu.splitlines():
            match = re.match(r'\s+- row "(.*)"(.*):$', line)
            if match:
                rows.append({"name": match.group(1), "disabled": "[disabled]" in match.group(2), "selected": "[selected]" in match.group(2)})
        groups.append({"group": name, "evidence": run, "evidence_id": lookup[run]["evidence_id"], "step_id": step_id, "scope": "Captured visible accessibility tree; includes group headings. Menu presence does not establish availability or successful use.", "rows": rows})
    return groups


def main():
    index = json.loads((ROOT / "evidence/index.json").read_text())
    menu_inventory = inventory(index)
    index += json.loads((ROOT / "evidence/authenticated-index.json").read_text())
    (ROOT / "FEATURE-INVENTORY.json").write_text(json.dumps(menu_inventory, indent=2, ensure_ascii=False) + "\n")
    sections = []
    nav = []
    for source, section_id, title in [
        ("requirements-dossier.md", "requirements", "Dukascopy version requirements"),
        ("domain-model.md", "domain-model", "Dukascopy domain model"),
        ("architecture-dossier.md", "architecture", "Dukascopy architecture — boundaries, resilience and verification"),
        ("architecture-review.md", "architecture-review", "Independent architecture review"),
        ("ui-dossier.md", "ui-dossier", "Dukascopy UI dossier — Gate G4 approved; high-fidelity propagation next"),
        ("ui-review.md", "ui-review", "Independent UI adversarial review"),
        ("visual-system.md", "visual-system", "Visual system — accepted direction and canonical tokens"),
        ("implementation-standards.md", "implementation-standards", "Implementation standards — Gate G6 approved; ready for foundation bootstrap"),
        ("AUTHENTICATED-FINDINGS.md", "authenticated", "Authenticated findings"),
        ("REPLICATION-ANALYSIS.md", "analysis", "Replication analysis"),
        ("LOCAL-IMPLEMENTATION.md", "implementation", "Local implementation"),
    ]:
        md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"], extension_configs={"toc": {"baselevel": 2}})
        rendered = md.convert((ROOT / source).read_text())
        rendered = rendered.replace('href="LOCAL-IMPLEMENTATION.md"', 'href="#implementation"').replace('href="index.html"', 'href="#analysis"')
        rendered = rendered.replace('href="AUTHENTICATED-FINDINGS.md"', 'href="#authenticated"').replace('href="REPLICATION-ANALYSIS.md"', 'href="#analysis"')
        rendered = rendered.replace('href="requirements-dossier.md"', 'href="#requirements"')
        rendered = rendered.replace('href="domain-model.md"', 'href="#domain-model"')
        rendered = rendered.replace('href="architecture-dossier.md"', 'href="#architecture"')
        rendered = rendered.replace('href="architecture-review.md"', 'href="#architecture-review"')
        rendered = rendered.replace('href="ui-dossier.md"', 'href="#ui-dossier"')
        rendered = rendered.replace('href="ui-review.md"', 'href="#ui-review"')
        rendered = rendered.replace('href="visual-system.md"', 'href="#visual-system"')
        rendered = rendered.replace('href="implementation-standards.md"', 'href="#implementation-standards"')
        # Prefix heading IDs to avoid collisions between documents.
        def heading_tokens(tokens):
            for token in tokens:
                yield token
                yield from heading_tokens(token.get("children", []))

        for token in heading_tokens(md.toc_tokens):
            old_id = token["id"]
            new_id = section_id + "-" + old_id
            rendered = rendered.replace(f'id="{old_id}"', f'id="{new_id}"')
            if token["level"] <= 3:
                nav.append(f'<a href="#{html.escape(new_id)}">{html.escape(token["name"])}</a>')
        sections.append(f'<section id="{section_id}">{rendered}</section>')
    cards = []
    for run in index:
        for step in run["steps"]:
            shot = step["files"].get("screenshot")
            if not shot:
                continue
            title = f'{run["id"]} · {run["title"]} · {step["step_id"]}'
            ax = step["files"].get("accessibility")
            ax_link = f' · <a href="{html.escape(ax)}">Accessibility text</a>' if ax else ""
            cards.append(f'<figure data-search="{html.escape(title.lower())}"><a href="{html.escape(shot)}"><img loading="lazy" src="{html.escape(shot)}" alt="{html.escape(title)}"></a><figcaption>{html.escape(title)}<br><span class="muted">Step outcome: {html.escape(step["status"])}</span>{ax_link}</figcaption></figure>')
    controlled_images = len(cards)
    references = json.loads((ROOT / "ui-artifacts/reference-screenshots.json").read_text())["screenshots"]
    for ref in references:
        shot = ref["file"]
        assert hashlib.sha256((ROOT / shot).read_bytes()).hexdigest() == ref["sha256"]
        title = f'{ref["id"]} · {ref["title"]} · {Path(shot).name}'
        cards.append(f'<figure data-search="{html.escape(title.lower())}"><a href="{html.escape(shot)}"><img loading="lazy" src="{html.escape(shot)}" alt="{html.escape(ref["description"])}"></a><figcaption>{html.escape(title)}<br><span class="muted">User-designated visual reference; capture provenance unverified. Separate from the older controlled A30–A32 scenarios.</span></figcaption></figure>')
    evidence_rows = []
    for run in index:
        failed = sum(s["status"] == "failed" for s in run["steps"])
        state = "Includes interrupted actions" if any(s["status"] != "completed" for s in run["steps"]) else "Declared actions completed"
        evidence_rows.append(f'<tr><td>{run["id"]}</td><td>{html.escape(run["title"])}</td><td><code>{run["evidence_id"]}</code></td><td>{state}</td></tr>')
    content = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><title>TradingView local replication dossier</title>
<style>
:root{font-family:system-ui,sans-serif;color:#192b3a;background:#f5f7f8;line-height:1.65;--surface:#fff;--border:#d9e1e7;--muted:#536879;--accent:#006b61}
*{box-sizing:border-box}body{margin:0}a{color:var(--accent);text-underline-offset:3px}a:focus-visible,input:focus-visible{outline:3px solid #feae35;outline-offset:3px}
header{background:#123b3c;color:#fff;padding:32px max(24px,calc((100vw - 1470px)/2));border-bottom:5px solid #35b9a0}header p{margin:8px 0;max-width:850px}header a{color:#c7fff0}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase}.title{font-size:clamp(26px,3vw,42px);line-height:1.2;font-weight:700;margin:10px 0}
.layout{max-width:1518px;margin:auto;display:grid;grid-template-columns:250px minmax(0,1fr);gap:40px;padding:32px 24px}nav{position:sticky;top:16px;align-self:start;max-height:calc(100vh - 32px);overflow:auto;font-size:13px}nav strong{display:block;margin:12px 0 6px}nav a{display:block;padding:6px 10px;text-decoration:none;border-radius:5px}nav a:hover{background:var(--border)}main{min-width:0}section{margin-bottom:44px;padding:30px;background:var(--surface);border:1px solid var(--border);border-radius:9px;scroll-margin-top:18px}h1,h2,h3{line-height:1.3;scroll-margin-top:24px}h1{font-size:30px}h2{font-size:24px;margin-top:40px}h3{font-size:19px;margin-top:28px}p,li{max-width:90ch}pre{background:#122d35;color:#e4f4ef;padding:18px;border-radius:6px;overflow:auto;font-size:12px;line-height:1.6}code{font-family:ui-monospace,monospace;font-size:.88em;overflow-wrap:anywhere}p code,td code{background:#91a9b21a;padding:1px 4px;border-radius:3px}table{border-collapse:collapse;width:100%;font-size:13px;display:block;overflow-x:auto;margin:20px 0}td,th{border:1px solid var(--border);padding:10px 12px;text-align:left;vertical-align:top}th{background:#91a9b217}img{max-width:100%;height:auto;border:1px solid var(--border);border-radius:4px}figure{margin:0;border:1px solid var(--border);padding:12px;border-radius:6px}figcaption{font-size:12px;margin-top:8px}.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.gallery img{max-height:340px;width:100%;object-fit:contain;background:#7771}input{font:inherit;width:100%;padding:10px 14px;border:1px solid var(--border);border-radius:6px;margin-bottom:20px;background:var(--surface);color:inherit}.muted{color:var(--muted)}.scope{border-left:4px solid #35b9a0;padding-left:16px}.evidence td:nth-child(3){max-width:260px;word-break:break-all}[hidden]{display:none!important}
@media(max-width:960px){.layout{grid-template-columns:1fr;gap:12px}nav{position:static;max-height:230px;border:1px solid var(--border);padding:10px;background:var(--surface)}section{padding:18px}.gallery{grid-template-columns:1fr}}
@media(prefers-color-scheme:dark){:root{background:#101a21;color:#e3ecef;--surface:#18252e;--border:#344651;--muted:#aec3cc;--accent:#75d8bf}pre{background:#0c171e}header{background:#102d2e}}
@media print{header{padding:20px;color:#000;background:#fff}nav,input{display:none}.layout{display:block;padding:0}section{border:0;padding:10px;margin:0;break-before:page}a{color:inherit}.gallery{grid-template-columns:1fr 1fr}figure{break-inside:avoid}pre{white-space:pre-wrap;color:#000;background:#eee}table{display:table}body{background:#fff;color:#000}}
</style></head><body>
<header><div class="eyebrow">Observed interface · independent reconstruction design</div><div class="title">TradingView local replication dossier</div><p>A public-session baseline for rebuilding the SPX chart workspace locally, with an implementation blueprint and explicit parity gaps.</p><p>15 October 2026 · 18 captures · 32 selected screenshots · Signed out</p><p><a href="REPLICATION-ANALYSIS.md">Analysis source</a> · <a href="LOCAL-IMPLEMENTATION.md">Implementation source</a> · <a href="FEATURE-INVENTORY.json">Menu inventory JSON</a> · <a href="evidence/network-summary.json">Network summary</a></p></header>
<div class="layout"><nav aria-label="Report contents"><strong>Read</strong><a href="#analysis">Replication analysis</a><a href="#implementation">Local implementation</a><a href="#gallery">Screenshot gallery</a><a href="#evidence">Evidence register</a><strong>Document sections</strong>__NAV__</nav><main>
__SECTIONS__
<section id="gallery"><h2>Screenshot gallery</h2><p>Click an image to inspect its original pixels. A failed step can still capture a useful registration gate; captions preserve the action outcome.</p><label for="gallery-filter">Filter screenshots by feature or evidence reference</label><input id="gallery-filter" type="search" placeholder="For example: settings, Pine, E10, dark"><p id="gallery-count" class="muted" aria-live="polite">32 screenshots</p><div class="gallery">__CARDS__</div></section>
<section id="evidence"><h2>Evidence register</h2><p class="scope">These are controlled scenarios. Menu presence is separate from successful use. Authenticated operations and numerical parity remain unresolved. The full bundle preserves all limitations and failed/cancelled steps.</p><p><a href="evidence/index.json">Compact evidence index</a> · <a href="evidence/rea-session.json">Full REA evidence bundle (approximately 33 MB)</a> · <a href="extract_evidence.py">Offline extractor</a></p><table class="evidence"><thead><tr><th>Reference</th><th>Scope</th><th>Full REA Evidence ID</th><th>Action result</th></tr></thead><tbody>__ROWS__</tbody></table></section>
</main></div><script>
const filter=document.getElementById('gallery-filter');const figures=[...document.querySelectorAll('.gallery figure')];filter.addEventListener('input',()=>{const q=filter.value.trim().toLowerCase();let count=0;for(const f of figures){f.hidden=!f.dataset.search.includes(q);if(!f.hidden)count++;}document.getElementById('gallery-count').textContent=count+' screenshots';});
</script></body></html>"""
    content = content.replace("__NAV__", "".join(nav)).replace("__SECTIONS__", "\n".join(sections)).replace("__CARDS__", "\n".join(cards)).replace("__ROWS__", "\n".join(evidence_rows))
    content = content.replace("A public-session baseline for rebuilding the SPX chart workspace locally, with an implementation blueprint and explicit parity gaps.", "Anonymous and authenticated reference evidence for rebuilding the chart workspace locally, with an implementation blueprint and explicit parity gaps.")
    content = content.replace("15 October 2026 · 18 captures · 32 selected screenshots · Signed out", f"15–16 October 2026 · {len(index)} controlled scenarios · {controlled_images} controlled screenshots + {len(references)} supplemental UI references · Anonymous + signed in")
    content = content.replace('<a href="REPLICATION-ANALYSIS.md">Analysis source</a>', '<a href="AUTHENTICATED-FINDINGS.md">Authenticated update</a> · <a href="REPLICATION-ANALYSIS.md">Analysis source</a>')
    content = content.replace('<strong>Read</strong><a href="#analysis">', '<strong>Read</strong><a href="#authenticated">Authenticated findings</a><a href="#analysis">')
    content = content.replace('>32 screenshots</p>', f'>{len(cards)} screenshots</p>')
    content = content.replace('Authenticated operations and numerical parity remain unresolved. The full bundle preserves all limitations and failed/cancelled steps.', 'Authenticated workflows are documented separately from the anonymous baseline. Numerical parity, alert delivery, and order execution remain open. The indices preserve limitations and failed/cancelled steps; authenticated review text is a masked derivative.')
    content = content.replace('<a href="evidence/index.json">Compact evidence index</a>', '<a href="evidence/authenticated-index.json">Authenticated index</a> · <a href="evidence/authenticated-review.json">Authenticated review derivative</a> · <a href="evidence/index.json">Anonymous index</a>')
    (ROOT / "index.html").write_text(content)
    print(json.dumps({"gallery_images": len(cards), "inventory_groups": len(menu_inventory), "inventory_rows": sum(len(g["rows"]) for g in menu_inventory), "html_bytes": len(content.encode())}))


if __name__ == "__main__":
    main()
