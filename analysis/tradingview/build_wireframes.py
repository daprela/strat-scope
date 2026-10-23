"""Build authored, offline Stage 2C SVGs and their review gallery.

Design artifacts only: no production interface, market data or captured HTML.
The upstream state names remain sourced from Part III; compositions are authored
below. Run from any directory with Python's standard library.
"""

import calendar
import copy
import html
import json
import re
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ui-artifacts" / "wireframes"
VERSION = "WF-SET-001-r14"


def gate_status():
    """Keep regenerated metadata aligned with the canonical approval record."""
    source = (ROOT / "ui-dossier.md").read_text()
    return "APPROVED" if f"**Gate G4:** `APPROVED_FOR_HIGH_FI_DESIGN` — {VERSION}" in source else "PENDING"

# Logical region metadata: semantic ID, heading, content and scoped commands.
# These groups are not page layouts or parallel columns.
VIEWS = {
    1: ("Chart and replay workspace", [
        ("001", "Basis and navigation", ["Layout [name] / Active chart 1", "Dukascopy / EURUSD / M1 / Bid", "Candles / display timezone [selected]", "Archive [earliest] to [latest usable]", "Loaded range is only part of archive", "Search symbol, provider alias or name"], ["Select basis", "Go to date", "Pan / zoom", "Range / latest"]),
        ("002", "Chart, studies and inspection", ["Selected bar [time] / OHLC [values]", "Volume [value + provider qualifier]", "Studies [instance + warm-up/value]", "Watchlist [bounded observation times]", "Objects [type / hidden / locked]"], ["Previous / next bar", "Numeric inspector", "Draw / objects", "Configure"]),
        ("003", "Historical progression", ["Historical simulation / Run [identity]", "Retained original input basis [version]", "Actual cursor [time] / completed point", "Selected bar differs from run cursor", "Speed [selected] / step reference [chart]"], ["Play / pause", "Step bar", "Seek forward", "Rewind review", "Trading", "Exit replay"]),
    ]),
    2: ("Scoped configuration", [
        ("005", "Scope and committed settings", ["Simulation settings / Instrument EURUSD", "Committed settings [version]", "Selected run settings [retained version]", "Edits do not revalue retained results", "Return to original sizing input"], ["Analysis settings", "Simulation settings"]),
        ("006", "Editable draft", ["Initial balance [USD input]", "Sizing [fixed quantity / risk percent]", "Quantity [units] / SL [price] if required", "Commission [fixed USD / USD per unit / %]", "Metadata vs overrides [explicit source]", "Unit / multiplier / price increment", "Quantity increment / minimum [inputs]", "Estimate [quantity / planned risk / fees]", "Estimate is not a fill or maximum loss"], ["Expand specification", "Calculation detail"]),
        ("007", "Validation and commitment", ["Draft [version] / target [identity]", "Currency USD (fixed)", "Required facts and units before apply", "Applied working state differs from saved", "Incompatible run change requires restart"], ["Apply valid draft", "Cancel draft", "Review restart"]),
    ]),
    3: ("Layouts, retained work and recovery", [
        ("008", "Named work and arrangement", ["Layouts [names] / Runs [identities]", "Selected candidate [identity / version]", "Current layout [name] / Active chart 1", "Arrangement [one / two charts]", "Interval sync [on / off] (explicit)", "Selecting a candidate does not restore it"], ["Create / name layout", "Restore layout", "Resume run", "Arrange / sync"]),
        ("009", "Save and authority", ["Working state [version]", "Acknowledged retained state [version]", "Writer [writable / read-only + reason]", "Original run input closure [validated]", "Only identified checkpoint is saved", "Inspection never reissues trade commands"], ["Inspect checkpoint", "Save recovery", "Safe diagnostics"]),
        ("010", "Backup and replacement", ["Own backup includes [layouts / runs]", "Pinned retained generation [identity]", "Includes required original run inputs", "Newer unsaved work is not included", "Candidate [local file] / integrity [result]", "Restore replaces; no merge or credentials"], ["Make own backup", "Choose own backup", "Validate candidate", "Review replacement", "Review delete / reset"]),
    ]),
    4: ("Paper trading over replay", [
        ("012", "Entry draft", ["Simulated entry / EURUSD / Market", "Type [Market / Limit / Stop]", "Direction [Buy / Sell] / quantity [units]", "Level [if required] / SL / TP [optional]", "Buy uses ask / sell uses bid", "Size [quantity] / planned risk [USD]", "Estimated commission [USD + basis]", "Effective after this completed decision", "Acceptance is not a fill"], ["Submit entry", "Simulation settings"]),
        ("013", "Independent positions", ["Selected position [identity / version]", "Direction [long / short] / EURUSD", "Remaining quantity [units]", "Protection [SL / TP and quantities]", "Close [partial quantity / full remainder]", "Long exit sells bid; short exit buys ask", "Estimated exit fee [USD]", "Opposite entry creates separate exposure"], ["Request targeted close", "Orders / modify / cancel"]),
        ("014", "Recorded results and evidence", ["Filter [own run / selected execution]", "State [accepted / triggered / filled]", "Fill [event time / side / price / units]", "Entry / exit fees [USD] / result [USD]", "Metrics [recorded value / absent reason]", "ASM-01: stop-first if unresolved SL/TP", "ASM-02: full-fill / bar-touch assumption", "Original FX / spec / bar / tick provenance"], ["Inspect execution", "Open original block", "Own-run report"]),
    ]),
    5: ("Original historical-event resolution", [
        ("015", "Original event held", ["Run [identity] / retained input [version]", "Original event [identity / time]", "Instrument / side / instruction [target]", "Last coherent prefix [boundary]", "Missing historical USD conversion", "No new partial execution effects", "Dismissal does not resolve this block"], ["Return paused"]),
        ("016", "Evidence and applicability", ["Needed fact [historical pair / time]", "Retained applicable source [identity]", "Compatibility [pending validation]", "Price gaps require qualified evidence", "Finer stored bars before local ticks", "No automatic missing-tick download", "Stop-first cannot replace missing FX"], ["Inspect evidence", "Data continuity", "Specification detail"]),
        ("017", "Qualified resolution", ["Reevaluate original occurrence only", "Same historical price context", "Whole effect publishes with resolution", "Updated basis requires explicit restart", "Remain paused on unknown prerequisite", "No automatic playback after resolution"], ["Resolve when compatible", "Review updated restart", "Return to run"]),
    ]),
    6: ("Data continuity and access", [
        ("018", "Data-only access", ["Dukascopy / access [verified condition]", "Data receipt [local receipt time]", "Observation event [event time]", "Receiving is not complete history", "History remains available locally", "No account figures or credentials"], ["Qualified reconnect", "Return to origin"]),
        ("019", "Coverage and publication", ["EURUSD / Bid / M1 + H1 recovery", "Requested span [start / end]", "Qualified subset [intervals]", "Unresolved remainder [intervals + reason]", "Provisional / completed / final distinct", "Current catalog [published version]", "Saved run retains original input basis"], ["Inspect spans", "Inspect lineage"]),
        ("020", "Recovery and diagnostics", ["Reason [qualified feed / coverage fact]", "Known phase [discovery / catch-up]", "No unsupported deadline or percentage", "Receipt / display / retention separate", "Safe correlation [identifier only]"], ["Qualified retry", "Safe diagnostics", "Return to block"]),
    ]),
    7: ("Replay and saved-work actions", [
        ("021", "Rewind consequence", ["Run [identity] / expected [version]", "Current cursor [time]", "Proposed earlier destination [time]", "Discard later trading actions and effects", "Retain coherent prefix [boundary]", "Layout/instrument drawings untouched", "No automatic discarded-state archive"], []),
        ("022", "Validate exact scope", ["Operation: trading rewind", "Original retained input basis [version]", "Required original inputs [validated]", "Target/version must still match", "Old state authoritative until publication", "Changed scope requires new review"], ["Inspect scope"]),
        ("023", "Confirm or cancel", ["Review target and consequence first", "Confirm prepares whole replacement", "Preparation is not published success", "Cancel preserves old state before publish", "Unknown outcome requires reconciliation"], ["Confirm rewind", "Cancel review"]),
    ]),
    8: ("Results and local export", [
        ("024", "Pinned source and kind", ["Kind: own-run report", "Own run [identity / retained input basis]", "Source snapshot [version / cursor]", "Original invoking result [identity]", "Changing workspace does not repin output"], ["Chart image", "Own-run report"]),
        ("025", "Included content and evidence", ["Recorded outcomes through pinned cursor", "Units / fees / USD result [recorded]", "Original historical FX / specifications", "ASM-01 stop-first; ASM-02 full-fill", "Bar / tick evidence and limitations", "Unavailable metrics retain their reasons", "No later observations or secret material"], ["Review inclusion", "Extended provenance"]),
        ("026", "Local artifact outcome", ["Pinned source [version]", "Artifact [not generated]", "Complete only after matching verification", "Incomplete / failed / unknown distinct", "Source analysis/run stays unchanged"], ["Generate local report", "Cancel output"]),
    ]),
}

# State-specific safety message, next-action label, availability, content change.
# Placeholders are intentional: no invented price, fee, multiplier, FX or risk.
STATES = {
    1: ("Ready: selected basis and bounded observations", "Inspect selected bar", True),
    2: ("Loading requested basis; retained plot keeps its old identity", "Cancel pending inspection", True),
    3: ("Actual coverage end: no later usable bars; positions remain open", "Change range / basis", True),
    4: ("Offline: qualified local history remains readable", "Inspect continuity", True),
    5: ("Blocked at original event: historical prerequisite missing", "Open original event", True),
    6: ("Drawing preview: invalid anchor; committed object unchanged", "Correct / cancel preview", True),
    7: ("Save outcome unknown: working effects differ from retained checkpoint", "Reconcile saved state", True),
    8: ("Read-only: another writer owns mutations; inspection available", "Inspect authority", True),
    9: ("Ready: review this draft before applying to the named scope", "Apply valid draft", True),
    10: ("Calculating draft estimate; prior committed settings retained", "Apply (estimate pending)", False),
    11: ("Missing historical specification or FX: estimate unavailable", "Apply (required fact missing)", False),
    12: ("Invalid quantity: required unit/constraint shown at the field", "Apply (invalid draft)", False),
    13: ("Target changed: old estimate superseded; review current scope", "Apply (review required)", False),
    14: ("Metadata offline: valid retained settings remain inspectable", "Review local settings", True),
    15: ("Draft applied to working state; save failed for this version", "Open save recovery", True),
    16: ("Target unavailable or writer denied: configuration read-only", "Apply (restricted)", False),
    17: ("Ready: selected candidate and current work remain distinct", "Inspect selected work", True),
    18: ("No retained layouts or runs; no checkpoint exists", "Create named layout", True),
    19: ("Validating candidate input closure; old generation retained", "Restore (validation pending)", False),
    20: ("Newer working state is unsaved; backup includes older checkpoint", "Inspect retained version", True),
    21: ("Publication outcome unknown; conflicting writes suspended", "Reconcile generation", True),
    22: ("Required original inputs missing/corrupt; affected resume unavailable", "Choose coherent own backup", True),
    23: ("Backup rejected: input closure or integrity validation failed", "Choose valid own backup", True),
    24: ("Read-only writer restriction; local inspection remains available", "Inspect authority", True),
    25: ("Paused completed decision: valid entry/target can be reviewed", "Review entry draft", True),
    26: ("No active run: no invented orders, positions or results", "Choose start / resume", True),
    27: ("Submitting same intent: no duplicate decision or advance", "Submit (pending original intent)", False),
    28: ("Accepted waiting: instruction recorded; no fill claimed", "Inspect accepted instruction", True),
    29: ("Target conflict: requested close exceeds current remainder", "Review current remainder", True),
    30: ("Execution blocked at original event; no partial new effect", "Open original event", True),
    31: ("Command outcome unknown: reconcile original occurrence first", "Reconcile same intent", True),
    32: ("Read-only run: retained evidence readable; mutations denied", "Inspect authority", True),
    33: ("Blocked: original event and missing historical FX retained", "Inspect required evidence", True),
    34: ("Loading prerequisite evidence; original block persists", "Resolve (evidence pending)", False),
    35: ("Evidence inapplicable to original time; required fact absent", "Resolve (no valid prerequisite)", False),
    36: ("Applying whole original-event effect; no new decision yet", "Resolve (already applying)", False),
    37: ("Resolved: whole original effect recorded; playback stays paused", "Inspect recorded effect", True),
    38: ("New evidence changes committed basis; cannot mix into this run", "Review updated-data restart", True),
    39: ("Read failed/offline: retained evidence remains readable", "Qualified evidence retry", True),
    40: ("Historical explanation: event/epoch no longer current", "Return to current run", True),
    41: ("Receiving: feed receipt does not certify complete coverage", "Inspect qualified coverage", True),
    42: ("Partial catch-up: requested span exceeds qualified subset", "Inspect unresolved spans", True),
    43: ("No recent receipt: freshness unknown; closure unproven", "Inspect session evidence", True),
    44: ("Coverage conflict: prior qualified catalog preserved", "Inspect conflicting span", True),
    45: ("Offline/rate-limited: local qualified history remains usable", "Qualified reconnect when allowed", True),
    46: ("Live access unverified/denied; historical work remains usable", "Inspect protected setup prerequisite", True),
    47: ("Catalog publication unknown: receipt is not retained success", "Reconcile catalog publication", True),
    48: ("Replay inspection: later price facts withheld; authority checked", "Return to historical run", True),
    49: ("Review exact target, discarded suffix and retained basis", "Confirm rewind", True),
    50: ("Required original inputs absent; confirmation unavailable", "Confirm (validation failed)", False),
    51: ("Target version changed: previous proposal invalidated", "Review revised scope", True),
    52: ("Reconstructing confirmed replacement; old state authoritative", "Confirm (preparation underway)", False),
    53: ("Cancelled before publication: original cursor/state unchanged", "Return to original run", True),
    54: ("Replacement outcome unknown: reconcile old/new generation", "Reconcile active generation", True),
    55: ("Replacement published: surviving state has fresh authority", "Open surviving work", True),
    56: ("Writer denied: old work unchanged; confirmation unavailable", "Confirm (restricted authority)", False),
    57: ("Ready: source, cursor and inclusion reviewed before output", "Generate local report", True),
    58: ("No recorded outcomes: empty history is not zero profit", "Generate (source absent)", False),
    59: ("Writing pinned snapshot; source workspace unchanged", "Generate (already writing)", False),
    60: ("Workspace advanced; output still uses original pinned source", "Continue pinned output", True),
    61: ("Output incomplete: matching complete artifact not established", "Retry same pinned snapshot", True),
    62: ("Artifact outcome unknown: verify before repeat or success", "Verify existing artifact", True),
    63: ("Verified complete: local artifact matches pinned snapshot", "Return to selected result", True),
    64: ("Source disclosure invalid: excluded content cannot be exported", "Generate (invalid scope)", False),
}


