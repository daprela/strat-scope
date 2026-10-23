"""Realize approved wireframes as offline Stage 2D design artifacts.

Reads authored SVG only, never captured target HTML. Preserves geometry, applies
VIS roles and bounded illustrative fixtures. Not production UI or market data.
"""

import argparse
import copy
import hashlib
import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'ui-artifacts' / 'wireframes'
OUT = ROOT / 'ui-artifacts' / 'mockups'
VERSION = 'MP-SET-001-r9'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

# Exact VIS-COLOR and VIS-DATA values, in light/dark order.
TOKENS = {
    'base': ('#FFFFFF', '#151619'),
    'content': ('#FFFFFF', '#151619'),
    'raised': ('#FFFFFF', '#151619'),
    'text': ('#1E293B', '#D1D4DC'),
    'secondary': ('#1E293B', '#D1D4DC'),
    'border': ('#D4DAE3', '#2A2B30'),
    'separator': ('#D4DAE3', '#2A2B30'),
    'action': ('#1D4ED8', '#93C5FD'),
    'on_action': ('#FFFFFF', '#0F172A'),
    'success': ('#166534', '#86EFAC'),
    'warning': ('#92400E', '#FCD34D'),
    'error': ('#B91C1C', '#FCA5A5'),
    'uncertain': ('#6D28D9', '#D8B4FE'),
    'buy_bg': ('#DCFCE7', '#DCFCE7'),
    'buy_fg': ('#14532D', '#14532D'),
    'sell_bg': ('#FEE2E2', '#FEE2E2'),
    'sell_fg': ('#7F1D1D', '#7F1D1D'),
    'up': ('#16A34A', '#22C55E'),
    'up_border': ('#15803D', '#16A34A'),
    'down': ('#DC2626', '#F87171'),
    'down_border': ('#C91F1F', '#EF4444'),
}

# Fixture identifiers/times expose density without choosing financial defaults.
# Unknown financial inputs remain explicit; no filled trade is manufactured.
FIXTURES = {
    '[name]': 'Morning review', '[id]': 'R-014', '[identity]': 'R-014',
    '[version]': 'v12', '[settings version]': 'v3', '[retained version]': 'v12',
    '[time]': '09:42', '[bar time]': '09:41 UTC', '[run time]': '09:42 UTC',
    '[candidate time]': '09:30 UTC', '[cursor]': '09:42 UTC',
    '[paused / processing]': 'Paused', '[selected]': 'UTC',
    '[observation time]': '09:41 UTC', '[earliest]': 'Discovered start',
    '[latest usable]': 'Qualified end', '[quantity]': '10,000',
    '[quantity / instrument units]': '10,000 units', '[price if Limit / Stop]': 'Market — no price',
    '[optional price]': 'Not set', '[USD input]': '10,000.00',
    '[USD]': 'Unavailable', '[price]': 'Not set', '[value]': 'Unavailable',
    '[values]': 'Unavailable', '[provider-qualified]': 'provider activity',
    '[identity / current version]': 'O-008 / v2', '[symbol / provider alias / name]': 'EURUSD',
    '[local + provider identity]': 'EURUSD / Dukascopy', '[new basis]': 'Ask / H1',
    '[old basis]': 'Bid / M1', '[object]': 'Brush 03', '[brush]': 'Brush',
    '[identity / version]': 'Morning review / v12', '[items affected]': 'Selected layout',
    '[validated version]': 'v13', '[complete]': 'Validated',
    '[display time]': '09:42:00', '[TZ]': 'UTC',
    '[discovered bounds]': 'Discovered archive bounds', '[qualified condition]': 'Qualified local history',
    '[unavailable]': 'unavailable', '[selected name]': 'Morning review',
    '[version / cursor]': 'v12 / 09:42 UTC', '[identity / cursor]': 'R-014 / 09:42 UTC',
    '[identity / expected version]': 'R-014 / v12', '[time or owned scope]': '09:30 UTC / R-014',
    '[chart / run identity]': 'Chart 1 / R-014', '[instrument / settings version]': 'EURUSD / v3',
    '[balance]': '10,000.00', '[USD estimate]': 'Unavailable: no stop',
    '[basis / rate]': 'Fixed USD / 0.00', '[metadata / explicit override]': 'Retained instrument spec',
    '[instrument / side / period]': 'EURUSD / Bid / M1', '[instrument / side / timeframe]': 'EURUSD / Bid / M1',
    '[published version]': 'v12', '[local time]': '09:42 UTC',
    '[start / end]': '09:00–09:42 UTC', '[intervals]': '09:00–09:30 UTC',
    '[reason]': 'Required evidence unavailable', '[locked]': 'Locked', '[preview]': 'Preview',
    '[Buy or Sell]': 'Buy', '[requested levels]': 'Not set', '[selected index]': 'Point 03',
    '[time input]': '09:30 UTC', '[price input]': '1.08420',
    '[manual ticker / provider alias / name]': 'EURUSD', '[pending]': 'Loading',
    '[quantity / units]': '10,000 units', '[requested units]': '10,000 units',
    '[Bid or Ask]': 'Bid', '[YYYY-MM-DD]': '2026-10-15', '[hh:mm]': '09:30',
    '[display precision]': 'Use instrument precision', '[selected timezone]': 'UTC',
    '[selected study]': 'No study selected', '[completed time]': '09:42 UTC',
    '[side]': 'Buy', '[prices]': 'Not set', '[start date]': '2026-10-14', '[end date]': '2026-10-15',
}


