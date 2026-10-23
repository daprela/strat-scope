"""Create a review derivative; original authenticated capture stays outside the ZIP.

Usage: python extract_authenticated_evidence.py /tmp/strat-scope-authenticated-rea-session.json
With no argument, regenerate extracts from the packaged review derivative.
Captured text is parsed as data and never executed.
"""
import base64
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parent
TITLES = [
    'Authenticated layout menu', 'New layout form', 'Create isolated inspection layout',
    'RSI duplicate locator failure', 'Add RSI and inspect outputs', 'RSI pointer interception',
    'RSI settings and save', 'Drawing placement undo redo and save', 'Drawing coordinate edit and contextual alert',
    'Price alert condition', 'Alert trigger and message', 'Alert notifications', 'Replay entry',
    'Historical replay step and speeds', 'Replay exit confirmation', 'Leave replay and layout menu',
    'Two charts and blocked switch locator', 'Blocked sync label locator', 'Working interval synchronization',
    'Reload multi-chart layout and restore single', 'Compile authored SMA indicator', 'Compiler diagnostic from entered indentation',
    'Compile authored strategy and report', 'Strategy trades and properties', 'Broker chooser',
    'Paper connection form', 'Connect simulator', 'SPX nontradable ticket', 'EURUSD market ticket',
    'Limit and stop tickets with blocked DOM click', 'Keyboard DOM ladder', 'Account manager and cleanup attempt',
    'Cleanup selector failure', 'Transient menu cleanup failure', 'Tooltip selector cleanup failure',
]
SHOTS = {
    'A05': ['data-state'], 'A07': ['inputs-state', 'style-state', 'visibility-state'],
    'A08': ['objects-state', 'drawing-dialog'], 'A09': ['coordinate-state', 'alert-state'],
    'A10': ['alert-form', 'condition-options'], 'A11': ['trigger-options', 'message-state'],
    'A12': ['notification-state'], 'A14': ['historical-state', 'forward-state', 'speed-options'],
    'A15': ['exit-state'], 'A19': ['sync-state', 'synced-state'], 'A20': ['restored-state'],
    'A21': ['compile-state'], 'A22': ['strategy-state'], 'A23': ['strategy-state'],
    'A24': ['report-state', 'trades-state', 'properties-state'], 'A28': ['ticket-state'],
}

def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def redact(text):
    for old, new in [('daprela', '[account]'), ('Real simulation USD', '[paper account]'),
                     ('🧑‍🎓Layout Morpheus per Studenti', '[existing layout]'), ('🐐Goat', '[existing layout]'),
                     ('Morpheus', '[existing layout]'), ('WDOU2PKE', 'EXISTING_LAYOUT'),
                     ('UEW6nYzD', 'EXISTING_LAYOUT'), ('hcl2sbij', 'EXISTING_LAYOUT')]:
        text = text.replace(old, new)
    text = re.sub(r'USER(?:%3[Bb]|;)[^/\s"?]+', 'USER;[script-id]', text)
    text = re.sub(r'99[,\u202f ]?989[.,]11|[−-]10[.,]89', '[account figure]', text)
    # Remove numerical account summary values, retaining labels and the grid shape.
    lines = text.splitlines()
    private_block = False
    for i, line in enumerate(lines):
        if 'text: Account balance' in line or 'text: Available margin' in line:
            private_block = True
        if private_block and re.search(r'\b(tab|grid|button|radio)\b', line):
            private_block = False
        if private_block and re.search(r'\d', line):
            lines[i] = re.sub(r'[\d,\.\u202f]+', '[omitted]', line)
    return '\n'.join(lines)

def scrub(value):
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items()}
    return value