def esc(value):
    return html.escape(str(value), quote=True)


class Canvas:
    def __init__(self, width, height, title):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{esc(title)}</title><desc id="desc">Offline low-fidelity design. Bracketed values are semantic placeholders. Chart marks are schematic, not market evidence.</desc>',
                      '<style>text{font-family:system-ui,sans-serif;fill:#171717;font-size:14px} .meta{font-size:12px} .heading{font-size:16px;font-weight:600} .title{font-size:20px;font-weight:600}</style>']
        self.rect(0, 0, width, height, "#e9e9e9")

    def rect(self, x, y, w, h, fill="#fff", dash=False, weight=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#555" stroke-width="{weight}"{chr(32) + "stroke-dasharray=\"5 4\"" if dash else ""}/>')

    def text(self, x, y, value, cls="", width=90):
        lines = textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False) or [""]
        for i, line in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y+i*20}" class="{cls}">{esc(line)}</text>')
        return y + len(lines) * 20

    def button(self, x, y, w, label, enabled=True):
        self.rect(x, y, w, 48, "#fff" if enabled else "#e7e7e7", dash=not enabled)
        self.text(x + 8, y + 19, label, "meta", width=max(12, int((w-16)/6.5)))

    def finish(self):
        return "\n".join(self.parts) + "\n</svg>\n"


def source_states():
    source = (ROOT / "ui-dossier.md").read_text()
    return {int(n): (name.strip(), change.strip(), recovery.strip()) for n, name, change, recovery in
            re.findall(r"^\| UIS-STATE-(\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", source, re.M)}


def panel_content(view, state, variant):
    # Copy authored rows; semantic content can change without mutating the source.
    panels = [(r, h, list(lines), list(actions)) for r, h, lines, actions in VIEWS[view][1]]
    if state in (2, 3, 5, 6, 8):
        reason = {2: "Requested [new basis] pending / retained [old basis]", 3: "No later usable bar: archive end (not paging)", 5: "This panel not ready at common boundary: unavailable", 6: "Preview [object]: anchor invalid / correct before commit", 8: "Read-only / object inspection available; editing denied"}[state]
        panels[1][2].insert(0, reason)
    if state == 6 or variant == "anchors":
        panels[1] = ("002", "Drawing point editor - preview", ["Layout / instrument / object [identity]", "Type [brush] / uncommitted point sequence", "Point [selected] / time [input] / price [input]", "Add / select / edit / remove point", "Error: anchor must satisfy declared constraint", "Locked / hidden objects retain named identity", "Long/short measurement is analysis, not order"], ["Commit valid drawing", "Cancel preview", "Undo [analysis edit]"])
    if variant == "current-history":
        panels[2] = ("003", "Current-history mode", ["No active replay boundary", "Selected bar [time] / actual archive bounds", "Latest navigation uses qualified history", "Feed condition separate from save state", "Starting a run selects valid start/basis", "Saved runs remain available separately"], ["Start historical run", "Choose retained run", "Data continuity"])
    if variant == "selection":
        panels[0] = ("001", "Search and requested selection", ["Query [symbol / provider alias / name]", "Candidate [local + provider identity]", "Requested basis differs from adopted", "Periods M1/M5/M15/H1/H4/D1/W1/MN1", "Quote side [Bid default / Ask]", "No match: change query; no substitution"], ["Adopt matching basis", "Cancel selection"])
        panels[1][2][0] = "Retained adopted chart keeps old identity until match"
    if state in (10, 11, 12, 13, 16):
        panels[1][2][-2:] = ["Estimate unavailable: " + STATES[state][0].split(":", 1)[-1].strip(), "Committed valid settings unchanged"]
    if variant == "analysis":
        panels[0] = ("005", "Analysis target and committed values", ["Chart 1 / study [instance]", "Committed [settings version]", "Draft preview is not saved", "Return to invoking study/chart control"], ["Presentation", "Study settings"])
        panels[1] = ("006", "Analysis draft and preview", ["Type [candles / line] / timezone [selected]", "Precision [display only] / light or dark", "Study [SMA / EMA / RSI / MACD / BB]", "Inputs [declared parameters; no numeric default]", "Pane / overlay [supported placement]", "Warm-up / unavailable reason [explicit]", "Source UTC buckets and values unchanged"], ["Preview settings", "Hide / show study", "Remove study"])
        panels[2][2][:] = ["Target chart/study [identity]", "Field-level validity [reason]", "Apply to selected analysis only", "Cancel restores committed settings", "No simulation terms in analysis task"]
        panels[2][3][:] = ["Apply valid draft", "Cancel draft"]
    if state == 18:
        panels[0][2][:] = ["No named layouts / no retained runs", "No checkpoint to resume", "Create initial supported analysis", "Initial symbol/period not selected here"]
        panels[0][3][:] = ["Create named layout"]
    if state in (19, 22, 23):
        panels[2][2].insert(0, {19: "Candidate validation pending: no activation", 22: "Original run input closure incomplete", 23: "REJECTED candidate / reason [validation fact]"}[state])
        panels[2][3][:] = ["Choose own backup", "Inspect validation reason"]
    if state in (21, 24):
        panels[0][3][:] = ["Inspect selected work"]
        panels[2][3][:] = ["Inspect backup scope"]
    if state == 26:
        for _, _, lines, actions in panels:
            lines[:] = ["No active historical run", "No positions / orders / recorded results", "Start or resume a valid retained run"]
            actions[:] = []
    if state == 28 or variant == "pending":
        panels[0] = ("012", "Selected pending instruction", ["Order [identity / current version]", "Original valid terms [side / type / units]", "State: accepted waiting (not filled)", "Effective after [completed boundary]", "Modification draft [levels / quantity]", "Trigger differs from execution price", "Rejected edit preserves valid old terms"], ["Modify selected order", "Cancel selected order"])
    if state == 29:
        panels[1][2].insert(0, "ERROR: close quantity exceeds current remainder")
        panels[1][3][:] = ["Review remainder / correct quantity"]
    if state == 31:
        panels[0][3][:] = ["Reconcile original intent"]
        panels[1][3][:] = ["Inspect target (no repeat close)"]
    if state == 32:
        panels[0][3][:] = ["Inspect terms (read-only)"]
        panels[1][3][:] = ["Inspect position (read-only)"]
    if state in (34, 35, 38, 39, 40):
        panels[1][2].insert(0, STATES[state][0])
        panels[2][3][:] = ["Remain paused", "Return to current run"]
        if state == 38:
            panels[2][3].insert(0, "Review updated restart")
    if state in (36, 37):
        panels[2][2][:] = ["Original event [identity / time]", "Whole execution [pending]" if state == 36 else "Whole recorded effect [execution identity]", "Quantity / fee / USD [pending or recorded]", "Working effect vs retained checkpoint [status]", "Playback remains paused"]
        panels[2][3][:] = ["Inspect effect", "Return paused"] if state == 37 else ["Wait for original outcome"]
        if state == 37:
            panels[0] = ("015", "Original event record", ["Run [identity] / retained input [version]", "Original event [identity / time]", "Former block: historical FX (resolved)", "Whole effect recorded at original occurrence", "Current coherent boundary [time]", "No automatic playback"], ["Return paused"])
            panels[1][2][2] = "Compatibility: established for this effect"
    if variant == "resolution-unknown":
        panels[0] = ("015", "Original event and known prefix", ["Run [identity] / retained input [version]", "Original event [identity / time]", "Former missing prerequisite [reason]", "Applicable evidence [identity]", "Known prefix [time]; publication unknown"], ["Return paused"])
        panels[2][2][:] = ["Outcome unknown: original resolution [identity]", "Whole publication must be reconciled", "Do not infer effect or rollback", "No second resolution or new decision"]
        panels[2][3][:] = ["Reconcile original publication", "Return paused"]
    if state == 46:
        panels[0][2][:] = ["Dukascopy data-only access: unverified/denied", "Protected integration setup prerequisite", "No credential-entry UI prescribed here", "Qualified local history remains available"]
        panels[0][3][:] = ["Inspect access reason", "Return to history"]
    if state == 48:
        panels[0][2][:] = ["Replay-origin inspection / Run [identity]", "Operational connection/receipt condition only", "Later event times and price facts withheld", "Revoked authority cannot publish callbacks"]
        panels[1][2][:] = ["Requested historical series/span [bounded]", "Run input basis [retained version]", "Operational catch-up phase [condition]", "No later OHLC or derived metrics", "Explicit exit needed for latest-price view"]
        panels[0][3][:] = ["Return to replay", "Explicit exit to history"]
    if variant in ("restore", "delete", "restart"):
        operation = {"restore": "Restore own backup", "delete": "Delete selected layout", "restart": "Restart with updated data"}[variant]
        panels[0] = ("021", operation + " consequence", ["Exact target [identity / version]", "Current owned scope [items affected]", {"restore": "Replace included analysis/runs; no merge", "delete": "Delete named layout and its owned analysis", "restart": "Discard later trading actions/results"}[variant], "Unrelated work stays outside this scope", "No automatic archive promised"], [])
        panels[1] = ("022", "Validated replacement scope", ["Operation: " + operation, "Expected old generation [version]", "Candidate / new basis [validated version]", "Original input closure [complete]", "No credentials or capabilities restored", "Old generation retained until publication"], ["Inspect scope"])
        panels[2][3][:] = ["Confirm " + variant, "Cancel review"]
    if state in (50, 51, 52, 53, 54, 55, 56):
        panels[2][3][:] = [STATES[state][1]]
        if state in (50, 51, 56):
            panels[2][3].append("Cancel review")
        if state == 50:
            panels[1][2][2] = "Required original inputs: missing / invalid"
        if state == 51:
            panels[1][2][3] = "Target/version changed: old proposal invalid"
        if state == 52:
            panels[2][2].append("Cancel preparation only before publication")
        if state == 54:
            panels[2][2][:] = ["Old/new active generation unknown", "No assumed rollback or success", "Further replacement unavailable", "Reconcile whole generation before repeat"]
        if state == 55:
            panels[2][2][:] = ["New surviving generation [identity]", "Cursor / mode [known actual values]", "Fresh authority [scope]", "No promise of discarded-state archive"]
    if state in (58, 59, 60, 61, 62, 63, 64):
        panels[2][2].insert(0, STATES[state][0])
        panels[2][3][:] = [STATES[state][1], "Return to source"]
    if state == 58:
        panels[1][2][:] = ["No recorded result history", "Metrics unavailable: no observations", "No profit figure inferred from emptiness"]
    if variant == "image":
        panels[0][2][:] = ["Kind: local chart image", "Chart 1 / Dukascopy / EURUSD / Bid / M1", "Source viewport [range / snapshot version]", "Mode / actual cursor [bounded]", "Return to original chart/range"]
        panels[1][2][:] = ["Intended chart / studies / drawings", "Readable identity, side, period and legend", "Provider-volume qualifier", "Visible gaps / warm-up / unavailable labels", "No later replay observations", "Source image geometry [declared options]"]
        panels[2][3][:] = ["Generate local chart image", "Cancel output"]
    return panels


def line(c, x1, y1, x2, y2, dash=False, stroke="#777"):
    c.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{stroke}"' + (' stroke-dasharray="4 4"' if dash else '') + '/>')


def control(c, x, y, w, label, enabled=True, selected=False, h=30, toggle=False):
    wrap=max(10, int((w-16)/6.8))
    if len(textwrap.wrap(label,width=wrap,break_long_words=False))>1:
        h=max(h,48)
    pressed=f' role="button" aria-pressed="{str(selected).lower()}" aria-label="Show/hide {esc(label.lower())} candles"' if toggle else ''
    c.parts.append(f'<g data-control="{esc(label)}" aria-disabled="{str(not enabled).lower()}"{pressed}>')
    c.rect(x, y, w, h, "#dedede" if selected else "#fff" if enabled else "#eee", dash=not enabled)
    c.text(x+8, y+20, label, "meta", width=wrap)
    if toggle and selected:
        c.parts.append(f'<path d="M{x+w-15} {y+15} l3 3 l5 -7" fill="none" stroke="#333" stroke-width="1.5"/>')
    c.parts.append('</g>')