def tag(name):
    return f'{{{NS}}}{name}'


def fixture(text, frame):
    """Only replace declared fixture fields; unresolved facts remain reasoned."""
    if frame.get('mockup_version') in ('MP-SET-001-r2', 'MP-SET-001-r8', VERSION):
        text = text.replace('[replay time]', '09:42 UTC').replace('[bars left]', 'Bars: —')
        text = text.replace('[replay price]', '1.08438')
        if text == 'P/L [USD]':
            return 'P/L —'
        if text.startswith('Order value '):
            return 'Value unavailable · Risk: no SL · 10,000 units'
        if text == 'Speed v':
            return 'Speed'
    text = text.replace('WF-FRAME-', 'MP-MOCK-').replace('WF-SET-001-r6', VERSION)
    text = text.replace('Bullish light / bearish dark', 'Rising green / falling red')
    text = text.replace('Bullish candles use light shades and bearish candles dark shades', 'Rising candles use green and falling candles red')
    text = text.replace('Bullish / rising: light gray · Bearish / falling: dark gray',
                        'Rising: green · Falling: red · open left / close right')
    text = text.replace('schematic chart / placeholder values', 'synthetic chart / review fixtures')
    text = text.replace('O [value]  H [value]  L [value]  C [value]   Selected [bar time]',
                        'O 1.08420  H 1.08446  L 1.08412  C 1.08438 · 09:41 UTC')
    text = text.replace('[selected value]', '1.08438')
    if text.startswith(('Bid OHLCV:', 'Bid O ', 'Bid L ', 'Ask OHLCV:', 'Ask O ', 'Ask L ')):
        ask = text.startswith('Ask')
        values = {'[open]': '1.08422' if ask else '1.08420', '[high]': '1.08448' if ask else '1.08446',
                  '[low]': '1.08414' if ask else '1.08412', '[close]': '1.08440' if ask else '1.08438',
                  '[volume]': '118' if ask else '124'}
        for field, value in values.items():
            text = text.replace(field, value)
    # Conditional draft readback and editor use the same illustrative level.
    # Keep optional/unknown prices elsewhere absent; pending validity retains terms.
    if text.startswith(('Type: Limit · level ', 'Type: Stop · level ')):
        text = text.replace('[price]', FIXTURES['[price input]'])
    for old, new in FIXTURES.items():
        text = text.replace(old, new)
    # Remaining semantic placeholders stay explicit: not guessed parameter values.
    return text


def status_role(frame):
    state = frame['state']
    if frame.get('mockup_version') == VERSION:
        if frame['variant'] in ('risk-invalid', 'entry-sell-risk-invalid'):
            return 'error'
        if 'pending' in frame['variant']:
            return 'warning'
    if state in (7, 21, 31, 47, 54, 62) or frame['variant'] == 'resolution-unknown':
        return 'uncertain'
    if state in (6, 12, 15, 22, 23, 29, 35, 44, 50, 53, 61):
        return 'error'
    if state in (4, 11, 13, 14, 20, 30, 33, 34, 38, 39, 40, 42, 43, 45, 46, 49, 51, 56, 60, 64):
        return 'warning'
    if state in (37, 55, 63):
        return 'success'
    return 'secondary'


