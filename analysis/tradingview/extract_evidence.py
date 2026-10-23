"""Extract reviewable artifacts from the retained REA bundle, without network access.

Run from any directory: python analysis/tradingview/extract_evidence.py
The input is untrusted captured content. This script parses it as data only.
"""

import base64
import collections
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent
RUNS = [
    ("E01", "4472b012", "Baseline SPX", ["load-chart"]),
    ("E02", "b75f3be3", "Symbols intervals and chart styles", ["symbol-dialog", "intervals", "chart-types"]),
    ("E03", "937d697e", "Indicators and trend tools", ["indicator-loaded", "trend-tools"]),
    ("E04", "ab417925", "Settings and layout inventory with interrupted flow", ["layout"]),
    ("E05", "7c7ad5cc", "Alert replay and save registration gates", ["alert-state", "replay-state", "save-state"]),
    ("E06", "04c1dda1", "Object tree and Pine editor", ["objects-state", "pine-state"]),
    ("E07", "8a0dd827", "Settings canvas and broker chooser", ["settings-ready", "canvas-state", "trade-state"]),
    ("E08", "ca905101", "Daily to hourly change with interrupted style selection", []),
    ("E09", "ef5051fe", "Line style and indicator dialog DOM", ["indicator-dom"]),
    ("E10", "9885f2d2", "Drawing category inventories", ["fibonacci-state", "patterns-state", "measurements-state", "shapes-state", "annotations-state", "magnets-state"]),
    ("E11", "b68bbe66", "Indicator search with unmatched text locator", []),
    ("E12", "2ad85902", "Indicator search with unmatched built-in text locator", []),
    ("E13", "ac923bd0", "Horizontal line registration gate", ["place-line"]),
    ("E14", "07ba055b", "RSI search and stable DOM identity", ["search-results"]),
    ("E15", "b7fc1eae", "Built-in RSI registration gate", ["rsi-state"]),
    ("E16", "338a9188", "Narrow viewport with dark system preference", ["mobile-ready"]),
    ("E17", "a7336de1", "Main menu snapshot and data window", ["menu-state", "snapshot-state", "data-window-state"]),
    ("E18", "a0ff708c", "AAPL symbol selection and explicit dark theme", ["aapl-results", "symbol-state", "dark-state"]),
]


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.styles = []
        self.canvases = []
        self.inline_scripts = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script":
            if "src" in a:
                self.scripts.append(a["src"])
            else:
                self.inline_scripts += 1
        if tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a.get("href"))
        if tag == "canvas":
            self.canvases.append(a)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def decode_frames(events):
    """Parse length-framed messages; never treat partial previews as complete JSON."""
    out, failures = [], []
    for event in events:
        if not event["kind"].startswith("websocket-frame-"):
            continue
        payload = event.get("payload_text")
        if not isinstance(payload, str):
            continue
        if event.get("truncated"):
            failures.append({"sequence": event["sequence"], "reason": "truncated frame"})
            continue
        position = 0
        while position < len(payload):
            match = re.match(r"~m~(\d+)~m~", payload[position:])
            if not match:
                failures.append({"sequence": event["sequence"], "reason": "unframed remainder"})
                break
            start = position + match.end()
            length = int(match.group(1))
            # Observed protocol length counts JavaScript UTF-16 code units.
            units = 0
            end = start
            while end < len(payload) and units < length:
                units += 2 if ord(payload[end]) > 0xFFFF else 1
                end += 1
            if units != length:
                failures.append({"sequence": event["sequence"], "reason": "length mismatch"})
                break
            body = payload[start:end]
            position = end
            if body.startswith("~h~"):
                continue
            try:
                message = json.loads(body)
            except json.JSONDecodeError:
                failures.append({"sequence": event["sequence"], "reason": "non JSON message"})
                continue
            out.append({"event_sequence": event["sequence"], "direction": event["kind"], "message": message})
    return out, failures