def field(c, x, y, w, label, value, enabled=True):
    c.text(x, y+14, label, "meta", width=max(20, int(w/7)))
    c.rect(x, y+22, w, 30, "#fff" if enabled else "#eee", dash=not enabled)
    c.text(x+8, y+42, value, "meta", width=max(18, int((w-16)/7)))


def tool_icon(c, x, y, kind, label, selected=False, disabled=False):
    c.parts.append(f'<g role="img" aria-label="{esc(label)}" aria-disabled="{str(disabled).lower()}"><title>{esc(label)}</title>')
    if selected or disabled:
        c.rect(x+4, y+3, 32, 32, "#ddd" if selected else "#eee", dash=disabled)
    paths = {
        "cross": "M20 8 V30 M9 19 H31", "trend": "M10 28 L30 10 M9 27 h3 v3 h-3 Z M28 8 h3 v3 h-3 Z",
        "horizontal": "M8 20 H32", "vertical": "M20 8 V31",
        "ray": "M9 29 L31 7 M9 27 h3 v3 h-3 Z",
        "fib": "M8 10 H32 M8 17 H27 M8 24 H32 M8 30 H25 M11 9 L28 31",
        "rectangle": "M9 10 H31 V29 H9 Z", "brush": "M8 28 Q18 2 23 17 Q29 30 32 9",
        "measure": "M9 28 L28 9 L33 14 L14 33 Z M15 23 L19 27 M20 18 L24 22",
        "list": "M10 9 H30 V31 H10 Z M14 15 H26 M14 21 H26 M14 27 H23",
        "trade": "M10 13 H30 L25 8 M30 25 H10 L15 30",
        "objects": "M8 18 L20 10 L32 18 L20 26 Z M8 24 L20 32 L32 24",
        "data": "M9 30 V17 M16 30 V9 M23 30 V20 M30 30 V13",
        "work": "M8 12 H18 L21 16 H32 V30 H8 Z",
        "output": "M10 24 V31 H31 V24 M20 8 V25 M14 14 L20 8 L26 14",
        "bundle": "M9 13 L20 7 L31 13 V27 L20 33 L9 27 Z M9 13 L20 20 L31 13 M20 20 V33",
        "settings": "M10 12 H31 M10 21 H31 M10 30 H31 M17 8 V16 M25 17 V25 M16 26 V34",
    }
    if kind == "text":
        c.text(x+14, y+27, "T", "title")
    else:
        c.parts.append(f'<path transform="translate({x},{y})" d="{paths.get(kind, paths["list"])}" stroke="#333" stroke-width="1.4" fill="none"/>')
    c.parts.append('</g>')


def chart(c, x, y, w, h, replay=False, state=1, active=True, chart_number=1, controller_h=0, selecting=False, visibility="bid", basis="Bid"):
    """Schematic full chart, including axes and provider-labelled volume."""
    assert w >= 240 and h >= 200
    c.parts.append(f'<g id="chart-{chart_number}" data-role="persistent-chart">')
    c.rect(x, y, w, h, "#fff", weight=2 if active and chart_number==2 else 1)
    c.text(x+12, y+23, f'{"Active " if active else ""}Chart {chart_number} · EURUSD · M1 · Dukascopy · basis {basis}', "meta", width=int((w-24)/7))
    if visibility!='both':c.text(x+12, y+45, f'Calculations: {basis} · OHLC / studies / volume [{basis} values] · selected [time]', "meta", width=int((w-24)/7))
    if visibility=='both':
        c.text(x+12,y+45,'Bid OHLCV: O [open] H [high] L [low] C [close] V [volume]','meta',width=int((w-24)/7))
        c.text(x+12,y+65,'Ask OHLCV: O [open] H [high] L [low] C [close] V [volume]','meta',width=int((w-24)/7))
    if replay:c.text(x+12,y+61,'Select starting bar [time]' if selecting else ('Replay · R-014 · G-013 · Paused · cursor [earlier time]' if state==55 else 'Replay · R-014 · current cursor unavailable; reconcile' if state==54 else 'Replay · run [id] · cursor [time]'),'meta',width=int((w-24)/7))
    header_extra=26 if visibility=='both' else 0
    px, py, pw, ph = x+10, y+66+header_extra, w-68, h-136-controller_h-header_extra
    c.parts.append(f'<rect data-role="plot-area" x="{px}" y="{py}" width="{pw}" height="{ph}" fill="none" stroke="none"/>')
    for i in range(1,6):
        gy=py+ph*i/6
        line(c, px, gy, px+pw, gy, dash=True, stroke="#dedede")
        c.text(px+pw+8, gy+4, '[price]', 'meta')
    for i in range(1,7):
        gx=px+pw*i/7
        line(c, gx, py, gx, py+ph, dash=True, stroke="#e5e5e5")
    # These marks are explicitly labelled schematic in the external review header.
    visible_pw=pw*(.58 if selecting else .82) if replay else pw
    n=max(20,int(visible_pw/(24 if visibility=='both' else 12)))
    for i in range(n):
        bx=px+12+i*(visible_pw-28)/n
        wave=((i*13)%37)-18
        by=py+ph*.66-i*ph*.004+wave*ph*.003
        body=6+(i*7)%14
        direction='up' if i%3 else 'down'
        body_shade='#bbb' if direction=='up' else '#444'
        edge_shade='#777' if direction=='up' else '#222'
        for side in ('bid','ask'):
            if visibility not in (side,'both'):continue
            cx=bx+(9 if side=='ask' and visibility=='both' else 0)
            cy=by-(5 if side=='ask' else 0)
            c.parts.append(f'<g data-role="{side}-candle" data-bucket="{i}" data-direction="{direction}">')
            line(c,cx+2.5,cy-9,cx+2.5,cy+body+9,stroke=edge_shade)
            fill=body_shade if side=='bid' else '#fff'
            c.parts.append(f'<rect x="{cx}" y="{cy}" width="5" height="{body}" fill="{fill}" stroke="{edge_shade}" stroke-width="1.5"/>')
            # Open is the left tick, close the right; direction is independent of quote-side fill.
            op,cl=(cy+body,cy) if i%3 else (cy,cy+body)
            line(c,cx-2,op,cx,op,stroke=edge_shade)
            line(c,cx+5,cl,cx+7,cl,stroke=edge_shade)
            c.parts.append('</g>')
        volume_sides=('bid','ask') if visibility=='both' else (basis.lower(),)
        for side in volume_sides:
            vx=bx+(9 if side=='ask' and visibility=='both' else 0)
            vh=10+((i*17+(11 if side=='ask' else 0))%max(15,int(ph*.13)))
            c.parts.append(f'<g data-role="{side}-volume" data-bucket="{i}" data-direction="{direction}">')
            fill=body_shade if side=='bid' else '#fff'
            c.parts.append(f'<rect x="{vx}" y="{py+ph-vh}" width="5" height="{vh}" fill="{fill}" stroke="{edge_shade}"/>')
            c.parts.append('</g>')
    c.text(px+4,py+ph-85,'Volume · Bid filled / Ask hollow · provider-qualified' if visibility=='both' else f'Volume · {basis} · provider-qualified','meta',width=int(pw/7))
    c.text(px+4,py+20,'Retained before-snapshot G-012; current values unavailable' if state==54 else {'bid':'Bid: filled body · open left / close right ticks','ask':'Ask: hollow body · open left / close right ticks','both':'Bid filled left / Ask hollow right · same UTC bucket','none':'Candles hidden · calculations retained on named basis'}[visibility],'meta',width=int(pw/7))
    if visibility!='none':c.text(px+4,py+40,'Bullish / rising: light gray · Bearish / falling: dark gray','meta',width=int(pw/7))
    if replay:
        boundary=px+pw*(.60 if selecting else .84)
        line(c,boundary,py,boundary,py+ph,dash=True,stroke="#333")
        c.text(boundary-132,py+18,'Start candidate [time]' if selecting else 'Cursor [earlier time]' if state==55 else 'Old cursor G-012' if state==54 else 'Run cursor [time]','meta')
    if state==2:
        c.rect(px+14,py+12,min(380,pw-28),30,"#f5f5f5")
        c.text(px+24,py+32,'Loading requested basis; retained basis shown','meta',width=int((pw-36)/7))
    if state==3:
        c.rect(px+14,py+12,min(360,pw-28),30,"#f5f5f5")
        c.text(px+24,py+32,'Coverage end · earlier history remains readable','meta',width=int((pw-36)/7))
    for i in range(4):
        c.text(px+16+i*(pw-70)/4,y+h-49-controller_h,'[time]','meta')
    range_bar(c,x,y+h-36,w)
    c.parts.append('</g>')


def range_bar(c,x,y,w):
    """Viewport presets and calendar action, following the E01 bottom strip."""
    c.parts.append('<g data-role="chart-range-controls" aria-label="Chart date and viewport range">')
    c.rect(x,y,w,36,'#fafafa')
    for i,label in enumerate(('1D','5D','1M','3M','6M','YTD','1Y','5Y','All')):
        bx=x+6+i*32
        c.parts.append(f'<g role="img" aria-label="View range {label}"><title>View range {label}</title>')
        c.text(bx+4,y+24,label,'meta')
        c.parts.append('</g>')
    bx=x+304
    line(c,bx-6,y+7,bx-6,y+29,stroke='#ccc')
    c.parts.append('<g role="img" aria-label="Go to date or custom range"><title>Go to date or custom range</title>')
    c.rect(bx,y+4,30,28,'#fff')
    c.parts.append(f'<path transform="translate({bx+5},{y+7})" d="M2 4 H19 V21 H2 Z M2 9 H19 M6 1 V6 M15 1 V6 M12 13 H17 M15 11 L18 14 L15 17" fill="none" stroke="#333"/>')
    c.parts.append('</g>')
    if w>700:c.text(x+w-156,y+24,'[display time] [TZ]','meta')
    c.parts.append('</g>')


def go_to_window(c,x,y,w,h,custom=False):
    """A29 date tab; custom-range fields are an explicit design realization."""
    c.parts.append('<g data-role="go-to-window">')
    c.rect(x+4,y+4,w,h,'#ccc')
    c.rect(x,y,w,h,'#fff',weight=2)
    c.text(x+20,y+34,'Go to','title')
    c.text(x+w-30,y+32,'×','title')
    c.text(x+20,y+77,'Date','heading')
    c.text(x+100,y+77,'Custom range','heading')
    line(c,x+20,y+90,x+w-20,y+90,stroke='#ddd')
    line(c,x+(100 if custom else 20),y+90,x+(220 if custom else 56),y+90,stroke='#222')
    if custom:
        field(c,x+20,y+104,w-40,'From','[start date]    [time]')
        field(c,x+20,y+170,w-40,'To','[end date]      [time]')
        cal_y=y+256
    else:
        field(c,x+20,y+100,w-136,'Date','[YYYY-MM-DD]')
        field(c,x+w-104,y+100,84,'Time','[hh:mm]')
        cal_y=y+190
    c.text(x+30,cal_y,'‹','heading')
    c.text(x+w/2-54,cal_y,'October 2026','heading')
    c.text(x+w-38,cal_y,'›','heading')
    cell=(w-40)/7
    for i,day in enumerate(('Mo','Tu','We','Th','Fr','Sa','Su')):
        c.text(x+20+i*cell+8,cal_y+34,day,'meta')
    for row,week in enumerate(calendar.monthcalendar(2026,10)):
        for col,day in enumerate(week):
            if not day:continue
            dx=x+20+col*cell
            dy=cal_y+52+row*34
            if day==20:c.rect(dx+2,dy-3,cell-6,30,'#ddd')
            c.text(dx+9,dy+18,str(day),'meta')
    line(c,x,y+h-64,x+w,y+h-64,stroke='#ddd')
    control(c,x+w-190,y+h-46,80,'Cancel')
    control(c,x+w-100,y+h-46,80,'Go to')
    c.parts.append('</g>')


def quote_inspector(c,x,y,w,h,visibility,basis):
    c.parts.append('<g data-role="quote-series-inspector">');c.rect(x,y,w,h)
    rows=['Quote inspection · Chart 1', 'Visible: '+visibility, 'Calculation basis: '+basis,
          'Bid — filled / left slot', 'Bid O [open] H [high]', 'Bid L [low] C [close] V [volume]',
          'Ask — hollow / right slot', 'Ask O [open] H [high]', 'Ask L [low] C [close] V [volume]',
          'Volume bars: Bid filled / Ask hollow' if visibility=='both' else 'Volume · provider-qualified · '+basis,
          'Study SMA [value or warm-up] · '+basis,
          'Bullish light / bearish dark', 'Same selected UTC bucket / run boundary',
          'Provider volume units unverified']
    for i,row in enumerate(rows):c.text(x+12,y+26+i*44,row,'meta',width=int((w-24)/7))
    control(c,x+12,y+h-54,w-24,'Settings > Symbol > basis')
    c.parts.append('</g>')