def realize(frame, theme):
    path = SOURCE / frame['file']
    root = ET.fromstring(path.read_text())
    index = 0 if theme == 'light' else 1
    colors = {key: value[index] for key, value in TOKENS.items()}
    role = status_role(frame)
    root.set('data-theme', theme)
    revision = frame.get('mockup_version', VERSION)
    root.set('data-version', revision)
    root.set('data-source', frame['id'])
    root.find(tag('title')).text = f"MP-MOCK-{frame['id'][-3:]} — {frame['title']} / {theme}"
    root.find(tag('desc')).text = (
        'High-fidelity static design. Synthetic sample marks and fixture values are '
        'not market evidence, financial advice, product defaults or recorded trades. '
        'Bracketed facts remain unresolved design fields. No controls execute actions.')
    style = root.find(tag('style'))
    style.text = f'''
text{{font-family:system-ui,"Segoe UI",sans-serif;fill:{colors['text']};font-size:14px;font-variant-numeric:tabular-nums}}
.meta{{font-size:12px;fill:{colors['secondary']}}}
.heading{{font-size:16px;font-weight:600}} .title{{font-size:20px;font-weight:600}}
.control{{font-size:14px;font-weight:500}} .data{{font-size:13px}}
.identifier{{font-family:ui-monospace,Consolas,monospace;font-size:12px}}
'''
    for group in root.iter(tag('g')):
        if group.get('data-role') in ('settings-window', 'go-to-window'):
            for rect in group.findall(tag('rect'))[:2]:
                if float(rect.get('height', 0)) > 200:
                    rect.set('rx', '8')
        if group.get('data-control'):
            rect = group.find(tag('rect'))
            if rect is not None and rect.get('fill') in ('#dedede', '#d3d3d3'):
                group.set('data-selected', 'true')
        # State-note panels retain geometry but promote the scoped reason to
        # body type and add a redundant semantic marker rather than hue alone.
        children = list(group)
        for i, element in enumerate(children):
            if (element.tag == tag('rect') and element.get('fill') == '#f4f4f4'
                    and float(element.get('height', 0)) >= 48):
                for text in children[i+1:]:
                    if text.tag != tag('text'):
                        break
                    text.set('class', 'body')
                    text.set('style', f"fill:{colors[role]}")
                if i+1 < len(children) and children[i+1].tag == tag('text'):
                    first = children[i+1]
                    if role in ('warning', 'error', 'uncertain', 'success'):
                        first.text = {'warning': '! ', 'error': '× ', 'uncertain': '? ', 'success': '✓ '}[role] + (first.text or '')
    fills = {
        '#e9e9e9': 'base', '#fff': 'content', '#f7f7f7': 'base', '#fafafa': 'base',
        '#f5f5f5': 'raised', '#f4f4f4': 'raised', '#f0f0f0': 'raised',
        '#eee': 'base', '#e7e7e7': 'base', '#dedede': 'raised', '#ddd': 'base',
        '#f6f6f6': 'raised', '#f8f8f8': 'base', '#e8e8e8': 'base',
        '#f2f2f2': 'base', '#ccc': 'separator',
        '#d3d3d3': 'raised', '#e5e5e5': 'separator',
    }
    for element in root.iter():
        for attr in ('fill', 'stroke'):
            old = element.get(attr)
            if old in fills:
                element.set(attr, colors[fills[old]])
            elif old in ('#555', '#777', '#888', '#999', '#aaa', '#bbb'):
                element.set(attr, colors['border'])
            elif old in ('#171717', '#333', '#444', '#222', '#111'):
                element.set(attr, colors['text'])
            elif old in ('#e5e5e5', '#ddd'):
                element.set(attr, colors['separator'])
        if element.tag == tag('text') and element.text:
            element.text = fixture(element.text, frame)
            if 'WF-SET-' in element.text or VERSION in element.text:
                element.text = re.sub(r'(?:WF|MP)-SET-001-r\d+', revision, element.text)
        if element.tag == tag('rect'):
            w, h = float(element.get('width', 0)), float(element.get('height', 0))
            if h in (30, 32, 48) and w > 20:
                element.set('rx', '4')
        if element.tag == tag('path') and element.get('stroke-dasharray') == '4 4':
            # Decorative grid is subordinate to data/cursor lines.
            if element.get('stroke') in (colors['raised'], '#e5e5e5'):
                element.set('stroke', colors['separator'])
    for group in root.iter(tag('g')):
        if group.get('data-control'):
            rect = group.find(tag('rect'))
            label = group.get('data-control')
            selected = group.get('data-selected') == 'true'
            disabled = group.get('aria-disabled') == 'true'
            if selected:
                rect.set('stroke', colors['action'])
                rect.set('stroke-width', '2')
                group.set('data-selected', 'true')
                # A short selected marker is independent of text and focus.
                ET.SubElement(group, tag('path'), {
                    'd': f"M{float(rect.get('x'))+5},{float(rect.get('y'))+6} v18",
                    'stroke': colors['action'], 'stroke-width': '2', 'fill': 'none'})
            for text in group.findall(tag('text')):
                text.set('class', 'control')
                if disabled:
                    text.set('style', f"fill:{colors['secondary']}")
            if label in ('Buy', 'Sell', 'Buy direction', 'Sell direction') and rect is not None:
                side = label.split()[0].lower()
                rect.set('fill', colors[side + '_bg'])
                rect.set('stroke', colors[side + '_fg'])
                if disabled:
                    rect.set('stroke-dasharray', '4 3')
                for item in group:
                    if item.tag == tag('text'):
                        item.set('style', f"fill:{colors[side + '_fg']}")
                    elif item.tag == tag('path'):
                        item.set('stroke', colors[side + '_fg'])
            if label.startswith(('Confirm ', 'Delete ')) and not disabled and rect is not None:
                rect.set('stroke', colors['error'])
                for text in group.findall(tag('text')):
                    text.set('style', f"fill:{colors['error']}")
        if group.get('data-role') == 'persistent-chart':
            plot = next(e for e in group if e.get('data-role') == 'plot-area')
            py, ph = float(plot.get('y')), float(plot.get('height'))
            for marks in group.iter(tag('g')):
                mark_role = marks.get('data-role', '')
                if mark_role not in ('bid-candle', 'ask-candle', 'bid-volume', 'ask-volume'):
                    continue
                direction = marks.get('data-direction')
                for element in marks:
                    if element.tag == tag('rect'):
                        element.set('fill', colors[direction] if mark_role.startswith('bid-') else colors['content'])
                        element.set('stroke', colors[direction + '_border'])
                    elif element.tag == tag('path'):
                        element.set('stroke', colors[direction + '_border'])
            axis_index = 0
            time_index = 0
            for element in group.findall(tag('text')):
                if (element.text or '').startswith('O 1.08420'):
                    element.set('class', 'data')
                if element.text == 'Not set':
                    element.text = f'{1.0870-axis_index*0.0010:.4f}'
                    element.set('class', 'data')
                    axis_index += 1
                if element.text == '09:42':
                    element.text = ('09:00', '09:10', '09:20', '09:30')[time_index % 4]
                    time_index += 1
    # Scoped exception copy remains full-contrast and uses a distinct symbol.
    for element in root.iter(tag('text')):
        text = element.text or ''
        if re.search(r'outcome unknown|publication unknown|unknown save', text, re.I):
            element.set('style', f"fill:{colors['uncertain']}")
            element.text = '? ' + re.sub(r'^\?\s*', '', text)
        elif re.search(r'^ERROR:|^Error:|^REJECTED|^Invalid|^Blocked|^Missing', text):
            element.set('style', f"fill:{colors[role]}")
            element.text = '! ' + text
    theme_toolbars(root, theme)
    # Outside product canvas: unambiguous sample/non-authority note.
    meta = ET.SubElement(root, tag('text'), {'x': '24', 'y': '128', 'class': 'meta'})
    gate = 'G4 approved / G5 pending' if frame['gate_g4'] == 'APPROVED' else 'Scoped geometry revision / G4 and G5 pending'
    meta.text = f'{theme.title()} theme · Synthetic review fixtures only · {gate}'
    source_note = ET.SubElement(root, tag('text'), {'x': '24', 'y': '58', 'class': 'meta'})
    source_note.text = f"Source: {frame['id']} · {frame.get('source_version', 'WF-SET-001-r6')}"
    return ET.tostring(root, encoding='unicode') + '\n'