def main():
    mapping = json.loads((ROOT / 'evidence/authenticated-map.json').read_text())
    derivative = ROOT / 'evidence/authenticated-review.json'
    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
        raw = source.read_bytes()
        bundle = json.loads(raw)
        records = {r['evidence_id']: r for r in bundle['records']}
        selected = []
        for row in mapping:
            original = records[row['evidence_id']]
            record = scrub(copy.deepcopy(original))
            for old_step, step in zip(original['normalized_result']['steps'], record['normalized_result']['steps']):
                for kind in ['accessibility', 'dom']:
                    art = step['artifacts'][kind]
                    if art['state'] == 'captured':
                        value = art['value']
                        original_value = old_step['artifacts'][kind]['value']
                        assert hashlib.sha256(original_value['text'].encode()).hexdigest() == original_value['sha256']
                        value['source_sha256'] = original_value['sha256']
                        value['sha256'] = hashlib.sha256(value['text'].encode()).hexdigest()
                        value['review_derivative'] = True
                shot = step['artifacts']['screenshot']
                if shot['state'] == 'captured':
                    value = shot['value']
                    pixels = base64.b64decode(value.pop('data_base64'), validate=True)
                    assert hashlib.sha256(pixels).hexdigest() == value['sha256']
                    if step['step_id'] in SHOTS.get(row['id'], []):
                        target = f"screenshots/authenticated/{row['id']}-{step['step_id']}.png"
                        (ROOT / target).parent.mkdir(parents=True, exist_ok=True)
                        (ROOT / target).write_bytes(pixels)
                        value['review_file'] = target
                    value['review_omission'] = 'Inline image bytes excluded; selected original images are linked separately.'
            selected.append(record)
        write(derivative, {'format': 'REA review derivative, not an original evidence bundle',
              'source_bundle_sha256': hashlib.sha256(raw).hexdigest(),
              'policy': 'Account names, existing layout identities, account summary figures and private script IDs are masked in text. Selected screenshots are original pixels and retain ordinary signed-in UI; account balance/ticket screenshots A29 onward are excluded. Image bytes are omitted from records. Evidence IDs identify original records; derivative text hashes are separate.',
              'records': selected})
    bundle = json.loads(derivative.read_text())
    records = {r['evidence_id']: r for r in bundle['records']}
    index, network = [], []
    for number, row in enumerate(mapping):
        record = records[row['evidence_id']]
        steps = []
        for step in record['normalized_result']['steps']:
            files = {}
            artifact = step['artifacts']['accessibility']
            if artifact['state'] == 'captured':
                content = artifact['value']['text'].encode()
                assert hashlib.sha256(content).hexdigest() == artifact['value']['sha256']
                relative = f"evidence/authenticated/accessibility/{row['id']}-{step['step_id']}.txt"
                (ROOT / relative).parent.mkdir(parents=True, exist_ok=True)
                (ROOT / relative).write_bytes(content)
                files['accessibility'] = relative
            shot = step['artifacts']['screenshot']
            if shot['state'] == 'captured' and shot['value'].get('review_file'):
                relative = shot['value']['review_file']
                assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == shot['value']['sha256']
                files['screenshot'] = relative
            steps.append({'step_id': step['step_id'], 'status': step['status'], 'action': step['action'], 'error': step.get('error'), 'files': files})
        result = record['normalized_result']
        index.append({**row, 'title': TITLES[number], 'date': '2026-10-16', 'review_derivative': True,
                      'parameters': record['parameters'], 'limitations': record['limitations'],
                      'completeness': result['completeness'], 'browser': result['browser'], 'steps': steps})
        if row['id'] in ['A21', 'A22', 'A23']:
            requests = []
            for event in result['events']['items']:
                if event.get('kind') != 'request':
                    continue
                parts = urlsplit(event['url']['url'])
                if parts.netloc != 'pine-facade.tradingview.com':
                    continue
                requests.append({'step_index': event['step_index'], 'sequence': event['sequence'],
                                 'method': event['method'], 'host': parts.netloc,
                                 'path': parts.path, 'query_names': list(parse_qs(parts.query))})
            network.append({'id': row['id'], 'evidence_id': row['evidence_id'], 'dropped': result['events']['dropped'], 'requests': requests})
    write(ROOT / 'evidence/authenticated-index.json', index)
    write(ROOT / 'evidence/authenticated-network-summary.json', {'scope': 'A21–A23 authored Pine probes only; endpoint metadata, no bodies, header values or websocket payloads. Does not alter E01 startup network summary.', 'captures': network})
    print(json.dumps({'scenarios': len(index), 'steps': sum(len(r['steps']) for r in index),
                      'screenshots': sum('screenshot' in s['files'] for r in index for s in r['steps'])}))

if __name__ == '__main__':
    main()