def watchlist(c,x,y,w,h):
    c.rect(x,y,w,h)
    c.text(x+12,y+25,'Watchlist','heading')
    c.text(x+w-48,y+25,'+   ×','heading')
    line(c,x,y+42,x+w,y+42)
    c.text(x+12,y+66,'Symbol          Last       Time','meta')
    for i,symbol in enumerate(('EURUSD','GBPUSD','USDJPY','XAUUSD','SP500','DAX')):
        ry=y+80+i*34
        if i==0:c.rect(x+4,ry,w-8,32,'#eee')
        c.text(x+12,ry+21,symbol,'meta')
        c.text(x+110,ry+21,'[value]   [time]','meta')
    dy=y+310
    line(c,x,dy,x+w,dy)
    c.text(x+12,dy+30,'EURUSD · Dukascopy','heading')
    c.text(x+12,dy+60,'Bid / M1 · [observation time]','meta')
    c.text(x+12,dy+96,'[selected value]','title')
    c.text(x+12,dy+126,'Open  [value]    High  [value]','meta')
    c.text(x+12,dy+151,'Low   [value]    Close [value]','meta')
    c.text(x+12,dy+188,'Coverage [discovered bounds]','meta')
    c.text(x+12,dy+212,'Feed [qualified condition]','meta')
    c.text(x+12,dy+242,'Details / numeric inspector >','meta')


def state_note(c,x,y,w,state,variant="state",h=72):
    message,next_action,_=STATES[state]
    if variant in ('restore','delete','restart'):
        message='Review '+variant+': exact target and expected version'
        next_action='Confirm '+variant+' or cancel'
    elif variant=='image':
        message='Chart image · pinned source [version / cursor]'
        next_action='Generate local chart image'
    elif variant=='resolution-unknown':
        message='Resolution outcome unknown; original event retained'
        next_action='Reconcile original publication'
    c.rect(x,y,w,h,'#f4f4f4')
    c.text(x+10,y+20,message,'meta',width=max(24,int((w-20)/7)))
    # Primary reason is always visible; longer recovery explanation lives in
    # its named details drawer, never beneath an overlapping command.
    return next_action



def entry_context(variant):
    """Revision 29's single draft; fixtures express no numerical policy."""
    direction = 'Sell' if variant.startswith('entry-sell') else 'Buy'
    status = 'pending' if 'pending' in variant else 'invalid' if 'invalid' in variant else 'ready'
    risk = variant in ('risk', 'risk-invalid') or 'risk' in variant
    return direction, status, risk


def entry_form(c, x, y, w, h, variant):
    direction, status, risk = entry_context(variant)
    c.parts.append('<g data-role="entry-direction-editor">')
    c.rect(x,y,w,h)
    c.text(x+12,y+25,'Entry draft · R-014 · EURUSD','heading')
    c.text(x+12,y+49,'Select direction (does not submit)','meta')
    for i,side in enumerate(('Buy','Sell')):
        control(c,x+12+i*(w-24)/2,y+60,(w-28)/2,'Select '+side,selected=direction==side)
        if direction==side:
            c.text(x+(i+1)*(w-24)/2-12,y+80,'✓','meta')
    kind='Market' if variant in ('paper-replay','state') else 'Stop' if variant=='stop' else 'Limit'
    rows=[
        'Direction: '+direction+' · Type: '+kind,
        'Completed decision [time] · basis D-006',
        'Sizing: Risk % · [risk input]' if risk else 'Sizing: Fixed units · [quantity input]',
        'Entry level — market · SL / TP [inputs]' if kind=='Market' else 'Entry level [price input] · SL / TP [inputs]',
        'Sell executes bid' if direction=='Sell' else 'Buy executes ask',
        'Specs / fees / FX [selected historical basis]',
        'VALID: permitted quantity / risk / fees [estimate]' if status=='ready' else
        'PENDING: prior validation / estimates superseded' if status=='pending' else
        'ERROR: retained levels invalid for Sell' if direction=='Sell' else 'ERROR: required SL missing; estimate unavailable',
        'Review '+direction+'; matching replay action submits' if status=='ready' else 'Both submissions blocked; correct / validate',
        'After boundary; acceptance / fill / save separate',
    ]
    spacing=26 if h<500 else 44
    for i,row in enumerate(rows):
        c.text(x+12,y+116+i*spacing,row,'meta',width=int((w-24)/6.7))
    if h>=500:
        c.text(x+12,y+h-140,'Edits retain inputs; validate current context','meta',width=int((w-24)/6.7))
        c.text(x+12,y+h-120,'No guaranteed loss; gaps may exceed planned risk','meta',width=int((w-24)/6.7))
        control(c,x+12,y+h-84,w-24,'Simulation settings')
    control(c,x+12,y+h-44,w-24,'Cancel entry draft')
    c.parts.append('</g>')


def replay_controller(c,x,y,w,h,state,variant,paper=False,narrow=False):
    """A31/A32: one compact floating capsule, not a reserved chart dock."""
    selecting=variant=='replay-select'
    playing=variant=='replay-active'
    unresolved=variant=='resolution-unknown'
    entry=paper and state==25 and variant not in ('pending','close-partial','close-full')
    direction,status,risk=entry_context(variant)
    ready=entry and status=='ready' and not playing
    bw=min(850,w-24)
    bx=x+(w-bw)/2
    by=y
    # Small-screen reflow preserves a floating surface; transport and trading
    # wrap within it instead of becoming a full-width chart dock.
    two_rows=bw<740
    bh=76 if two_rows else 40
    c.parts.append('<g data-role="floating-replay-bar">')
    c.parts.append(f'<rect x="{bx+3}" y="{by+4}" width="{bw}" height="{bh}" rx="6" fill="#ccc"/>')
    c.parts.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="#f5f5f5" stroke="#888"/>')

    def cell(cx,cy,cw,label,enabled=True,fill=None,glyph=None):
        c.parts.append(f'<g data-control="{esc(label)}" aria-disabled="{str(not enabled).lower()}"><title>{esc(label)}</title>')
        if fill:
            c.parts.append(f'<rect x="{cx}" y="{cy+4}" width="{cw}" height="28" rx="4" fill="{fill}" stroke="#bbb"/>')
        if glyph=='play':
            c.parts.append(f'<path d="M{cx+9} {cy+11} L{cx+9} {cy+25} L{cx+20} {cy+18} Z" fill="#444"/>')
        elif glyph=='step':
            c.parts.append(f'<path d="M{cx+8} {cy+11} L{cx+8} {cy+25} L{cx+18} {cy+18} Z M{cx+21} {cy+11} V{cy+25}" fill="#444" stroke="#444"/>')
        elif glyph=='pause':
            c.parts.append(f'<path d="M{cx+10} {cy+11} V{cy+25} M{cx+18} {cy+11} V{cy+25}" stroke="#444" stroke-width="3"/>')
        elif glyph=='pin':
            c.parts.append(f'<path d="M{cx+8} {cy+10} H{cx+18} M{cx+11} {cy+10} V{cy+18} L{cx+7} {cy+22} H{cx+19} L{cx+15} {cy+18} V{cy+10} M{cx+13} {cy+22} V{cy+28}" fill="none" stroke="#444"/>')
        else:c.text(cx+5,cy+23,label,'meta',width=max(10,int((cw-8)/6.5)))
        if not enabled:c.parts.append(f'<path d="M{cx+4} {cy+31} H{cx+cw-4}" stroke="#999" stroke-dasharray="2 2"/>')
        c.parts.append('</g>')

    cx=bx+8;cy=by+2
    for yy in (12,18,24):
        for xx in (4,8):c.parts.append(f'<circle cx="{cx+xx}" cy="{cy+yy}" r="1" fill="#888"/>')
    cx+=16
    cell(cx,cy,78,'Select bar' if selecting else 'Start bar',not unresolved and state not in (5,26,27,30,31,32,33,34,35,36,38,39,40,52,54) and not playing);cx+=80
    cell(cx,cy,28,'Pause' if playing else 'Play',not unresolved and not selecting and command_enabled(state,'Play / pause'),glyph='pause' if playing else 'play');cx+=28
    cell(cx,cy,28,'Step',not unresolved and not selecting and not playing and command_enabled(state,'Step bar'),glyph='step');cx+=32
    cell(cx,cy,48,'Speed v');cx+=50
    line(c,cx,by+8,cx,by+32,stroke='#ccc');cx+=10
    cell(cx,cy,106,'[candidate time]' if selecting else '[earlier time]' if state==55 else '[unknown time]' if state==54 else '[replay time]');cx+=108
    cell(cx,cy,86,'[bars left]');cx+=90
    if two_rows:cx=bx+12;cy=by+38
    else:line(c,cx,by+8,cx,by+32,stroke='#ccc');cx+=8
    if selecting:
        cell(cx,cy,100,'Start replay',True,fill='#ddd');cx+=104
        cell(cx,cy,28,'×')
    else:
        cell(cx,cy,44,'Sell',ready and direction=='Sell',fill='#e5e5e5');cx+=46
        cell(cx,cy,66,'[quantity]',ready);cx+=68
        cell(cx,cy,54,'Units v');cx+=58
        cell(cx,cy,44,'Buy',ready and direction=='Buy',fill='#d3d3d3');cx+=48
        cell(cx,cy,68,'P/L [USD]' if paper else 'P/L [—]');cx+=70
        cell(cx,cy,26,'Pin',glyph='pin');cx+=28
        cell(cx,cy,26,'×')
    if entry:
        sy=by-160
        c.rect(bx,sy,bw,154,'#fff')
        c.text(bx+10,sy+18,'R-014 · EURUSD · completed decision [time] · '+direction+' draft','meta',width=int((bw-20)/6.7))
        c.text(bx+10,sy+38,'Type: '+('Market' if variant in ('paper-replay','state') else 'Stop' if variant=='stop' else 'Limit')+' · level [price] · SL / TP [inputs]','meta',width=int((bw-20)/6.7))
        reason=('Sell unavailable: draft is Buy' if direction=='Buy' else 'Buy unavailable: draft is Sell') if ready else 'Both unavailable: validation '+status+'; old estimates superseded'
        c.text(bx+10,sy+58,'Sizing: '+('Risk % [input]' if risk else 'Fixed units [input]')+' · specs / fees / FX [basis]','meta',width=int((bw-20)/6.7))
        c.text(bx+10,sy+78,reason,'meta',width=int((bw-20)/6.7))
        c.text(bx+10,sy+98,('VALID: '+direction+' / '+('ask' if direction=='Buy' else 'bid')+' · quantity / risk / fees [estimate]') if ready else 'Proposed levels need current side-specific validation','meta',width=int((bw-20)/6.7))
        control(c,bx+10,sy+122,bw-20,'Edit entry / direction')
    c.parts.append('</g>')


def trading_branch(c,x,y,w,h,state,variant):
    if state==25 and variant not in ('pending','close-partial','close-full'):
        entry_form(c,x,y,w,h,variant)
        return
    c.parts.append('<g data-role="targeted-trading-form">')
    c.rect(x,y,w,h)
    title='Order draft · R-014'
    rows=[]; actions=[]
    if state==26:
        title='Historical trading · no run'
        rows=['No active historical run','No orders, positions or recorded results','Choose a start or a retained run','Analysis remains available']
        actions=['Choose start / resume']
    elif state==27:
        title='Submitting entry · R-014'
        rows=['Pending request I-009 · original occurrence',
              'Completed decision [time] · basis D-006',
              'Submitted terms [side / type / units]',
              'Submitted level / SL / TP [prices]',
              'Prior valid orders / positions retained',
              'No new entry or replay advance while pending',
              'Await original intent; do not submit again',
              'Acceptance / fill not confirmed; save separate']
        actions=['Inspect submitted terms','Return to chart']
    elif state in (30,31,32):
        title={30:'Run R-014 · Blocked',31:'Run R-014 · Outcome unknown',32:'Run R-014 · Read-only'}[state]
        rows=['Original basis D-006 · known prefix [time]',
              {30:'Event EV-027 / original time [time]',31:'Intent I-009 / original occurrence [time]',32:'Writer authority denied for this run'}[state],
              {30:'Missing historical USD conversion',31:'Effect / publication requires reconciliation',32:'Retained evidence remains inspectable'}[state],
              'No new entry, close, modification or replay advance']
        actions=[{30:'Open original event',31:'Reconcile same intent',32:'Inspect writer authority'}[state],'Return to chart']
    elif variant=='pending':
        title='Modify Order O-008 / v2'
        rows=['Run R-014 · completed decision [time]', 'Accepted waiting; not filled · Buy Limit',
              'Valid old terms retained until accepted edit', 'Quantity draft [units] / prior [units]',
              'Entry level draft [price] / prior [price]', 'SL / TP draft [prices] / prior [prices]',
              'Estimate [quantity / fees / planned risk]', 'Applies after this decision; no new entry']
        actions=['Apply modification','Cancel selected order','Discard edit']
    elif variant in ('close-partial','close-full') or state==29:
        title='Close Position P-004 / v3'
        amount='12,000 units' if state==29 else '4,000 units' if variant=='close-partial' else '10,000 units'
        rows=['Run R-014 · completed decision [time]', 'Independent long position · remaining 10,000 units',
              'Current SL / TP [recorded protection]', 'Close amount: '+amount,
              'ERROR: 12,000 exceeds 10,000 remainder' if state==29 else 'Review partial close · remainder 6,000 units' if variant=='close-partial' else 'Review full close · remainder 0 units',
              'Remainder keeps valid SL / TP' if variant=='close-partial' else 'Full close ends associated protection' if state!=29 else 'Valid position and protection unchanged',
              'Close sells at eligible bid · fees [USD]', 'Request is not a fill; recorded outcome follows']
        actions=['Request targeted close','Cancel close draft']
    else:
        kind='Stop' if variant=='stop' else 'Limit'
        risk=variant in ('risk','risk-invalid')
        rows=['Run R-014 · completed decision [time]', 'Direction: Buy · Type: '+kind,
              'Entry level [price input] · required', 'Sizing: Risk %' if risk else 'Sizing: Fixed units',
              'Risk percent [input] / SL [price required]' if risk else 'Quantity [units input]',
              'ERROR: required SL missing; estimate unavailable' if variant=='risk-invalid' else 'Quantity / planned risk / fees [estimate]',
              'Rounded permitted quantity / minimum [validation]', 'SL / TP [optional prices]' if not risk else 'Includes configured entry and exit fees',
              'No guaranteed loss; gaps may exceed planned risk', 'Valid draft: use replay-bar Buy to submit' if variant!='risk-invalid' else 'Replay-bar Buy disabled until valid']
        actions=['Simulation settings','Cancel entry draft']
    c.text(x+12,y+27,title,'heading',width=int((w-24)/9));line(c,x,y+40,x+w,y+40)
    for i,row in enumerate(rows):
        c.rect(x+10,y+51+i*45,w-20,42,'#fafafa')
        c.text(x+18,y+68+i*45,row,'meta',width=int((w-36)/7))
    for i,action in enumerate(actions):
        control(c,x+12,y+h-46*(len(actions)-i)-8,w-24,action,not (state==29 and action=='Request targeted close'))
    c.parts.append('</g>')