def theme_toolbars(root, theme):
    """Mark toolbar scope; all surfaces inherit the exact active theme palette."""
    shell = root.find(f".//{tag('g')}[@data-role='workspace-shell']")
    canvas = shell.find(tag('rect'))
    width, height = float(canvas.get('width')), float(canvas.get('height'))
    top = 88 if width == 640 else 44
    left = 44 if width == 640 else 48
    boxes = [(0, 0, width, top), (0, top, left, height-26),
             (width-44, top, width, height-26), (0, height-26, width, height)]
    def inside(element):
        if element.get('x') is None or element.get('y') is None:
            return False
        x, y = float(element.get('x')), float(element.get('y'))
        w, h = float(element.get('width', 0)), float(element.get('height', 0))
        return any(x >= a and y >= b and x+w <= c and y+h <= d for a,b,c,d in boxes)
    def apply(element):
        element.set('data-surface', 'toolbar')
        index = 0 if theme == 'light' else 1
        for rect in element.iter(tag('rect')):
            if rect.get('fill') not in ('none', TOKENS['buy_bg'][index], TOKENS['sell_bg'][index], TOKENS['action'][index]):
                rect.set('fill', TOKENS['base'][index])
    for element in shell:
        rect = element if element.tag == tag('rect') else element.find(tag('rect'))
        role = element.get('data-role', '')
        if element.get('role') == 'img' or role == 'floating-replay-bar' or (rect is not None and inside(rect)) or (element.tag == tag('text') and inside(element)):
            apply(element)
    # Per-chart range/calendar control strips are toolbars too.
    for group in shell.iter(tag('g')):
        if group.get('data-role') in ('range-strip', 'chart-range-strip', 'chart-range-controls'):
            apply(group)