def main():
    bundle_path = ROOT / "evidence/rea-session.json"
    bundle = json.loads(bundle_path.read_text())
    (ROOT / "evidence/accessibility").mkdir(exist_ok=True)
    (ROOT / "evidence/dom").mkdir(exist_ok=True)
    summary = []
    for short, prefix, title, selected in RUNS:
        record = next(r for r in bundle["records"] if r["evidence_id"].startswith("ev_" + prefix))
        steps = []
        for step in record["normalized_result"]["steps"]:
            files = {}
            for kind, directory, extension in [("accessibility", "evidence/accessibility", "txt"), ("dom", "evidence/dom", "html")]:
                artifact = step["artifacts"][kind]
                if artifact["state"] == "captured":
                    value = artifact["value"]
                    content = value["text"].encode()
                    assert hashlib.sha256(content).hexdigest() == value["sha256"]
                    relative = f"{directory}/{short}-{step['step_id']}.{extension}"
                    (ROOT / relative).write_bytes(content)
                    files[kind] = relative
            shot = step["artifacts"]["screenshot"]
            if step["step_id"] in selected and shot["state"] == "captured":
                content = base64.b64decode(shot["value"]["data_base64"], validate=True)
                assert hashlib.sha256(content).hexdigest() == shot["value"]["sha256"]
                relative = f"screenshots/{short}-{step['step_id']}.png"
                (ROOT / relative).write_bytes(content)
                files["screenshot"] = relative
            steps.append({"step_id": step["step_id"], "status": step["status"], "error": step.get("error"), "files": files})
        summary.append({"id": short, "evidence_id": record["evidence_id"], "title": title, "parameters": record["parameters"], "limitations": record["limitations"], "completeness": record["normalized_result"]["completeness"], "browser": record["normalized_result"]["browser"], "steps": steps})
    write_json(ROOT / "evidence/index.json", summary)
    baseline = next(r for r in bundle["records"] if r["evidence_id"].startswith("ev_4472"))
    events = baseline["normalized_result"]["events"]
    messages, decode_failures = decode_frames(events["items"])
    endpoint_rows = {}
    for event in events["items"]:
        if event["kind"] != "request":
            continue
        parts = urlsplit(event["url"]["url"])
        key = (event["method"], parts.netloc, parts.path)
        row = endpoint_rows.setdefault(key, {"method": key[0], "host": key[1], "path": key[2], "query_names": set(), "resource_types": set(), "observed_requests": 0})
        row["query_names"].update(parse_qs(parts.query))
        row["resource_types"].add(event.get("resource_type"))
        row["observed_requests"] += 1
    symbol = None
    quote = {}
    series = []
    names = collections.Counter()
    for row in messages:
        m = row["message"]
        if not isinstance(m, dict) or "m" not in m:
            continue
        names[(row["direction"], m["m"])] += 1
        p = m.get("p", [])
        if m["m"] == "symbol_resolved" and p[2].get("pro_name") == "SP:SPX":
            symbol = {k: p[2].get(k) for k in ["name", "full_name", "pro_name", "description", "exchange", "type", "timezone", "session", "session_display", "minmov", "pricescale", "has_intraday", "delay", "allowed_adjustment"]}
        if m["m"] == "qsd" and p[1].get("n") == "SP:SPX":
            quote.update({k: v for k, v in p[1].get("v", {}).items() if k in ["lp", "ch", "chp", "volume", "is_tradable", "provider_id", "update_mode", "value_unit_id", "current_session"]})
        if m["m"] == "timescale_update":
            for key, value in p[1].items():
                if isinstance(value, dict) and value.get("s"):
                    bars = value["s"]
                    series.append({"event_sequence": row["event_sequence"], "series_id": key, "row_count": len(bars), "first_row": bars[0], "last_row": bars[-1]})
    for row in endpoint_rows.values():
        row["query_names"] = sorted(row["query_names"])
        row["resource_types"] = sorted(row["resource_types"])
    html = baseline["normalized_result"]["steps"][-1]["artifacts"]["dom"]["value"]["text"]
    inventory = Inventory()
    inventory.feed(html)
    write_json(ROOT / "evidence/network-summary.json", {
        "evidence_id": baseline["evidence_id"],
        "scope": "E01 startup window only; no exhaustive API discovery or body replay",
        "events_retained": events["retained"], "events_dropped": events["dropped"],
        "event_kinds": dict(collections.Counter(e["kind"] for e in events["items"])),
        "message_counts": [{"direction": d, "message": n, "count": count} for (d, n), count in sorted(names.items())],
        "frame_decode_failures": decode_failures,
        "symbol_metadata": symbol, "selected_quote_metadata": quote,
        "series_windows": series,
        "http_endpoints": sorted(endpoint_rows.values(), key=lambda r: (r["host"], r["path"])),
        "dom_script_urls": inventory.scripts, "dom_stylesheet_urls": inventory.styles,
        "dom_inline_script_count": inventory.inline_scripts, "dom_canvas_count": len(inventory.canvases),
        "main_canvas_nodes": inventory.canvases[:7],
    })
    print(json.dumps({"records": len(summary), "selected_screenshots": sum("screenshot" in s["files"] for r in summary for s in r["steps"]), "decoded_frames_messages": len(messages), "decode_failures": len(decode_failures), "bundle_sha256": hashlib.sha256(bundle_path.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