def paper_order_drawer(c,x,y,w,h,state,variant):
    """Trace A32's hierarchy and grouping; draft-only fields stay in the panel."""
    c.parts.append('<g data-role="paper-replay-order-drawer">')
    c.rect(x,y,w,h)
    c.text(x+14,y+24,'Order O-008' if variant=='paper-accepted' else 'Order panel','heading')
    c.text(x+w-24,y+24,'×','heading')
    line(c,x,y+40,x+w,y+40,stroke='#ddd')
    c.parts.append(f'<defs><clipPath id="paper-ticket-body"><rect x="{x+4}" y="{y+44}" width="{w-8}" height="{h-152}"/></clipPath></defs><g clip-path="url(#paper-ticket-body)">')
    c.rect(x+14,y+60,16,16,'#eee')
    c.text(x+40,y+74,'Paper Trading v','heading')
    c.text(x+w-28,y+74,'…','heading')
    c.text(x+14,y+100,'Paper · Simulated, not real money','meta')
    half=(w-42)/2
    for dx,label,value,dy in ((0,'Balance','[USD]',126),(half+14,'Equity','[USD]',126),(0,'Open P/L','[USD]',166),(half+14,'Today (UTC)','[USD]',166)):
        c.text(x+14+dx,y+dy-12,label,'meta')
        c.text(x+14+dx,y+dy+4,value,'',width=20)
    line(c,x,y+192,x+w,y+192,stroke='#ddd')
    c.text(x+14,y+218,'EURUSD','heading')
    c.text(x+w-108,y+218,'[replay price]','meta')
    c.text(x+14,y+254,'Preset','meta')
    control(c,x+w-86,y+232,72,'None v',False)
    # The large Sell/Buy pair selects the ticket direction; the floating bar
    # commits the matching historical intent, as A32 explicitly instructs.
    for dx,label,selected in ((0,'Sell',False),(half+14,'Buy',True)):
        accepted=variant=='paper-accepted'
        processing=variant=='paper-processing'
        action=('Modify order' if label=='Sell' else 'Cancel order') if accepted else label+' direction'
        caption=action if accepted else 'Select '+label if variant=='paper-replay' else label
        disabled=' aria-disabled="true"' if processing else ' aria-pressed="'+str(selected).lower()+'"' if variant=='paper-replay' else ''
        c.parts.append(f'<g data-control="{action}"{disabled}><rect x="{x+14+dx}" y="{y+276}" width="{half}" height="44" rx="6" fill="{"#d3d3d3" if selected and not accepted else "#eee"}" stroke="#aaa"/>')
        c.text(x+14+dx+half/2-(len(caption)*3.5 if accepted else len(caption)*3.5 if variant=='paper-replay' else 12),y+303,caption,'')
        c.parts.append('</g>')

    def segments(yy,items):
        sw=(w-28)/len(items)
        c.rect(x+14,y+yy,w-28,28,'#f4f4f4')
        for i,(label,enabled,selected) in enumerate(items):
            enabled=enabled and variant not in ('paper-accepted','paper-processing')
            c.parts.append(f'<g data-control="{esc(label)}" aria-disabled="{str(not enabled).lower()}">')
            if selected:c.rect(x+14+i*sw,y+yy,sw,28,'#fff')
            c.text(x+20+i*sw,y+yy+19,label,'meta',width=14)
            c.parts.append('</g>')
    segments(334,[('Market',True,True),('Limit',True,False),('Stop',True,False)])
    c.text(x+14,y+388,'Quantity','meta')
    c.text(x+w-46,y+388,'Units','meta')
    segments(396,[('USD',False,False),('Units',True,True),('% equity',False,False),('Risk',True,False)])
    c.parts.append(f'<rect x="{x+14}" y="{y+430}" width="{w-28}" height="36" rx="6" fill="#f8f8f8" stroke="#aaa"/>')
    c.text(x+26,y+454,'[quantity]','')
    chip=(w-46)/4
    for i,label in enumerate(('$1K','$5K','$10K','$25K')):control(c,x+14+i*(chip+6),y+472,chip,label,False,h=24)
    c.text(x+14,y+516,'Order value [USD] · [risk %] · [units]','meta',width=int((w-28)/7))
    segments(530,[('Price',True,True),('%',False,False),('Ticks',False,False),('ATR',False,False)])
    control(c,x+14,y+564,72,'$ risk',False,h=24)
    for dx,label,hint in ((0,'Stop loss','Use 1%'),(half+14,'Take profit','Use 2%')):
        c.text(x+14+dx,y+616,label,'meta')
        c.parts.append(f'<rect x="{x+14+dx}" y="{y+626}" width="{half}" height="36" rx="6" fill="#f8f8f8" stroke="#aaa"/>')
        c.text(x+24+dx,y+649,'Optional','meta')
        control(c,x+14+dx+half-64,y+630,60,hint,False,h=24)
    c.parts.append(f'<rect x="{x+14}" y="{y+678}" width="{w-28}" height="42" rx="5" fill="#ddd" stroke="#aaa"/>')
    message={'paper-accepted':'Accepted · waiting; not filled',
             'paper-processing':'Evaluating event · new decisions unavailable'}.get(variant,'Valid Buy draft: replay Buy submits')
    c.text(x+26,y+704,message,'meta',width=int((w-48)/7))
    detail={'paper-accepted':'Next eligible event · use Modify order',
            'paper-processing':'O-008 · no fill confirmed'}.get(variant,'Select direction only; edits invalidate')
    c.text(x+14 if variant in ('paper-accepted','paper-processing') else x+w/2-74,y+743,detail,'meta')
    c.parts.append('</g>')
    # At the baseline height the ticket scrolls internally, as a normal sidebar.
    if h<850:
        line(c,x+w-7,y+58,x+w-7,y+h-120,stroke='#ccc')
        c.rect(x+w-10,y+80,6,100,'#999')
    fy=y+h-96
    line(c,x,fy-12,x+w,fy-12,stroke='#ddd')
    for label,yy in (('Ask before placing',fy+12),('Kill switch',fy+40)):
        c.text(x+14,yy,label,'meta')
        c.parts.append(f'<g data-control="{label}" aria-disabled="true"><rect x="{x+w-42}" y="{yy-13}" width="26" height="14" rx="7" fill="#eee" stroke="#aaa"/><circle cx="{x+w-35}" cy="{yy-6}" r="5" fill="#aaa"/></g>')
    c.text(x+14,fy+68,'Run [id] · USD · Buy ask / Sell bid','meta',width=int((w-28)/7))
    c.parts.append('</g>')


def drawer(c,x,y,w,h,title,state,variant="state",kind="data"):
    if kind=='trade' and (state==25 and variant!='paper-replay' or variant in ('limit','stop','risk','risk-invalid','pending','close-partial','close-full') or state in (26,29,30,31,32) or state==27 and variant!='paper-processing'):
        trading_branch(c,x,y,w,h,state,variant)
        return
    if kind=='trade' and (state not in (26,28,29) and variant!='pending' or variant=='paper-accepted'):
        paper_order_drawer(c,x,y,w,h,state,variant)
        return
    c.parts.append('<g data-role="context-drawer">')
    c.rect(x,y,w,h)
    c.text(x+12,y+27,title,'heading',width=int((w-48)/9))
    c.text(x+w-24,y+26,'×','heading')
    line(c,x,y+42,x+w,y+42)
    cy=y+58
    # Rows below are actual scoped controls/details, rather than separate pages.
    if kind=='trade':
        c.text(x+12,cy+14,'Run [id] · Paused · USD','meta');cy+=26
        c.text(x+12,cy+14,'Cursor [time] · completed decision','meta');cy+=30
        if variant=='pending' or state==28:
            fields=[('Order','[identity / version]'),('Instruction state','Accepted waiting · not filled'),('Type / direction','[type] / [Buy or Sell]'),('Quantity','[units]'),('Level / SL / TP','[requested levels]')]
            actions=['Modify order','Cancel selected order']
        elif state==29:
            fields=[('Position','[identity / current version]'),('Remaining','[quantity / units]'),('Close amount','[requested units]'),('Closing side / fee','[Bid or Ask] / [USD]')]
            actions=['Request targeted close','Review remainder']
        elif state==26:
            fields=[('Historical run','No active run'),('Orders / positions','No active collection')]
            actions=['Choose start / resume']
        else:
            fields=[('Order type','Market / Limit / Stop'),('Direction','Buy / Sell'),('Quantity','[quantity] units'),('Order price','[price if required]'),('Stop loss / Take profit','[optional prices]')]
            actions=['Reconcile same intent','Inspect target'] if state==31 else ['Submit entry','Simulation settings']
        for label,value in fields:
            field(c,x+12,cy,w-24,label,value);cy+=62
        if state!=26:
            c.text(x+12,cy+13,'Planned risk [USD] · Fees [USD]','meta');cy+=24
            c.text(x+12,cy+13,'After decision · accepted ≠ filled','meta');cy+=24
            c.text(x+12,cy+13,'Buy uses ask · Sell uses bid','meta')
    elif kind=='objects':
        c.text(x+12,cy+14,'Objects · EURUSD / layout [name]','meta');cy+=38
        for name in ('Trendline [selected]','Horizontal line [locked]','Brush [preview]'):
            control(c,x+12,cy,w-24,name,selected='selected' in name);cy+=42
        for label,value in [('Point','[selected index]'),('Time anchor','[time input]'),('Price anchor','[price input]')]:
            field(c,x+12,cy,w-24,label,value);cy+=62
        c.text(x+12,cy+14,'Add point / Remove point','meta')
        actions=['Commit valid drawing','Cancel preview']
    elif kind=='event':
        rows=['Run [identity] / retained basis','Original event [identity / time]','Last coherent prefix [time]','Needed: historical USD conversion','Applicable evidence [identity]','Compatibility [required outcome]']
        if state==37 and variant!='resolution-unknown':rows[3]='Former missing FX: resolved'
        if variant=='resolution-unknown':
            rows[3]='Publication outcome unknown'
            rows.append('Start / Play / Step blocked until reconciled')
        for row in rows:
            cy=c.text(x+12,cy+16,row,'meta',width=int((w-24)/7))+(10 if variant=='resolution-unknown' else 18)
        control(c,x+12,cy+10,w-24,'Evidence and provenance >');cy+=70
        c.text(x+12,cy+14,'Original occurrence only','meta');cy+=26
        c.text(x+12,cy+14,'No automatic playback','meta')
        actions=['Resolve when compatible','Return paused'] if state not in (37,38,40) else [STATES[state][1],'Return paused']
        if variant=='resolution-unknown':actions=['Reconcile publication','Return paused']
    else:
        rows=['Dukascopy · data only','Series [instrument / side / period]','Requested span [start / end]','Qualified subset [intervals]','Unresolved spans [reason]','Receipt time [local time]','Event time [observation time]','Catalog [published version]','Saved runs retain original inputs']
        if state==48:rows=['Replay run [identity / cursor]','Operational connection status only','Requested historical span [bounds]','Later times / prices withheld','No later OHLC or derived metrics','Retained run basis unchanged']
        if state==46:rows[0]='Live access unverified / denied'
        for row in rows:cy=c.text(x+12,cy+14,row,'meta',width=int((w-24)/7))+18
        control(c,x+12,cy+8,w-24,'Coverage / lineage details >')
        actions=['Qualified reconnect','Safe diagnostics']
    note_y=y+h-174
    assert cy < note_y+20, (title,'drawer content overflow',cy,note_y)
    state_note(c,x+10,note_y,w-20,state,variant,h=88)
    for i,action in enumerate(actions[:2]):
        control(c,x+12,note_y+100+i*36,w-24,action,command_enabled(state,action))
    c.parts.append('</g>')