def gallery(frames):
    esc = html.escape
    parts = ['''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'">
<title>High-fidelity mockups — Gate G5</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#151619;color:#D1D4DC;font:14px/1.5 system-ui,sans-serif}
main{max-width:1450px;margin:auto;padding:32px}h1{font-size:28px}h2{font-size:20px;margin-top:40px}
a{color:#93C5FD}a:focus-visible,summary:focus-visible{outline:2px solid #93C5FD;outline-offset:4px}
nav{display:flex;flex-wrap:wrap;gap:12px}figure{margin:16px 0 32px;border:1px solid #2A2B30;border-radius:8px;overflow:hidden}
figcaption{padding:16px;background:#151619}img{display:block;width:100%;height:auto}summary{padding:16px;cursor:pointer;background:#151619}
.badge{border:1px solid #2A2B30;padding:4px 8px;border-radius:4px}.note{max-width:95ch;color:#D1D4DC}
</style><main><p>DESIGN REVIEW · MP-SET-001-r1</p><h1>Chart workspace mockups</h1>
<p><span class="badge">113 compositions · 226 SVGs · light + dark</span> <span class="badge">G4 approved · G5 scoped review pending</span></p>
<p class="note">Review the preserved chart-led layout, semantic states and both themes. Synthetic fixtures demonstrate density; values are not market evidence or product defaults. Bracketed fields identify facts still governed upstream. These are static images: pictured controls do not execute actions.</p>
<nav><a href="../../index.html#ui-dossier">Dossier and verification</a><a href="../wireframes/index.html">Source wireframes</a><a href="mockup-index.json">Artifact metadata</a><a href="review-checks.json">Design check record</a><a href="#all">All views and states</a><a href="MP-SPEC-001.html">State / type / focus specimens</a></nav>
<h2>Featured compositions</h2>''']

    def figure(frame):
        mid = 'MP-MOCK-' + frame['id'][-3:]
        status = frame.get('source_status', 'Historical r6 design')
        return (f'<figure id="{mid}"><figcaption><strong>{mid} · {esc(frame["title"])}</strong> · '
                f'UIS-VIEW-{frame["view"]:03} / UIS-STATE-{frame["state"]:03} · {esc(status)}<br>'
                f'<a href="{mid}.svg">Light at full size</a> · <a href="{mid}-dark.svg">Dark at full size</a> · '
                f'<a href="../wireframes/{frame["file"]}">Source {frame["id"]}</a></figcaption>'
                f'<img loading="lazy" src="{mid}.svg" alt="Light: {esc(frame["title"])}">'
                f'<details><summary>Compare dark theme</summary><img loading="lazy" src="{mid}-dark.svg" alt="Dark: {esc(frame["title"])}"></details></figure>')
    featured = (107, 108, 109, 110, 111, 112, 113, 25, 68, 90, 93, 94, 95, 96, 27, 77, 15, 104, 103, 105, 106, 1, 90, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 78, 79, 80, 26, 30, 32, 55, 65)
    for number in dict.fromkeys(featured):
        parts.append(figure(frames[number-1]).replace('id="MP-MOCK-', 'id="featured-MP-MOCK-'))
    parts.append('<h2 id="all">Complete view and state inventory</h2>')
    for view in range(1, 9):
        group = [f for f in frames if f['view'] == view]
        parts.append(f'<section id="view-{view}"><h2>UIS-VIEW-{view:03}</h2>')
        parts.append(figure(group[0]))
        parts.append(f'<details><summary>{len(group)-1} state, disclosure and zoom variants</summary>')
        parts.extend(figure(f) for f in group[1:])
        parts.append('</details></section>')
    parts.append('</main></html>')
    content = '\n'.join(parts) + '\n'
    content = content.replace('DESIGN REVIEW · MP-SET-001-r1', f'DESIGN REVIEW · {VERSION}')
    content = content.replace('<h2>Featured compositions</h2>',
        '<p>All 113 compositions, both themes; approved r14 wireframes realized. Eleven conditional-entry pairs correct shared level readback in ready, pending, invalid, collapsed and zoom states. 102 other pairs retain exact approved bytes. Rising candles green; falling red. '
        'Bid bodies filled with darker matching borders; Ask hollow. Toolbars match theme backgrounds. '
        'All desktop side panels now align with watchlist top/bottom edges. '
        '104 shows both quotes with paired OHLCV/volume; 093–102 show trading and folder branches. '
        'Calculation basis remains independent. Scoped G5 review pending for 068/093–095/107–113 in both themes. UIADV-INT-002 owner correction supplied; independent closure requires G5 and independent recheck.</p><h2>Featured compositions</h2>')
    if all(f.get('gate_g5') == 'APPROVED' for f in frames):
        content = content.replace('G4 approved · G5 scoped review pending', 'G4 geometry accepted · G5 approved')
        content = content.replace('Scoped G5 review pending for 068/093–095/107–113 in both themes. UIADV-INT-002 owner correction supplied; independent closure requires G5 and independent recheck.', 'G5 approved: user, 22 October 2026, approve G5 mockups. Exact SVG hashes are recorded in approval-r9.json. Independent UIADV-INT-002 recheck is next.')
    (OUT / 'index.html').write_text(content)


