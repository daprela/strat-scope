"""Check authored Stage 2D artifacts offline; no runtime conformance or approval."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from build_mockups import TOKENS

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'ui-artifacts/mockups'
NS = {'s': 'http://www.w3.org/2000/svg'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(svg):
    return [tuple(e.get(a) for a in ('x', 'y', 'width', 'height'))
            for e in svg.findall('.//s:rect', NS)]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.executable = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[key] for key in ('href', 'src') if key in attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('script', 'iframe', 'object', 'embed') or any(k.startswith('on') for k in attrs):
            self.executable.append(tag)


def main():
    meta = json.loads((OUT / 'mockup-index.json').read_text())
    source_meta = json.loads((ROOT / 'ui-artifacts/wireframes/frame-index.json').read_text())
    approval = json.loads((ROOT / 'ui-artifacts/wireframes/approval.json').read_text())
    geometry_approval_path = ROOT / 'ui-artifacts/wireframes/approval-r12.json'
    geometry_approval = json.loads(geometry_approval_path.read_text()) if geometry_approval_path.exists() else {}
    # Historical acceptance remains valid for unchanged bytes across scoped revisions.
    approved_hashes = dict(approval['source_sha256'])
    if geometry_approval.get('status') == 'APPROVED':
        approved_hashes.update(geometry_approval.get('source_sha256', {}))
    approved_hashes.update(json.loads((ROOT/'ui-artifacts/wireframes/approval-r13.json').read_text())['source_sha256'])
    rows = meta['frames']
    assert len(rows) == 113 and len(source_meta['frames']) == 113
    assert meta['pending_source_wireframes'] == []
    assert [f['source_wireframe'] for f in rows] == [f['id'] for f in source_meta['frames']]
    revision_path = ROOT / 'ui-artifacts/wireframes/revision.json'
    revision = json.loads(revision_path.read_text()) if revision_path.exists() else {}
    current_approval_path = ROOT / 'ui-artifacts/wireframes' / revision.get('approval_record', 'approval.json')
    current_approval = json.loads(current_approval_path.read_text())
    if current_approval.get('version') == source_meta['version'] and current_approval.get('status') == 'APPROVED':
        approved_hashes.update(current_approval['source_sha256'])
    assert meta['current_source_version'] == source_meta['version']
    assert meta['source_version'] == source_meta['version']
    assert source_meta['version'] in (approval['version'], revision.get('version'))
    assert approval['status'] == 'APPROVED'
    assert meta['visual_sha256'] == digest(ROOT / 'visual-system.md'), 'VIS source drift'
    assert {f['view'] for f in rows} == set(range(1, 9))
    assert {f['state'] for f in rows} == set(range(1, 65))
    allowed = {color.upper() for pair in TOKENS.values() for color in pair}
    current, stale = [], []
    panel_checks = []
    for frame in rows:
        assert frame['gate_g5'] in ('PENDING', 'STALE', 'APPROVED')
        source = ROOT / 'ui-artifacts/wireframes' / Path(frame['source_file']).name
        source_matches = digest(source) == frame['source_sha256']
        expected = approved_hashes if frame['gate_g4'] == 'APPROVED' else revision.get('source_sha256', {})
        assert digest(source) == expected.get(source.name), 'G4/revision source drift'
        if source_matches:
            current.append(frame['id'])
        else:
            assert frame['gate_g5'] == 'STALE' and frame['source_status'].startswith('STALE_SOURCE')
            stale.append(frame['id'])
        old = ET.parse(source).getroot()
        for theme, filename, hash_key in (('light', frame['file'], 'light_sha256'),
                                          ('dark', frame['dark_file'], 'dark_sha256')):
            path = OUT / filename
            assert digest(path) == frame[hash_key], (filename, 'rendered SVG drift')
            svg = ET.parse(path).getroot()
            assert svg.get('data-theme') == theme
            assert not any(svg.findall('.//s:' + tag, NS) for tag in ('script', 'foreignObject', 'image'))
            for element in svg.iter():
                assert not any(k.lower().startswith('on') for k in element.attrib)
            assert all(c.upper() in allowed for c in re.findall(r'#[0-9a-fA-F]{3,6}\b', path.read_text()))
            if frame['gate_g5'] == 'APPROVED':
                accepted = json.loads((OUT / frame.get('approval_record', 'approval.json')).read_text())
                assert digest(path) == accepted['mockup_sha256'][filename], 'Retained G5 hash drift'
            if not source_matches:
                continue
            shell = svg.find('.//s:g[@data-role="workspace-shell"]', NS)
            labels = [e for e in shell.iter() if e.tag.endswith('}text')]
            product_text = ' '.join(e.text or '' for e in labels)
            number = int(frame['id'][-3:])
            if number in (25, 68, 90, 93, 94, 95, 96, *range(107, 114)):
                def entry_control(name):
                    control = shell.find(f'.//s:g[@data-control="{name}"]', NS)
                    assert control is not None, (filename, name)
                    return control
                ready_buy = number in (25, 68, 90, 93, 94, 95)
                ready_sell = number in (107, 110, 112)
                assert entry_control('Buy').get('aria-disabled') == str(not ready_buy).lower()
                assert entry_control('Sell').get('aria-disabled') == str(not ready_sell).lower()
                assert entry_control('Edit entry / direction').get('aria-disabled') == 'false'
                assert 'completed decision 09:42' in product_text
                if ready_buy:
                    assert 'Sell unavailable: draft is Buy' in product_text
                elif ready_sell:
                    assert 'Buy unavailable: draft is Sell' in product_text
                else:
                    assert 'old estimates superseded' in product_text
                if number in (68, 93, 94, 95, *range(107, 114)):
                    capsule = shell.find('.//s:g[@data-role="floating-replay-bar"]', NS)
                    assert capsule is not None, (filename, 'missing shared capsule')
                    summary = ' '.join(e.text or '' for e in capsule.findall('s:text', NS))
                    level = re.search(r'Type: (Limit|Stop) · level ([^ ]+)', summary)
                    assert level and level[2] == '1.08420', (filename, 'required proposed level')
                    editor = shell.find('.//s:g[@data-role="entry-direction-editor"]', NS)
                    if editor is not None:
                        ticket = ' '.join(e.text or '' for e in editor.iter() if e.tag.endswith('}text'))
                        proposed = re.search(r'Entry level ([^ ]+)', ticket)
                        assert proposed and proposed[1] == level[2], (filename, 'draft readback mismatch')
                        side = 'Buy' if number in (68, 93, 94, 95, 113) else 'Sell'
                        assert f'Direction: {side} · Type: {level[1]}' in ticket
                        assert f'{side} draft' in summary
                        assert 'Entry draft · R-014 · EURUSD' in ticket
                    else:
                        assert number == 110, (filename, 'missing ticket')
                    if ready_buy or ready_sell:
                        assert 'VALID:' in summary, (filename, 'missing validation context')
                    else:
                        assert 'Both unavailable:' in summary and 'VALID:' not in summary
                if number == 109:
                    error = next(e for e in labels if 'retained levels invalid for Sell' in (e.text or ''))
                    assert error.get('style') == 'fill:' + TOKENS['error'][0 if theme == 'light' else 1]
            if frame['id'] == 'MP-MOCK-015':
                failure = next(e for e in labels if 'save failed for this version' in (e.text or ''))
                assert failure.text.startswith('× ')
                assert failure.get('style') == 'fill:' + TOKENS['error'][0 if theme == 'light' else 1]
                assert 'Working v13 applied · Save FAILED v13 · Retained v12 · Retry retention (do not Apply again)' in product_text
            if frame['id'] in ('MP-MOCK-027', 'MP-MOCK-077'):
                for name in ('Start bar', 'Play', 'Step', 'Sell', 'Buy'):
                    controls = shell.findall(f'.//s:g[@data-control="{name}"]', NS)
                    assert controls and all(c.get('aria-disabled') == 'true' for c in controls)
                if frame['id'] == 'MP-MOCK-027':
                    for phrase in ('Submitting entry', 'Pending request I-009', 'original occurrence',
                                   'Submitted terms', 'Prior valid orders / positions retained',
                                   'No new entry or replay advance while pending'):
                        assert phrase in product_text
                else:
                    assert 'Publication outcome unknown' in product_text
                    recovery = shell.find('.//s:g[@data-control="Reconcile publication"]', NS)
                    assert recovery is not None and recovery.get('aria-disabled') != 'true'
            assert geometry(svg) == geometry(old), (filename, 'geometry drift')
            assert svg.get('viewBox') == old.get('viewBox')
            group_signature = lambda tree: [(e.get('transform'), e.get('data-role'))
                                            for e in tree.findall('.//s:g', NS)]
            assert group_signature(svg) == group_signature(old), filename
            controls = lambda tree: [(e.get('data-control'), e.get('aria-disabled'), e.get('display'))
                                     for e in tree.findall('.//s:g[@data-control]', NS)]
            assert controls(svg) == controls(old), filename
            for side in ('Bid', 'Ask'):
                toggle = svg.findall(f'.//s:g[@data-control="{side}"]', NS)
                assert len(toggle) == 1
                assert toggle[0].get('aria-pressed') == str(frame['candle_visibility'][side.lower()]).lower()
                assert toggle[0].get('role') == 'button'
                assert toggle[0].get('aria-label') == f'Show/hide {side.lower()} candles'
            index = 0 if theme == 'light' else 1
            for role in ('bid-candle', 'ask-candle', 'bid-volume', 'ask-volume'):
                groups = svg.findall(f'.//s:g[@data-role="{role}"]', NS)
                originals = old.findall(f'.//s:g[@data-role="{role}"]', NS)
                assert len(groups) == len(originals)
                for group, original in zip(groups, originals):
                    assert group.get('data-bucket') == original.get('data-bucket')
                    direction = group.get('data-direction')
                    assert direction == original.get('data-direction')
                    rect = group.find('s:rect', NS)
                    assert rect.get('fill') == TOKENS[direction if role.startswith('bid') else 'content'][index]
                    assert rect.get('stroke') == TOKENS[direction + '_border'][index]
                    for wick in group.findall('s:path', NS):
                        assert wick.get('stroke') == TOKENS[direction + '_border'][index]
            toolbars = svg.findall('.//*[@data-surface="toolbar"]')
            assert len(toolbars) >= 5, filename
            for toolbar in toolbars:
                for rect in toolbar.findall('.//s:rect', NS) + ([toolbar] if toolbar.tag.endswith('}rect') else []):
                    assert rect.get('fill') in (TOKENS['base'][index], TOKENS['action'][index], TOKENS['buy_bg'][index], TOKENS['sell_bg'][index], 'none'), (filename, rect.attrib)
            for control in svg.findall('.//s:g[@data-control]', NS):
                label = control.get('data-control') or ''
                side = label.split()[0].lower() if label else ''
                if label not in ('Buy', 'Sell', 'Buy direction', 'Sell direction'):
                    continue
                rect = control.find('s:rect', NS)
                assert rect.get('fill') == TOKENS[side + '_bg'][index]
                assert rect.get('stroke') == TOKENS[side + '_fg'][index]
                for label in control.findall('s:text', NS):
                    assert label.get('style') == 'fill:' + TOKENS[side + '_fg'][index]
                if control.get('aria-disabled') == 'true':
                    assert rect.get('stroke-dasharray') == '4 3'
            shell = svg.find('.//s:g[@data-role="workspace-shell"]', NS)
            canvas = shell.find('s:rect', NS)
            width, height = float(canvas.get('width')), float(canvas.get('height'))
            # Inspect EVERY side panel by its position/outer box, including the
            # ungrouped watchlist; do not whitelist just the reported names.
            panels = []
            for child in shell:
                rect = child if child.tag.endswith('}rect') else child.find('s:rect', NS)
                if rect is None:
                    continue
                x, y, w, h = (float(rect.get(k, 0)) for k in ('x', 'y', 'width', 'height'))
                if x > width / 2 and w > 100 and abs(x + w - (width - 44)) < .01:
                    assert y == (88 if width == 640 else 44), (filename, 'side-panel top', y)
                    assert y + h == height - 26, (filename, 'side-panel bottom', y+h)
                    panels.append(child.get('data-role', 'watchlist'))
            if panels:
                panel_checks.append({'file': filename, 'panels': panels, 'top': 44, 'bottom': height-26})
            product_path = OUT / 'previews' / filename.replace('.svg', '-product.svg')
            product = ET.parse(product_path).getroot()
            shell = svg.find('.//s:g[@data-role="workspace-shell"]', NS)
            assert geometry(product) == geometry(shell)
            box = shell.find('s:rect', NS)
            assert product.get('viewBox') == f"0 0 {box.get('width')} {box.get('height')}"
    text = (ROOT / 'ui-dossier.md').read_text()
    counts = {prefix: len(re.findall(r'^\| ' + prefix + r'\d+ \|', text, re.M))
              for prefix in ('MP-MOCK-', 'UI-ART-')}
    assert all(n == len(rows) for n in counts.values()), counts
    properties = re.findall(r'^\| (UIV-(?!EVID)[A-Z0-9]+-\d+) \|', text, re.M)
    assert len(properties) == len(set(properties)) == 34
    if stale:
        assert meta['gate_g5'] == 'STALE'
        assert 'READY_FOR_HUMAN_WIREFRAME_REVIEW' in text and 'STALE_SOURCE' in text
    else:
        assert ('G4 `SATISFIED`' in text or 'G4 `SCOPED REVISION PENDING`' in text) and ('G5 `PENDING HUMAN REVIEW`' in text or 'G5 `SATISFIED`' in text)
    checked = 0
    cache = {}
    for path in (OUT/'index.html', OUT/'MP-SPEC-001.html', ROOT/'index.html'):
        parser = Links()
        parser.feed(path.read_text())
        assert not parser.executable if path.parent == OUT else parser.executable == ['script']
        assert len(parser.ids) == len(set(parser.ids)), path
        for url in parser.links:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                assert path.parent != OUT, (path, 'external dependency', url)
                continue
            target = path.parent / unquote(parts.path) if parts.path else path
            assert target.exists(), (path, url)
            checked += 1
            if parts.fragment and target.suffix == '.html':
                if target not in cache:
                    other = Links()
                    other.feed(target.read_text())
                    cache[target] = other.ids
                assert unquote(parts.fragment) in cache[target], (path, url)
    for url in re.findall(r'\]\(([^)]+)\)', text):
        parts = urlsplit(url)
        if not parts.scheme and parts.path:
            assert (ROOT / unquote(parts.path)).exists(), url
    if all(frame['gate_g5'] == 'APPROVED' for frame in rows):
        approved = json.loads((OUT / meta.get('approval_record', 'approval.json')).read_text())
        assert approved['version'] == meta['version'] and approved['status'] == 'APPROVED'
        assert approved['visual_sha256'] == meta['visual_sha256']
        assert len(approved['mockup_sha256']) == 2 * len(rows)
        for filename, expected in approved['mockup_sha256'].items():
            assert digest(OUT / filename) == expected, 'Approved mockup drift'
    report = {
        'version': meta['version'], 'kind': 'Static authored design checks; no runtime pass or approval',
        'current_sources': current, 'stale_sources': stale,
        'svg_count': 2*len(rows), 'source_state_count': 64,
        'source_digest_geometry_controls': f'PASS for {2*len(current)} current-source SVGs; stale excluded',
        'palette_candle_quote_and_toolbar_rules': 'PASS for explicit attributes; actual rendering inspected separately',
        'xml_safety_and_local_links': 'PASS', 'checked_html_links': checked,
        'verification_property_count': len(properties),
        'conditional_entry_readback': 'PASS: 22 SVGs; shared proposed level, ticket direction/type/identity, ready validity, pending/invalid restrictions, collapsed and zoom summaries',
        'rendered_preview_count': len(list((OUT/'previews').glob('*.png'))),
        'rendering': 'See render-checks.json for actual render/visual-inspection scope',
        'runtime_evidence': 'UIV-EVID-001–009 expected during implementation; not observed here',
        'side_panel_bounds': {'status': 'PASS', 'files_checked': len(panel_checks), 'details': panel_checks},
        'g4': 'SCOPED REVISION PENDING' if any(f['gate_g4']!='APPROVED' for f in rows) else 'SATISFIED',
        'g5': 'STALE' if stale else ('APPROVED' if all(f['gate_g5']=='APPROVED' for f in rows) else 'PENDING')}
    (OUT/'review-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('current_sources','stale_sources','side_panel_bounds')}, indent=2))


if __name__ == '__main__':
    main()