def bottom_dock(c,x,y,w,h,state,variant):
    c.parts.append('<g data-role="bottom-dock">')
    c.rect(x,y,w,h)
    c.text(x+12,y+24,'Positions   |   Orders   |   Results / executions','meta')
    c.text(x+w-58,y+24,'—   ×','meta')
    line(c,x,y+38,x+w,y+38)
    c.text(x+12,y+62,'No run selected' if state==26 else 'Run R-014 · cursor [time] · original basis D-006 · USD','meta')
    if state==26:
        c.text(x+12,y+102,'No active run · start or resume from retained work','meta')
    else:
        columns=[('Target',.02),('Side',.23),('Quantity',.36),('State / protection',.51),('Fees / result USD',.76)]
        for label,p in columns:c.text(x+w*p,y+91,label,'meta')
        line(c,x+10,y+100,x+w-10,y+100)
        for label,p in ([('P-004 / v3',.02),('Long',.23),('10,000 units',.36),('Open; protection retained',.51),('[recorded USD]',.76)] if state==29 else [('[identity]',.02),('[Buy / Sell]',.23),('[units]',.36),('[recorded state]',.51),('[USD / reason]',.76)]):
            c.text(x+w*p,y+124,label,'meta')
        c.text(x+12,y+h-17,'Selected target details >    ASM-01 stop-first / ASM-02 full-fill and bar-touch · provenance >','meta',width=int((w-24)/7))
    c.parts.append('</g>')


def window(c,x,y,w,h,view,state,variant,docked=False):
    c.parts.append('<g data-role="context-drawer">' if docked else '<g data-role="settings-window">')
    titles={2:'Settings',1:'Select symbol'}
    title=titles.get(view,'Settings')
    if variant=='analysis':title='Chart settings'
    if not docked:c.rect(x+5,y+5,w,h,'#ccc')
    c.rect(x,y,w,h,'#fff',weight=2)
    c.text(x+20,y+33,title,'title')
    c.text(x+w-32,y+32,'×','title')
    line(c,x,y+52,x+w,y+52)
    body_bottom=y+h-110
    c.parts.append(f'<defs><clipPath id="window-content"><rect x="{x+8}" y="{y+58}" width="{w-20}" height="{h-174}"/></clipPath></defs><g clip-path="url(#window-content)">')
    cy=y+74
    if view==2:
        navw=156 if w>600 else 116
        items=['Symbol','Status line','Scales and lines','Canvas','Studies','Data location'] if variant=='analysis' else ['Simulation','Sizing','Commission','Instrument spec','Data location']
        for i,item in enumerate(items):
            control(c,x+16,cy+i*42,navw-24,item,selected=(item=='Data location' if variant.startswith('data-') else i==0))
        fx=x+navw+18;fw=w-navw-42
        if variant.startswith('data-'):
            rows=[('Current folder','[new committed root]' if variant=='data-applied' else '[retained local data root]'),('Dukascopy data folder','[absolute directory path input]'),('Validation',{'data-invalid':'Not readable / missing expected data','data-checking':'Checking selected folder; not applied','data-applied':'Folder applied; retained runs unchanged'}.get(variant,'Readable; supported data found')),('Coverage','Not established until valid check' if variant in ('data-invalid','data-checking') else '[detected assets / periods / limitations]')]
        elif variant=='analysis':
            rows=[('Chart type','Candles / Line'),('Candle appearance','Body / border / wick'),('Precision','[display precision]'),('Timezone','[selected timezone]'),('Calculation basis','Bid / Ask · active chart / studies / volume'),('Theme','Light / Dark'),('Study instance','[selected study]')]
        else:
            rows=[('Scope','[instrument / settings version]'),('Currency / initial balance','USD / [balance]'),('Sizing method','Fixed / Risk %'),('Quantity / planned risk','[units] / [USD estimate]'),('Commission','[basis / rate]'),('Instrument specification','[metadata / explicit override]')]
        for label,value in rows:
            field(c,fx,cy,fw,label,value,command_enabled(state,'Apply'));cy+=62
        if variant.startswith('data-'):
            control(c,fx,cy,fw,'Browse folder / paste path');cy+=40
            control(c,fx,cy,fw,'Check folder',variant!='data-checking')
        # Scroll reveals further supported parameters, never a new page.
    else:
        fx=x+24;fw=w-48
        field(c,fx,cy,fw,'Search','[manual ticker / provider alias / name]');cy+=74
        c.text(fx,cy+18,'Symbol       Provider       Instrument','meta');cy+=36
        for i,label in enumerate(('EURUSD · Dukascopy','GBPUSD · Dukascopy','USDJPY · Dukascopy')):
            control(c,fx,cy+i*48,fw,label,selected=i==0)
        cy+=156
        c.text(fx,cy+16,'Requested selection [pending] · adopted basis unchanged','meta',width=int(fw/7))
    c.parts.append('</g>')
    if view in (2,3):
        line(c,x+w-12,y+66,x+w-12,body_bottom-8,stroke='#ccc')
        c.rect(x+w-15,y+80,6,90,'#888')
    if variant.startswith('data-'):
        c.text(x+16,body_bottom+16,'Folder applied to working settings; save status below; files unchanged' if variant=='data-applied' else 'Previous folder remains until valid Apply; source files unchanged','meta',width=int((w-32)/7))
    else:state_note(c,x+16,body_bottom,w-32,state,variant,h=48)
    # Consequence/reason is above persistent commit and cancel controls.
    if variant.startswith('data-'):actions=['Close'] if variant=='data-applied' else ['Cancel','Apply folder']
    elif view==2:actions=['Close','Save recovery'] if state==15 else ['Cancel','Apply']
    else:actions=['Cancel','Adopt selection']
    for i,action in enumerate(actions):
        control(c,x+w-252+i*120,y+h-62,108,action,command_enabled(state,action) and not (action=='Apply folder' and variant in ('data-invalid','data-checking')))
    c.parts.append('</g>')


def work_drawer(c,x,y,w,h,state):
    c.parts.append('<g data-role="saved-work-drawer">')
    c.rect(x,y,w,h)
    c.text(x+12,y+26,'Saved work / recovery','heading')
    c.text(x+w-24,y+26,'×','heading')
    line(c,x,y+42,x+w,y+42)
    cy=y+58
    c.text(x+12,cy+16,'Layouts  |  Saved runs  |  Own backup','meta');cy+=32
    for name in ('Layout [selected name]','Run [identity / cursor]'):
        control(c,x+12,cy,w-24,name,selected='Layout' in name);cy+=40
    for text in ('Working [version] / Saved [version]','Writer [authority / reason]','Original inputs [validation result]'):
        c.text(x+12,cy+16,text,'meta',width=int((w-24)/7));cy+=26
    if h>500:
        field(c,x+12,cy,w-24,'Charts / interval sync','One / Two · sync on / off');cy+=66
        control(c,x+12,cy,w-24,'Own backup / validation details >')
    ny=y+h-150
    state_note(c,x+12,ny,w-24,state,h=68)
    control(c,x+12,ny+80,w-24,'Create layout' if state==18 else 'Restore layout',command_enabled(state,'Restore layout'))
    control(c,x+12,ny+116,w-24,'Close saved work')
    c.parts.append('</g>')


def review_dock(c,x,y,w,h,state,variant):
    c.parts.append('<g data-role="inline-confirmation-dock">')
    c.rect(x,y,w,h,'#fafafa')
    title={'restore':'Saved work > Restore backup','delete':'Saved work > Delete layout','restart':'Replay > Restart with updated data'}.get(variant,'Replay > Move back')
    rows={
        'restore':['Backup B-003 / snapshot v7 · validation: complete input closure',
                   'Replace: local work generation G-012 with backup generation B-003',
                   'Included: Layout L-002 + drawings; Run R-014 + original inputs',
                   'No merge; included newer local work is replaced; credentials excluded'],
        'delete':['Layout L-002 / expected v12 · Morning review',
                  'Delete this layout and its owned drawings / chart arrangement',
                  'Retained runs and unrelated layouts remain outside deletion scope',
                  'No automatic archive; cancel preserves this layout'],
        'restart':['Run R-014 / expected v12 · old input basis D-006',
                   'Selected new input basis D-009 · required input closure: complete',
                   'Restart at original start [time]; discard later trading actions/results',
                   'Drawings unchanged; old generation authoritative until publication'],
    }.get(variant,['Run R-014 / expected v12 · current cursor [old cursor]',
                   'Destination [earlier time] · retained original basis D-006',
                   'Discard later trading actions/results; drawings unchanged',
                   'Cancel preserves current run; no automatic discarded-state archive'])
    if state==55:
        title='Replay > Replacement published'
        rows=['Surviving Run R-014 / new generation G-013 / authority epoch E-013',
              'Actual cursor [earlier time] · Paused · retained input basis D-006',
              'Later trading suffix discarded; positions/results rebuilt to actual cursor',
              'Drawings unchanged; publication complete; cancellation no longer applies']
    elif state==54:
        rows=['Run R-014 · old G-012 / proposed G-013 · active generation unknown',
              'Current cursor / positions unavailable until reconciliation',
              'No rollback or publication success inferred; no repeated replacement',
              'Reconcile original publication to establish the surviving generation']
    elif state==53:
        rows=['Run R-014 / G-012 remains authoritative · original cursor [old cursor]',
              'Preparation cancelled / known not published; original work unchanged',
              'No replacement activated; return to original run']
    elif state in (50,51,52,56):
        rows[-1]={50:'Input validation failed: required original inputs absent; no confirmation',
                  51:'Target version changed; prior proposal invalid; review revised scope',
                  52:'Preparing replacement; old generation authoritative; not yet published',
                  56:'Writer authority denied; inspect authority; old work unchanged'}[state]
    c.text(x+12,y+25,title,'heading');line(c,x,y+38,x+w,y+38)
    for i,row in enumerate(rows):c.text(x+12,y+61+i*28,row,'meta',width=int((w-24)/7))
    confirm={'restore':'Confirm restore','delete':'Confirm delete','restart':'Confirm restart'}.get(variant,'Move back')
    if state==51:confirm='Review revised scope'
    if state==54:confirm='Reconcile outcome'
    if state in (53,55):confirm='Return to run'
    if state not in (53,54,55):control(c,x+w-292,y+h-43,108,'Cancel preparation' if state==52 else 'Cancel')
    control(c,x+w-172,y+h-43,160,confirm,state not in (50,52,56))
    c.parts.append('</g>')


def export_dock(c,x,y,w,h,state,variant):
    c.parts.append('<g data-role="results-export-dock">')
    c.rect(x,y,w,h,'#fafafa')
    image=variant=='image'
    c.text(x+12,y+25,'Chart > Export image' if image else 'Results > Export report','heading')
    c.text(x+w-26,y+25,'×','heading')
    line(c,x,y+38,x+w,y+38)
    c.text(x+12,y+62,'Source [chart / run identity] · snapshot [version / cursor]','meta',width=int((w-24)/7))
    c.text(x+12,y+92,'Include: chart, studies, drawings and legend' if image else 'Include: simulated trades, fees, USD results and evidence labels','meta',width=int((w-24)/7))
    c.text(x+12,y+122,'Artifact [actual outcome] · source stays pinned if the workspace advances','meta',width=int((w-24)/7))
    ny=y+h-96
    state_note(c,x+12,ny,w-24,state,variant,h=48)
    action='Export image' if image else 'Export report'
    if state==62:action='Verify output'
    if state==63:action='Return to results'
    if state==59:action='Writing output'
    control(c,x+w-292,y+h-43,108,'Cancel')
    control(c,x+w-172,y+h-43,160,action,command_enabled(state,'Generate') if action.startswith('Export') else state!=59)
    c.parts.append('</g>')