def specimens():
    parts = ['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'">
<title>MP-SPEC-001 — visual state specimens</title>
<style>body{margin:0;font:14px/20px system-ui,sans-serif;background:#FFFFFF;color:#1E293B}main{padding:32px;max-width:1100px;margin:auto}section{padding:24px;margin:24px 0;border:1px solid #2A2B30;border-radius:8px}button{font:500 14px/20px system-ui;padding:8px 16px;border:1px solid var(--border);border-radius:4px;background:var(--content);color:var(--text);margin:8px}button:focus-visible,.focus{outline:2px solid var(--action);outline-offset:2px;box-shadow:0 0 0 2px var(--content)}button[aria-pressed=true]{border:2px solid var(--action);text-decoration:underline}button:hover{background:var(--base)}.status{margin:12px 0;font-weight:600}.primary{background:var(--action);color:var(--on_action)}a{color:#1D4ED8}a:focus-visible{outline:2px solid #1D4ED8;outline-offset:2px}</style>
<main><h1>MP-SPEC-001 · component state specimens</h1><p>Supplement to all MP-MOCK frames. Static, inert specimens; focus via Tab is reviewable. No product navigation or state mutation is simulated.</p><a href="index.html">Back to mockups</a>''']
    for index, theme in enumerate(('light', 'dark')):
        colors = {key: value[index] for key, value in TOKENS.items()}
        style = ';'.join(f'--{key}:{value}' for key, value in colors.items())
        parts.append(f'<section style="{style};background:var(--content);color:var(--text)"><h2>{theme.title()} / VIS states</h2>')
        parts.append('<button>Default</button><button aria-pressed="true">Selected: Chart 1</button><button class="focus">Focus specimen</button><button class="primary">Apply valid draft</button><button disabled>Submit unavailable</button><p>Unavailable reason: event evaluation is unfinished. Inspection remains available.</p>')
        for token, label in (('success', '✓ Checkpoint v12 saved'), ('warning', '! Coverage partial — unresolved span remains'), ('error', '× Rejected — close quantity exceeds remainder'), ('uncertain', '? Outcome unknown — reconcile original intent'), ('secondary', 'Ⅱ Paused — completed decision point')):
            parts.append(f'<p class="status" style="color:{colors[token]}">{label}</p>')
        parts.append('<p style="font-size:13px;font-variant-numeric:tabular-nums">Quantity 10,000 units · sample only · unavailable P/L: no recorded result</p></section>')
        parts.append(f'<section style="{style};background:var(--content);color:var(--text)"><h2>{theme.title()} / independent Bid and Ask visibility</h2>')
        parts.append('<p>Inert visual specimens. Each toggle affects only its candle series. Calculation basis, replay cursor and executable bid/ask rules are unchanged.</p>')
        for label, bid, ask in (('Bid only', True, False), ('Ask only', False, True),
                                ('Both series', True, True), ('Neither series', False, False)):
            parts.append(f'<div><strong>{label}</strong>')
            for side, pressed in (('Bid', bid), ('Ask', ask)):
                parts.append(f'<button aria-label="Show/hide {side.lower()} candles" aria-pressed="{str(pressed).lower()}">{side}{" ✓" if pressed else ""}</button>')
            parts.append('</div>')
        parts.append('<p>With neither series visible, axes, drawings and context remain; absent prices retain explicit unavailable reasons.</p></section>')
        parts.append(f'<section style="{style};background:var(--content);color:var(--text)"><h2>Theme toolbar / trade actions</h2><button aria-pressed="true">Bid ✓</button><button>Ask</button><button class="focus">Focus</button><button style="background:{colors["buy_bg"]};color:{colors["buy_fg"]};border-color:{colors["buy_fg"]}">Buy</button><button style="background:{colors["sell_bg"]};color:{colors["sell_fg"]};border-color:{colors["sell_fg"]}">Sell</button><button disabled>Play unavailable</button><p>Toolbar background, foreground and borders follow the active theme. Trade labels stay readable with green/red light fills in both themes.</p></section>')
    parts.append('</main></html>')
    (OUT / 'MP-SPEC-001.html').write_text('\n'.join(parts))


def product_preview(filename):
    """Export the exact product canvas, leaving review margins in the canonical SVG."""
    source = ET.parse(OUT / filename).getroot()
    shell = copy.deepcopy(source.find(f".//{tag('g')}[@data-role='workspace-shell']"))
    shell.attrib.pop('transform', None)
    canvas = shell.find(tag('rect'))
    width, height = canvas.get('width'), canvas.get('height')
    product = ET.Element(tag('svg'), {'width': width, 'height': height,
        'viewBox': f'0 0 {width} {height}', 'role': 'img', 'aria-labelledby': 'title desc'})
    for name in ('title', 'desc', 'style'):
        product.append(copy.deepcopy(source.find(tag(name))))
    product.append(shell)
    target = OUT / 'previews' / filename.replace('.svg', '-product.svg')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(ET.tostring(product, encoding='unicode') + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--all', action='store_true', help='Refresh the entire approved set; G5 remains pending')
    scope.add_argument('--frame', type=int, action='append', help='Refresh named approved frames; G5 remains pending')
    args = parser.parse_args()
    data = json.loads((SOURCE / 'frame-index.json').read_text())
    approval = json.loads((SOURCE / 'approval.json').read_text())
    revision_path = SOURCE / 'revision.json'
    revision = json.loads(revision_path.read_text()) if revision_path.exists() else {}
    assert data['version'] in (approval['version'], revision.get('version'))
    assert revision.get('baseline_approval_version', approval['version']) == approval['version']
    geometry_approval_path = SOURCE / 'approval-r12.json'
    geometry_approval = json.loads(geometry_approval_path.read_text()) if geometry_approval_path.exists() else {}
    old = json.loads((OUT / 'mockup-index.json').read_text())
    records = {f['source_wireframe']: f for f in old['frames']}
    numbers = set(args.frame or [int(f['id'][-3:]) for f in data['frames']])
    assert numbers <= {int(f['id'][-3:]) for f in data['frames']}
    for frame in data['frames']:
        if int(frame['id'][-3:]) not in numbers:
            continue
        digest = hashlib.sha256((SOURCE / frame['file']).read_bytes()).hexdigest()
        approved = frame['gate_g4'] == 'APPROVED'
        approved_hashes = geometry_approval.get('source_sha256', {}) if geometry_approval.get('version') == data['version'] and geometry_approval.get('status') == 'APPROVED' else approval['source_sha256']
        current_approval_path = SOURCE / revision.get('approval_record', 'approval.json')
        current_approval = json.loads(current_approval_path.read_text())
        if current_approval.get('version') == data['version'] and current_approval.get('status') == 'APPROVED':
            approved_hashes = current_approval['source_sha256']
        expected = approved_hashes if approved else revision.get('source_sha256', {})
        assert digest == expected.get(frame['file']), frame['id']
        frame = {**frame, 'mockup_version': VERSION, 'source_version': frame.get('artifact_version', data['version'])}
        mid = 'MP-MOCK-' + frame['id'][-3:]
        files = [mid + '.svg', mid + '-dark.svg']
        previous = records.get(frame['id'], {})
        for theme, filename in zip(('light', 'dark'), files):
            (OUT / filename).write_text(realize(frame, theme))
            product_preview(filename)
        records[frame['id']] = {**frame, 'id': mid, 'source_wireframe': frame['id'],
            'source_file': '../wireframes/' + frame['file'], 'source_sha256': digest,
            'file': files[0], 'dark_file': files[1], 'version': VERSION, 'gate_g5': 'PENDING',
            'source_status': 'MATCHES_CURRENT_WIREFRAME / REVIEW_PENDING',
            'visual_authority': 'visual-system.md revision 7; exact theme neutrals and green/red trade buttons',
            'fixture_policy': 'Synthetic review only; unresolved facts remain labelled',
            'prior_source_sha256': previous.get('prior_source_sha256', previous.get('source_sha256'))}
    frames = [records[f['id']] for f in data['frames']]
    metadata = {'version': VERSION, 'source_version': data['version'],
        'status': 'CURRENT_SOURCE / REVIEW_PENDING', 'gate_g5': 'PENDING',
        'current_source_version': data['version'], 'pending_source_wireframes': [],
        'approval': 'G4 r14 SATISFIED; 11 conditional-entry pairs PENDING HUMAN REVIEW at G5; 102 unchanged pairs retain prior approval',
        'approval_record': 'approval.json', 'revision_record': 'revision-r9.json',
        'visual_sha256': hashlib.sha256((ROOT/'visual-system.md').read_bytes()).hexdigest(),
        'frames': frames}
    for record in frames:
        record['light_sha256'] = hashlib.sha256((OUT / record['file']).read_bytes()).hexdigest()
        record['dark_sha256'] = hashlib.sha256((OUT / record['dark_file']).read_bytes()).hexdigest()
    (OUT / 'mockup-index.json').write_text(json.dumps(metadata, indent=2) + '\n')
    gallery([{**record, 'id': record['source_wireframe'],
        'file': Path(record['source_file']).name} for record in frames])
    specimens()
    print(f'Built {len(numbers)} paired mockups from {data["version"]}; G5 pending.')


if __name__ == '__main__':
    main()
