"""Validate authored low-fi artifacts offline; never execute captured evidence."""
import hashlib
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'ui-artifacts' / 'wireframes'
NS = {'s': 'http://www.w3.org/2000/svg'}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag not in ('script', 'iframe', 'object', 'embed')
        assert not any(key.startswith('on') for key in attrs)
        self.links.extend(attrs[key] for key in ('href', 'src') if key in attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])


def main():
    meta = json.loads((OUT / 'frame-index.json').read_text())
    rows = meta['frames']
    assert len(rows) == 113
    assert {f['view'] for f in rows} == set(range(1, 9))
    assert {f['state'] for f in rows} == set(range(1, 65))
    assert len({f['id'] for f in rows}) == len(rows)
    svgs = {}
    texts = {}
    for frame in rows:
        svg = ET.parse(OUT / frame['file']).getroot()
        svgs[frame['id']] = svg
        shell = svg.find('.//s:g[@data-role="workspace-shell"]', NS)
        assert shell is not None
        texts[frame['id']] = ' '.join(' '.join(shell.itertext()).split())
        assert svg.find('.//s:g[@data-role="persistent-chart"]', NS) is not None
        assert not any(svg.findall('.//s:' + tag, NS) for tag in ('script', 'foreignObject', 'image'))
        for element in svg.iter():
            assert not any(key.lower().startswith('on') for key in element.attrib)
        for side, key in (('Bid', 'bid'), ('Ask', 'ask')):
            toggles = shell.findall(f'.//s:g[@data-control="{side}"]', NS)
            assert len(toggles) == 1
            assert toggles[0].get('aria-pressed') == str(frame['candle_visibility'][key]).lower()
        assert frame['gate_g4'] in ('PENDING', 'APPROVED')
        assert 'basis ' + frame['basis'] in texts[frame['id']]
        # Screen geometry, independent of the explanatory margins.
        box = shell.find('s:rect', NS)
        width, height = float(box.get('width')), float(box.get('height'))
        for rect in shell.findall('.//s:rect', NS):
            x, y, w, h = (float(rect.get(k, '0')) for k in ('x', 'y', 'width', 'height'))
            assert w >= 0 and h >= 0
            assert x >= 0 and y >= 0 and x + w <= width + 6 and y + h <= height + 6, (frame['id'], x, y, w, h)
    def text(number):
        return texts[f'WF-FRAME-{number:03}']
    def action(number, name):
        return svgs[f'WF-FRAME-{number:03}'].find(f'.//s:g[@data-control="{name}"]', NS)
    assert 'No active historical run' in text(26)
    assert svgs['WF-FRAME-026'].find('.//s:g[@data-role="floating-replay-bar"]', NS) is None
    for number in (30, 31, 32):
        assert action(number, 'Play').get('aria-disabled') == 'true'
        assert action(number, 'Buy').get('aria-disabled') == 'true'
    # State 037 has separate known-resolved and unreconciled endpoints.
    for name in ('Start bar', 'Play', 'Step'):
        assert action(77, name).get('aria-disabled') == 'true'
        assert action(37, name).get('aria-disabled') == 'false'
    for name in ('Sell', 'Buy'):
        assert action(77, name).get('aria-disabled') == 'true'
    for name in ('Reconcile publication', 'Return paused', 'Evidence and provenance >'):
        assert action(77, name).get('aria-disabled') == 'false'
    assert 'blocked until reconciled' in text(77)
    assert 'Pending request I-009' in text(27)
    assert 'Completed decision [time]' in text(27)
    assert 'Submitted terms' in text(27) and 'Prior valid orders / positions retained' in text(27)
    assert 'Acceptance / fill not confirmed; save separate' in text(27)
    assert 'Evaluating event' in text(92)
    for number in (27, 92):
        for name in ('Start bar', 'Play', 'Step', 'Sell', 'Buy'):
            assert action(number, name).get('aria-disabled') == 'true'
    assert 'EV-027' in text(30) and 'Missing historical USD conversion' in text(30)
    assert action(30, 'Open original event') is not None
    assert 'Writer authority denied' in text(32)
    assert 'G-013' in text(55) and 'Actual cursor [earlier time]' in text(55)
    assert action(55, 'Cancel') is None and 'Cancel keeps' not in text(55)
    assert 'Save FAILED v13' in text(15) and 'outcome UNKNOWN' not in text(15)
    assert 'Save outcome UNKNOWN v13' in text(7)
    for number, label in ((78, 'Backup B-003'), (79, 'Layout L-002'), (80, 'Selected new input basis D-009')):
        assert label in text(number) and 'Destination' not in text(number)
    assert '10,000' in text(29) and '12,000 exceeds 10,000' in text(29)
    assert 'Modify Order O-008 / v2' in text(76) and action(76, 'Apply modification') is not None
    for number in (93, 94):
        assert 'Entry level [price input]' in text(number)
    assert 'Sizing: Risk %' in text(95)
    assert action(96, 'Buy').get('aria-disabled') == 'true'
    revised = (25,68,90,93,94,95,96)
    ready_buy = (25,68,90,93,94,95)
    for number in ready_buy:
        assert action(number,'Buy').get('aria-disabled') == 'false'
        assert action(number,'Sell').get('aria-disabled') == 'true'
        assert 'Sell unavailable: draft is Buy' in text(number)
    for number in (107,110,112):
        assert action(number,'Sell').get('aria-disabled') == 'false'
        assert action(number,'Buy').get('aria-disabled') == 'true'
        assert 'Buy unavailable: draft is Sell' in text(number)
    for number in (96,108,109,111,113):
        for side in ('Buy','Sell'):
            assert action(number,side).get('aria-disabled') == 'true'
        assert 'old estimates superseded' in text(number)
    for number in revised + tuple(range(107,114)):
        assert action(number,'Edit entry / direction').get('aria-disabled') == 'false'
        assert 'completed decision [time]' in text(number)
    assert 'retained levels invalid for Sell' in text(109)
    assert 'Select Buy' in text(93) and 'Select Sell' in text(93)
    baseline=json.loads((OUT/'revision-r13.json').read_text())['source_sha256']
    changed={f'WF-FRAME-{n:03}.svg' for n in revised}
    for name, sha in baseline.items():
        if name not in changed:
            assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==sha, ('Unrelated approved drift',name)
    assert sum(f['gate_g4']=='APPROVED' for f in rows) in (99,113)
    assert 'remainder 6,000' in text(97) and 'remainder 0' in text(98)
    for number in (99, 100, 101, 102):
        assert 'Data location' in text(number) and 'Dukascopy data folder' in text(number)
    for number in (100, 101):
        assert action(number, 'Apply folder').get('aria-disabled') == 'true'
    assert 'basis Bid' in text(103) and 'Visible: ask' in text(103)
    assert 'Bid OHLCV:' in text(104) and 'Ask OHLCV:' in text(104)
    both=svgs['WF-FRAME-104']
    assert action(104,'Bid').get('aria-pressed')=='true' and action(104,'Ask').get('aria-pressed')=='true'
    quote_groups={role:both.findall(f'.//s:g[@data-role="{role}"]',NS) for role in ('bid-candle','ask-candle','bid-volume','ask-volume')}
    assert len({len(groups) for groups in quote_groups.values()})==1
    assert len(quote_groups['bid-candle'])>=20
    for groups in zip(*quote_groups.values()):
        assert len({group.get('data-bucket') for group in groups})==1
        bid,ask,bv,av=(group.find('s:rect',NS) for group in groups)
        direction=groups[0].get('data-direction')
        assert direction in ('up','down')
        expected_fill='#bbb' if direction=='up' else '#444'
        expected_edge='#777' if direction=='up' else '#222'
        assert bid.get('fill')==expected_fill and bv.get('fill')==expected_fill
        assert bid.get('stroke')==expected_edge and ask.get('stroke')==expected_edge
        assert ask.get('fill')=='#fff' and av.get('fill')=='#fff'
        assert float(bid.get('x'))<float(ask.get('x'))
        assert bid.get('x')==bv.get('x') and ask.get('x')==av.get('x')
    for role in ('bid-candle','ask-candle'):
        assert {g.get('data-direction') for g in quote_groups[role]}=={'up','down'}
    assert 'Bullish / rising: light gray' in text(104)
    assert 'Candles hidden' in text(105) and 'Volume · Bid' in text(105)
    assert 'basis Ask' in text(106) and 'Volume · Ask' in text(106)
    checked_links = 0
    for page in (OUT / 'index.html', OUT / 'replay-review.html'):
        parser = Links()
        parser.feed(page.read_text())
        assert len(parser.ids) == len(set(parser.ids))
        for link in parser.links:
            url = urlsplit(link)
            assert not url.scheme and not url.netloc, link
            target = page.parent / unquote(url.path) if url.path else page
            assert target.exists(), (page, link)
            checked_links += 1
    revision=json.loads((OUT/'revision.json').read_text())
    approval_path=OUT/revision.get('approval_record','approval.json')
    if approval_path.exists():
        approval=json.loads(approval_path.read_text())
        if approval['version']==meta['version'] and all(f['gate_g4']=='APPROVED' for f in rows):
            assert approval['source_sha256']=={f['file']:hashlib.sha256((OUT/f['file']).read_bytes()).hexdigest() for f in rows}, 'Approved SVG drift'
    report = {
        'version': meta['version'], 'kind': 'Static Mode A design checks; no runtime, independent review or approval claim',
        'svg_count': len(rows), 'views': 8, 'original_states': 64,
        'xml_and_inert_content': 'PASS', 'visibility_basis_and_material_branch_checks': 'PASS',
        'product_rect_bounds': 'PASS', 'local_gallery_links': checked_links,
        'both_selected_scenario': 'PASS: both pressed; matched Bid/Ask candle and volume groups per bucket; filled Bid / hollow Ask; separate OHLCV; bullish light / bearish dark shades',
        'g4': 'APPROVED' if all(f['gate_g4']=='APPROVED' for f in rows) else 'PENDING HUMAN REVIEW',
        'g5': 'Seven r7 entry pairs STALE_SOURCE and seven added frames PENDING STAGE 2D; scoped propagation follows G4',
        'rendered_inspection': 'See revision.json for scoped render inspection; SVGs remain canonical',
        'runtime_evidence': 'Not observed',
        'source_sha256': {f['file']: hashlib.sha256((OUT / f['file']).read_bytes()).hexdigest() for f in rows},
    }
    (OUT / 'revision-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'PASS: {len(rows)} wireframes, 8 views, 64 states, material branch semantics and {checked_links} local links')


if __name__ == '__main__':
    main()