def render(frame, state_names):
    view,state,variant=frame['view'],frame['state'],frame['variant']
    replay=state!=26 and (view in (4,5) or (view==8 and variant!='image') or state in (5,30,48) or variant in ('replay','replay-select','replay-active','two-chart','pending','resolution-unknown','restart') or (view==7 and variant not in ('restore','delete')))
    if variant in ('go-to-date','custom-range'):
        frame['annotation']='Calendar button in the bottom-left range strip opens the floating Go to window above the retained chart, as explicitly restored by the user. Date changes the viewport, never the run cursor. Cancel keeps the prior viewport. Calendar month/day selection is illustrative.'+(' Custom-range contents are a designed From/To realization of the visible A29 tab, not a captured tab-body reconstruction.' if variant=='custom-range' else ' Date tab follows A29 date/time inputs and month grid.')
    if variant in ('replay-select','replay-active','paper-replay','paper-accepted','paper-processing'):
        frame['annotation']=('A31/A32 geometry: one compact floating replay/trading capsule, with a grip, transport, time, Sell, quantity, unit selector, Buy, P/L, pin and close. A32 sidebar traced in the same order and grouping; state-25 results dock is closed. Screenshot-only presets, sizing/price modes and footer toggles are disabled reference placeholders, not new behavior. Prices/balances remain placeholders.')
    narrow=variant=='reflow' or variant.endswith('-reflow')
    paper_reference=variant in ('paper-replay','paper-accepted','paper-processing')
    width=1870 if paper_reference else 640 if narrow else 1280
    height=884 if paper_reference else 900 if narrow else 800
    c=Canvas(width+48,height+460,frame['id']+' — '+frame['title'])
    c.text(24,30,frame['id']+' / '+frame['title'],'title',width=55 if narrow else 106)
    c.text(24,83,f'{VERSION} · UIS-VIEW-{view:03} · UIS-STATE-{state:03}','meta')
    c.text(24,108,'1870 × 884 reference canvas · matches A32 screenshot dimensions; desktop baseline remains 1280 × 800' if paper_reference else '640px effective desktop zoom; scrolling task surfaces' if narrow else '1280 × 800 CSS px · reference-led geometry · schematic chart / placeholder values','meta',width=140)
    c.parts.append('<g transform="translate(24 136)" data-role="workspace-shell">')
    c.rect(0,0,width,height,'#fff')
    top=88 if narrow else 44
    rail=44
    left=44 if narrow else 48
    right=width-rail
    # Top toolbar: manual ticker, timeframe, indicators and chart commands.
    c.rect(0,0,width,top,'#f7f7f7')
    control(c,8,7,28,'☰')
    control(c,48,7,132,'EURUSD / ticker')
    control(c,188,7,64,'M1 v')
    control(c,260,7,72,'Candles')
    control(c,340,7,96,'Indicators')
    control(c,444,7,76,'Replay',selected=replay)
    if narrow:
        control(c,48,49,92,'Layout v');control(c,148,49,100,'Undo / redo');control(c,256,49,88,'Settings');control(c,352,49,84,'Export')
        control(c,528,7,50,'Bid',selected=True,toggle=True)
        control(c,582,7,50,'Ask',toggle=True)
    else:
        control(c,528,7,100,'Undo / redo');control(c,636,7,92,'Charts 1/2')
        control(c,736,7,56,'Bid',selected=frame.get('visibility','bid') in ('bid','both'),toggle=True)
        control(c,800,7,56,'Ask',selected=frame.get('visibility','bid') in ('ask','both'),toggle=True)
        if variant=='two-chart':control(c,864,7,64,'Sync v')
        control(c,width-344,7,112,'Layout / Save');control(c,width-224,7,92,'Settings');control(c,width-124,7,112,'Export image')
    c.rect(0,top,left,height-top-26,'#fafafa')
    tools=[('cross','Select / crosshair'),('trend','Trendline'),('horizontal','Horizontal line'),('vertical','Vertical line'),('ray','Ray'),('fib','Fibonacci retracement'),('rectangle','Rectangle'),('brush','Brush / editable points'),('text','Text'),('measure','Long / short measurement')]
    for i,(kind,label) in enumerate(tools):
        tool_icon(c,3,top+8+i*43,kind,label,selected=(i==7 and state==6),disabled=(state==8 and i>0))
    # The far-right launch rail stays distinct from its expandable panel.
    c.rect(right,top,rail,height-top-26,'#fafafa')
    launchers=[('list','Watchlist'),('trade','Historical trading'),('objects','Objects / numeric inspection'),('data','Data continuity'),('work','Saved work / recovery'),('bundle','Run bundle viewer — future version'),('output','Local output')]
    for i,(kind,label) in enumerate(launchers):tool_icon(c,right+2,top+10+i*50,kind,label,selected=(i==0 and view==1 and state!=6),disabled=kind=='bundle')
    c.text(right+10,top+10+5*50+49,'later','meta')
    date_task=variant in ('go-to-date','custom-range')
    selection_task=variant=='selection'
    drawer_view=view in (3,4,5,6) or (view==1 and (state==6 or variant=='anchors')) or selection_task
    collapsed=variant in ('collapsed','replay','replay-select','replay-active') or narrow or variant.endswith('-collapsed')
    pw=0 if collapsed else (360 if paper_reference or view==3 or selection_task or (view==4 and state not in (26,28,29)) else 320 if drawer_view else 280)
    panelx=right-pw
    chart_right=panelx
    replay_top=top
    dock_h=186 if view==4 and state!=25 and not narrow and not paper_reference else 0
    if view==7:dock_h=310 if narrow else 250
    if view==8:dock_h=310 if narrow else 250
    if narrow and drawer_view:dock_h=400
    fault_h=60 if view==1 and state in (4,5,7,8) else 0
    replay_top+=fault_h
    chart_h=height-26-replay_top-dock_h
    controller_h=0
    if variant=='two-chart':
        cw=(chart_right-left)/2
        chart(c,left,replay_top,cw,chart_h,True,state,True,1,controller_h)
        chart(c,left+cw,replay_top,cw,chart_h,True,state,False,2,controller_h)
    else:chart(c,left,replay_top,chart_right-left,chart_h,replay,state,controller_h=controller_h,selecting=variant=='replay-select',visibility=frame.get('visibility','bid'),basis=frame.get('basis','Bid'))
    if pw:
        if selection_task:
            window(c,panelx,top,pw,height-top-26,view,state,variant,docked=True)
        elif view==3:
            work_drawer(c,panelx,top,pw,height-top-26,state)
        elif drawer_view:
            title,kind={4:('Paper trading · replay','trade'),5:('Original blocked event','event'),6:('Data continuity','data')}.get(view,('Objects / point editor','objects'))
            # All side panels share the watchlist bounds below/above shell chrome.
            drawer(c,panelx,top,pw,height-top-26,title,state,variant,kind)
        else:
            if variant.startswith('quote-'):quote_inspector(c,panelx,top,pw,height-top-26,frame['visibility'],frame['basis'])
            else:watchlist(c,panelx,top,pw,height-top-26)
    if replay and state!=26:
        replay_controller(c,left,replay_top+chart_h-96 if not narrow else replay_top+chart_h-126,chart_right-left,40,state,variant,paper=view==4,narrow=narrow)
    if date_task:
        ww=344
        wh=586 if variant=='custom-range' else 520
        wx=left+(chart_right-left-ww)/2
        go_to_window(c,wx,top+68,ww,wh,variant=='custom-range')
        frame['surface']='go-to-window-over-chart'
    elif view==7:
        review_dock(c,left,height-26-dock_h,chart_right-left,dock_h,state,variant)
        frame['surface']='inline-confirmation-in-replay-or-work-dock'
    elif view==8:
        export_dock(c,left,height-26-dock_h,chart_right-left,dock_h,state,variant)
        frame['surface']='export-action-in-results-or-chart-dock'
    elif view==2:
        ww=min(720,chart_right-left-64) if not narrow else width-96
        wh=640 if not narrow and variant=='analysis' else 548 if not narrow else 510
        wx=left+(chart_right-left-ww)/2
        wy=top+90 if not narrow else top+240
        window(c,wx,wy,ww,wh,view,state,variant)
        frame['surface']='settings-window-over-chart'
    elif narrow and drawer_view:
        dx=left;dy=height-26-dock_h;dw=chart_right-left;dh=dock_h
        if view==4 and state==25:
            entry_form(c,dx,dy,dw,dh,variant)
        elif view==3:
            work_drawer(c,dx,dy,dw,dh,state)
        else:
            c.parts.append('<g data-role="zoom-task-dock">')
            c.rect(dx,dy,dw,dh,'#fff',weight=2)
            title={1:'Drawing point editor',4:'Paper trading · replay',5:'Original event',6:'Data continuity'}[view]
            c.text(dx+12,dy+26,title,'heading');c.text(dx+dw-24,dy+26,'×','heading')
            controls={1:[('Object / point','[target / point index]'),('Time / price','[time] / [price]')],4:[('Run / cursor','R-014 / completed decision [time]'),('Entry / required level','Buy Limit / [price input]'),('Quantity / SL / TP','[units] / [optional prices]')],5:[('Original event','[identity / time]'),('Missing prerequisite','[historically applicable fact]')],6:[('Series / span','[instrument / side / timeframe]'),('Coverage / receipt','[qualified intervals / status]')]}[view]
            for i,(label,value) in enumerate(controls):field(c,dx+12,dy+48+i*64,dw-24,label,value)
            note_y=dy+dh-140
            state_note(c,dx+12,note_y,dw-24,state,variant,h=74)
            control(c,dx+12,note_y+88,150,'Return to chart')
            control(c,dx+174,note_y+88,dw-186,'Full entry form > 093' if view==4 else 'Task detail / review >')
            c.parts.append('</g>')
        frame['surface']='zoom-task-dock-below-chart'
    else:
        if view==4 and dock_h:bottom_dock(c,left,height-26-dock_h,chart_right-left,dock_h,state,variant)
        frame['surface']=('paper-sidebar-with-floating-replay' if state==25 or paper_reference else 'right-drawer-and-bottom-dock') if view==4 else 'go-to-right-drawer' if date_task else 'symbol-search-right-drawer' if selection_task else 'right-context-drawer' if drawer_view else 'chart-with-watchlist' if pw else 'chart-with-collapsed-panels'
    # Workspace faults are scoped strips, not full-screen replacement pages.
    if view==1 and state in (4,5,7,8):
        note_w=min(520,chart_right-left-24)
        state_note(c,left,replay_top-fault_h,chart_right-left,state,h=fault_h)
    c.rect(0,height-26,width,26,'#f2f2f2')
    footer='Feed [condition] · Working [v] / Saved [v] · Save / authority detail >'
    if state==15:footer='Working v13 applied · Save FAILED v13 · Retained v12 · Retry retention (do not Apply again)'
    if state==7:footer='Working v13 · Save outcome UNKNOWN v13 · Reconcile saved state before repeat'
    c.text(10,height-8,footer,'meta',width=76 if narrow else 170)
    c.parts.append('</g>')
    ay=height+166
    c.text(24,ay,'REVIEW NOTES · outside the product','heading')
    c.text(24,ay+26,'Left: drawing tools. Top: ticker / timeframe / indicators. Right: launch rail and contextual drawer. Chart retained in every frame.','meta',width=76 if narrow else 170)
    c.text(24,ay+90,'Run bundle viewer: future launcher placeholder only, disabled; no V1 viewer or external import is introduced.','meta',width=76 if narrow else 170)
    c.text(24,ay+146,frame['annotation'],'meta',width=76 if narrow else 170)
    reference_note='Reference: E01-load-chart.png; calendar window: A29-range-selection.png, floating placement restored by the user. Calendar action changes the viewport; replay cursor stays unchanged.' if variant in ('go-to-date','custom-range') else 'References: E01 chart shell; E07 settings; A29 Go to; A31/A32 floating replay capsule. Settings, Go to and replay may float. Other tasks dock; state/target/boundary stay scoped.'
    c.text(24,ay+230,reference_note,'meta',width=76 if narrow else 170)
    frame['regions']=[f'UIS-REG-{r}' for r,_,_,_ in panel_content(view,state,variant)]
    if view==1:frame['regions'].append('UIS-REG-004')
    if view==4:frame['regions'].append('UIS-REG-011')
    frame['chart_persistent']=True
    frame['uses_overlay']=view==2 or date_task or replay
    frame['replay_stage']='start-selection' if variant=='replay-select' else 'playing' if variant=='replay-active' else 'event-processing' if state==27 and replay else 'paused' if replay else 'inactive'
    frame['replay_controls']='floating-capsule' if replay else None
    frame['paper_trading_over_replay']=view==4
    frame['future_launchers']=[{'name':'Run bundle viewer','status':'disabled','version':'future'}]
    frame['reference_screenshots']=['screenshots/E01-load-chart.png','screenshots/E07-settings-ready.png']
    if variant in ('go-to-date','custom-range'):
        frame['reference_screenshots'].append('screenshots/authenticated/A29-range-selection.png')
    if replay:
        frame['reference_screenshots']+=['screenshots/authenticated/A30-replay.png','screenshots/authenticated/A31-replay.png']
    if view==4:
        frame['reference_screenshots'].append('screenshots/authenticated/A32-paper-trading.png')
    return c.finish()


def command_enabled(state, action):
    """Gate effects rather than disabling a whole surface, including its exit."""
    mutations = ("Apply", "Commit", "Submit", "Modify", "Request targeted", "Confirm", "Restore layout",
                 "Resume run", "Review replacement", "Review delete", "Generate", "Resolve when",
                 "Play / pause", "Step bar", "Seek forward")
    blocked = {5, 6, 8, 10, 11, 12, 13, 16, 19, 21, 22, 23, 24, 26, 27, 29, 30, 31, 32,
               33, 34, 35, 36, 38, 39, 40, 50, 51, 52, 53, 54, 56, 58, 59, 62, 63, 64}
    if state in blocked and action.startswith(mutations):
        return False
    if state in {8, 16, 24, 32, 40, 56} and action.startswith(("Create", "Arrange", "Cancel selected", "Draw /")):
        return False
    if state == 31 and action.startswith("Cancel selected"):
        return False
    return not any(reason in action for reason in ("(restricted", "(pending", "(estimate pending", "(invalid", "(validation failed", "(already", "(source absent"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = source_states()
    assert set(names) == set(STATES) == set(range(1, 65))
    frames = []

    def add(view, state, title, variant="state", adapt=None):
        number = len(frames)+1
        frames.append({"id": f"WF-FRAME-{number:03}", "file": f"WF-FRAME-{number:03}.svg", "view": view,
                       "state": state, "variant": variant, "title": title,
                       "adapt": adapt or ["UIS-ADAPT-001", "UIS-ADAPT-004", "UIS-ADAPT-005", "UIS-ADAPT-006"],
                       "annotation": names[state][1] + ". " + names[state][2],
                       "gate_g4": gate_status()})

    # Stable IDs 001-064 match the source state numbering, with eight primary
    # frames (001,009,...057); the gallery presents those before state variants.
    for state in range(1, 65):
        add((state-1)//8+1, state, names[state][0])
    for view in range(1, 9):
        add(view, (view-1)*8+1, VIEWS[view][0] + " / zoom reflow", "reflow",
            ["UIS-ADAPT-001", "UIS-ADAPT-002", "UIS-ADAPT-003", "UIS-ADAPT-004", "UIS-ADAPT-005"])
    for view, state, title, variant in [
        (1, 1, "Two-chart comparison and active-chart switch", "two-chart"),
        (1, 6, "Keyboard brush and financial anchor editing", "anchors"),
        (2, 9, "Presentation and study configuration", "analysis"),
        (4, 25, "Pending order modification and cancellation", "pending"),
        (5, 37, "Original resolution publication unknown", "resolution-unknown"),
        (7, 49, "Validated own-backup replacement review", "restore"),
        (7, 49, "Selected layout deletion review", "delete"),
        (7, 49, "Explicit updated-basis restart review", "restart"),
        (8, 57, "Local chart image source and inclusion", "image"),
        (1, 1, "Current-history workspace and explicit replay entry", "current-history"),
        (1, 2, "Instrument search and requested versus adopted selection", "selection"),
        (1, 1, "Replay controls around the retained central chart", "replay"),
        (1, 1, "Expanded chart with right drawer closed", "collapsed"),
        (1, 1, "Bottom calendar action / floating Go to date window", "go-to-date"),
        (1, 1, "Go to / custom viewport range", "custom-range"),
        (1, 1, "Replay / select the starting bar (A30)", "replay-select"),
        (1, 1, "Replay / playing with bottom controls (A31)", "replay-active"),
        (4, 25, "Paper trading over replay / order terms and Sell-Buy strip (A32)", "paper-replay"),
        (4, 28, "Paper replay / accepted order waiting for an eligible event", "paper-accepted"),
        (4, 27, "Paper replay / event processing blocks new decisions", "paper-processing"),
    ]:
        add(view, state, title, variant)
    for view,state,title,variant in [
        (4,25,'Limit entry level and fixed quantity','limit'),
        (4,25,'Stop entry level and fixed quantity','stop'),
        (4,25,'Risk percentage sizing with planned-risk estimate','risk'),
        (4,25,'Risk sizing invalid: missing stop loss','risk-invalid'),
        (4,25,'Valid selected-position partial close','close-partial'),
        (4,25,'Valid selected-position full close','close-full'),
        (2,9,'Settings / Dukascopy data location / valid candidate','data-ready'),
        (2,9,'Settings / data location / invalid path','data-invalid'),
        (2,9,'Settings / data location / validation pending','data-checking'),
        (2,9,'Settings / data location / applied','data-applied'),
        (1,1,'Ask visible with independent Bid calculation basis','quote-ask'),
        (1,1,'Both selected / paired filled Bid and hollow Ask / dual OHLCV and volume','quote-both'),
        (1,1,'Neither candle series visible; basis values retained','quote-none'),
        (1,1,'Ask calculation basis explicitly adopted','quote-ask-basis'),
    ]:add(view,state,title,variant)
    for title,variant in [
        ('Sell fixed quantity / ready matching submission','entry-sell-fixed'),
        ('Changed direction / risk validation pending','entry-sell-risk-pending'),
        ('Changed direction / retained levels invalid','entry-sell-risk-invalid'),
        ('Sell ready / collapsed ticket and reachable editor','entry-sell-fixed-collapsed'),
        ('Sell pending / effective desktop zoom','entry-sell-risk-pending-reflow'),
        ('Sell risk sizing / fresh validation ready','entry-sell-risk'),
        ('Buy fixed edit / validation pending','entry-buy-fixed-pending'),
    ]:add(4,25,title,variant)
    old_meta=json.loads((OUT/'frame-index.json').read_text())
    old_frames={f['id']:f for f in old_meta['frames']}
    for frame in frames:
        frame['visibility']={'quote-ask':'ask','quote-both':'both','quote-none':'none','quote-ask-basis':'ask'}.get(frame['variant'],'bid')
        if frame['variant']=='quote-both':frame['annotation']='Both Bid and Ask selected. Each UTC bucket pairs a filled Bid candle on the left and a hollow Ask candle on the right, with two corresponding volume bars. The header and inspector expose separately labelled Bid and Ask OHLCV. Values and bars are schematic placeholders, not validated market data. Bullish candles use light shades and bearish candles dark shades on filled bodies and hollow borders/wicks. Calculation-side study selection remains independent.'
        frame['basis']='Ask' if frame['variant']=='quote-ask-basis' else 'Bid'
        frame['candle_visibility']={'bid':frame['visibility'] in ('bid','both'),'ask':frame['visibility'] in ('ask','both'),'independent_toggles':True,'scope':'active-chart'}
        path=OUT/frame['file']
        previous=path.read_text() if path.exists() else None
        if frame['id'] in {f'WF-FRAME-{n:03}' for n in (25,68,90,93,94,95,96)} or frame['variant'].startswith('entry-'):
            frame['annotation']='IF-BR-008a: ticket selects without submission. Matching current valid side alone commits; opposite activation has no effect. Any edit invalidates estimates; retain proposed inputs. Late validation cannot re-enable an old draft. Selection keeps focus; announce status; editor return restores invoker. Cancel abandons draft only. Pending/unknown original submission freezes terms and blocks both actions (027/031). No auto-submit or auto-play. Static design only.'
        if frame['id'] in old_frames and frame['id'] not in {f'WF-FRAME-{n:03}' for n in (25,68,90,93,94,95,96)}:
            frame['annotation']=old_frames[frame['id']]['annotation']
        if frame['id'] in {f'WF-FRAME-{n:03}' for n in (25,68,93,94,95,96)} or frame['variant'].startswith('entry-'):
            frame['annotation']='IF-BR-008a: direction selection submits nothing. Matching valid side alone commits; opposite has no effect. Edits supersede estimates; retain inputs. Keep focus; announce status. Editor restores invoker. No auto-submit/play.'
        rendered=render(frame,names)
        old=old_frames.get(frame['id'],{})
        old_version=old.get('artifact_version',old_meta['version'])
        same=previous is not None and rendered.replace(VERSION,old_version)==previous
        frame['gate_g4']=('APPROVED' if gate_status()=='APPROVED' else old.get('gate_g4','PENDING')) if same else 'PENDING'
        frame['artifact_version']=old_version if same else VERSION
        frame['revision_scope']=old.get('revision_scope','unchanged') if same and old_version==VERSION else 'unchanged' if same else 'revised' if previous else 'new'
        if not same:path.write_text(rendered)
    (OUT / "frame-index.json").write_text(json.dumps({"version": VERSION, "frames": frames}, indent=2) + "\n")
    gallery(frames)
    replay_review()
    print(f"Built {len(frames)} offline SVG wireframes, frame-index.json and review gallery ({VERSION}).")


def gallery(frames):
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
             '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' data:; style-src \'unsafe-inline\'; base-uri \'none\'">',
             '<title>Wireframes — Gate G4 review</title><style>body{font:16px/1.5 system-ui,sans-serif;color:#171717;background:#eee;margin:0}main{max-width:1400px;margin:auto;padding:24px}a{color:#17478d}a:focus-visible,summary:focus-visible{outline:3px solid #17478d;outline-offset:4px}nav{display:flex;gap:16px;flex-wrap:wrap}section{margin:40px 0}figure{margin:20px 0;padding:16px;background:white;border:1px solid #777}img{width:100%;height:auto}summary{cursor:pointer;padding:12px;border:1px solid #777;background:#fff}li{margin:8px 0}code{font-size:.9em}</style><main>',
             f'<h1>Low-fidelity wireframes</h1><p>{VERSION} · {len(frames)} frames · Gate G4: {gate_status()}.</p>',
             '<p>Bid and Ask are independent candle-visibility toggles for the active chart: either, both or neither may be shown. Selected buttons have a check mark; pictured default is Bid on / Ask off. Start with the chart shell, chart settings and trading compositions below. The replay bar, settings and the restored Go to date/range window may float above the chart; other tasks use side drawers, bottom docks or inline controls. Open state collections for additional cases; every view also has a desktop zoom frame. These are static design artifacts: pictured controls do not perform actions. Bracketed financial values are placeholders; chart marks are schematic.</p>',
             '<p><strong><a href="replay-review.html">Review corrected WF-FRAME-090 beside A32</a></strong></p><p><a href="../../index.html#ui-dossier">Offline dossier</a> · <a href="../../ui-dossier.md">Canonical Part IV</a> · <a href="frame-index.json">Frame metadata</a></p><nav aria-label="Views">']
    for view in VIEWS:
        parts.append(f'<a href="#view-{view}">{view}. {esc(VIEWS[view][0])}</a>')
    parts.append('</nav>')
    references=json.loads((ROOT/'ui-artifacts/reference-screenshots.json').read_text())['screenshots']
    parts.append('<section id="replay-references"><h2>Replay and paper-trading references</h2><p>User-designated visual references. These filename labels do not amend the earlier controlled A30–A32 scenarios. The replay strip floats as in A31/A32; settings and Go to are the other overlay exceptions.</p>')
    for ref in references:
        path='../../'+ref['file']
        parts.append(f'<figure id="{ref["id"]}"><figcaption>{ref["id"]} · {esc(ref["title"])} · {esc(ref["file"].split("/")[-1])}</figcaption><a href="{esc(path)}"><img loading="lazy" src="{esc(path)}" alt="{esc(ref["description"])}"></a></figure>')
    parts.append('</section>')
    parts.append('<section><h2>Chart workspace basics — revised from the reference screenshots</h2><p>Left drawing toolbar, top chart controls, right feature rail, expanding contextual panels; floating settings and Go to date/range windows. Run bundle viewer is reserved for a future version.</p>')
    for number in (25,68,90,93,94,95,96,107,108,109,110,111,112,113,77,27,37,92,104,99,100,101,102,78,79,80,26,30,32,55,15,76,97,98,103,105,106,1,75):
        parts.append(figure(frames[number-1]).replace('id="WF-FRAME-', 'id="featured-WF-FRAME-'))
    parts.append('</section>')
    for view in VIEWS:
        group = [f for f in frames if f["view"] == view]
        primary = group[0]
        parts.append(f'<section id="view-{view}"><h2>{view}. {esc(VIEWS[view][0])}</h2>')
        parts.append(figure(primary))
        parts.append(f'<details><summary>State, disclosure and zoom variants ({len(group)-1})</summary>')
        for frame in group[1:]:
            parts.append(figure(frame))
        parts.append('</details></section>')
    parts.append('<p>Approval covers geometry, grouping, safety context and adaptation of this version. High-fidelity design and rendered accessibility verification remain downstream.</p></main></html>')
    (OUT / "index.html").write_text("\n".join(parts) + "\n")


def replay_review():
    """Compare authored workspace geometry with the user's static PNG reference."""
    namespace = 'http://www.w3.org/2000/svg'
    ET.register_namespace('', namespace)
    source = ET.parse(OUT / 'WF-FRAME-090.svg').getroot()
    product = ET.Element(f'{{{namespace}}}svg', {'width': '1870', 'height': '884', 'viewBox': '0 0 1870 884'})
    for child in source:
        if child.tag in (f'{{{namespace}}}style', f'{{{namespace}}}defs'):
            product.append(copy.deepcopy(child))
    shell = copy.deepcopy(source.find(f".//{{{namespace}}}g[@data-role='workspace-shell']"))
    shell.attrib.pop('transform', None)
    product.append(shell)
    previews = OUT / 'previews'
    previews.mkdir(exist_ok=True)
    ET.ElementTree(product).write(previews / 'WF-FRAME-090-product.svg', encoding='unicode', xml_declaration=True)
    (OUT / 'replay-review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'">
<title>A32 / corrected WF-FRAME-090</title><style>
body{font:16px/1.5 system-ui;background:#eee;color:#171717;margin:24px}a{color:#17478d}
.compare{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}figure{margin:0;background:white;padding:12px}img{width:100%;height:auto}a:focus-visible{outline:3px solid #17478d}@media(max-width:1000px){.compare{grid-template-columns:1fr}}</style>
<h1>A32 / corrected WF-FRAME-090</h1><p>WF-SET-001-r14 · Gate G4 approved for all 113 wireframes. Single floating replay capsule, paper-trading sidebar aligned to watchlist bounds, results closed. Both workspaces use 1870 × 884. Wireframe values are placeholders; disabled reference controls do not add supported features.</p>
<div class="compare"><figure><figcaption>A32 reference · <a href="../../screenshots/authenticated/A32-paper-trading.png">Full size</a></figcaption><a href="../../screenshots/authenticated/A32-paper-trading.png"><img src="../../screenshots/authenticated/A32-paper-trading.png" alt="Original A32 paper trading screenshot"></a></figure>
<figure><figcaption>Corrected WF-FRAME-090 · <a href="previews/WF-FRAME-090-product.svg">Full size</a></figcaption><a href="previews/WF-FRAME-090-product.svg"><img src="previews/WF-FRAME-090-product.svg" alt="Corrected chart workspace with floating replay capsule and right paper trading sidebar"></a></figure></div>
<p><a href="WF-FRAME-090.svg">Full annotated wireframe</a> · <a href="index.html">Wireframe gallery</a></p></html>''')


def figure(frame):
    return (f'<figure id="{frame["id"]}"><figcaption><strong>{frame["id"]} — {esc(frame["title"])}</strong> '
            f'· UIS-VIEW-{frame["view"]:03} / UIS-STATE-{frame["state"]:03} '
            f'· <a href="{frame["file"]}">Open at full size</a></figcaption>'
            f'<a href="{frame["file"]}"><img loading="lazy" src="{frame["file"]}" '
            f'alt="{esc(frame["title"])}: {esc(frame["annotation"])}"></a></figure>')


if __name__ == "__main__":
    main()
