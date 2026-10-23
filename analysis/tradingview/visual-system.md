# Visual System — Dukascopy Chart Workspace and Historical Trading

## Document status

- Revision: 7 — 21 October 2026; exact user light/dark neutrals, theme-matching toolbars and dark green/red text on light green/red trade-button fills.
- Status: `READY_FOR_WIREFRAME_DESIGN`.
- Interface structure: [ui-dossier.md](ui-dossier.md), revision 21 (Parts I–III semantics from revision 20), Part III Sections 10–14; `READY_FOR_VISUAL_OR_WIREFRAME`.
- Interface requirements: the same dossier, Part I; G2 `SATISFIED` by explicit acceptance on 19 October 2026.
- Interaction model: the same dossier, Part II. These canonical parts explicitly replace standalone interface-structure.md, interface-requirements.md and interaction-model.md.
- Brand/identity authority: none supplied. TradingView reference styling is evidence, not an approved brand or permission to reproduce its identity.
- Existing visual evidence inspected: screenshots/E01-load-chart.png, screenshots/E07-settings-ready.png and screenshots/E18-dark-state.png. Only original PNG pixels were inspected; captured HTML was not executed or embedded.
- Upstream semantics: requirements-dossier.md revision 14, domain-model.md revision 1 and architecture-dossier.md revision 2, through their traceability in ui-dossier.md. Existing DEFER-001–DEFER-007 and ADV-VER-001 remain outstanding under their existing owners.

**Authority boundary:** the user accepted all six recommendations on 19 October 2026: “I accept all six recommendations”. VIS-DEC-001–VIS-DEC-006 therefore select option A. The derived values below are canonical visual design authority. Requirements, domain, architecture and accepted G2 capabilities retain their existing authority. This approval does not approve future wireframes or claim implemented accessibility conformance.

## Visual scope

**Later structural direction (20 October 2026):** ui-dossier.md revision 10, UIS-PAT-006–011, governs the reference-led shell. WF-SET-001-r7 corrects the rejected docked replay interpretation: the compact A31/A32 replay capsule floats over the chart, and the full-height paper sidebar follows A32. Default paper entry leaves Results closed. Settings and Go to are the other floating exceptions. Frame 090 uses the A32 reference canvas for comparison. Approved tokens and domain rules are unchanged; the future run bundle viewer remains disabled. Affected r6 high-fidelity derivatives are stale pending propagation of reviewed geometry.

Govern all eight UIS-VIEW-001–UIS-VIEW-008 task surfaces: chart/replay, configuration, retained work/recovery, simulated instructions/positions/results, original-event resolution, continuity/access, destructive review and local output. Carry the same meanings into chart images and own-run reports where applicable. Backup integrity and inclusion remain upstream semantics, not visual design choices.

Preserve supported desktop mouse/keyboard work, two-chart access, the accepted 1280×800 CSS-pixel baseline and zoom/reflow obligations. No mobile, additional selectable color-vision theme, live broker execution, new chart behavior, credential flow, provider timeout, numerical convention or initial market selection is introduced. No wireframes, rendered screens, framework, component library or implementation tokens are specified.

## Human-approved visual direction

All six recommendations were explicitly accepted together on 19 October 2026: “I accept all six recommendations”. Alternatives are retained for provenance; Project decision is option A in every row.

| ID | Decision | Alternatives / tradeoffs | Recommendation / rationale | Project decision | Acceptance evidence |
|---|---|---|---|---|---|
| VIS-DEC-001 | Character and continuity | A: restrained technical workspace retaining familiar chart emphasis; B: more spacious general productivity language, with less information visible; C: close reference appearance, with greater imitation/continuity burden | **A:** calm chrome, compact financial evidence, clear scope and state labels. Retain familiarity while giving the local simulation its own identity | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |
| VIS-DEC-002 | Typography strategy | A: offline system sans with tabular numerals and system monospace for identifiers; B: bundled IBM Plex Sans/Mono with a consistent technical voice, requiring local font distribution review; C: bundled Inter with system monospace, also requiring distribution review | **A:** works offline without new font assets; prioritize stable numerals, explicit units and readability over font identity | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |
| VIS-DEC-003 | Neutral/action palette direction | A: slate neutrals with blue action/focus; B: warmer neutral surfaces with indigo action; C: grayscale actions with strongly outlined focus, reserving hue almost entirely for data/status | **A:** restrained blue is familiar for selection and avoids assigning financial direction to action controls | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |
| VIS-DEC-004 | Density posture | A: compact chart/list work, more breathing room for forms and consequential review; B: uniformly comfortable controls with more sequential disclosure; C: uniformly dense workstation, with greater crowding risk | **A:** supports the two-chart workload without compressing target, risk, error or confirmation information. This defines contextual density, not a new density setting | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |
| VIS-DEC-005 | Realization of required light/dark themes | A: equal light/dark systems using paper/slate and charcoal/slate, identical semantic roles; B: equal light/dark with warmer paper and warm charcoal | **A:** both themes receive full contrast/state treatment. This choice does not select a startup theme or add automatic theme switching | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |
| VIS-DEC-006 | Financial/chart palette direction | A: teal rising, rose falling, distinct blue/violet/ochre study identities; B: blue rising, orange falling, alternate violet/teal study identities; C: monochrome candles with strong hollow/filled treatment and colored study lines | **A (historical; overridden by VIS-DEC-007):** familiar financial reading with mandatory shape/text redundancy; status success/error remain a separate semantic vocabulary. B improves hue separation but carries a larger continuity change | ACCEPTED — A | User, 19 October 2026: “I accept all six recommendations” |

The original accepted package is option A in all six rows. VIS-DEC-007 below supersedes the financial hues and toolbar surfaces by explicit later user instruction. The designer finalized the concrete values below within that direction; no additional visual assumption is needed. A later direction change requires updating dependent tokens and checking both themes.

## Visual principles

| ID | Principle | Operational consequence | Sources/rationale |
|---|---|---|---|
| VIS-PRIN-001 | The financial basis travels with evidence | Identify instrument/provider, period, bid/ask, current/replay mode, actual cursor and selected chart using stable text roles. Hover time never looks like the run boundary | UIS-REG-001/003/011; UIS-PAT-002; UIR-INFO-001/006 |
| VIS-PRIN-002 | Working, executed and saved are separate facts | Show independently named state scopes; an accepted order, coherent fill, saved checkpoint and complete output never share a single undifferentiated success indicator | UIS-PAT-001/003; UIR-STATE-007/009/014 |
| VIS-PRIN-003 | Calm evidence, explicit exceptions | Use ordinary readable hierarchy for history; reserve stronger emphasis for active target, blocked prerequisite, uncertainty and consequential action. A financial loss is not an application failure | UIS-REG-002/014/015/021; UIR-INFO-010/011/014 |
| VIS-PRIN-004 | Density yields to task meaning | Preserve target, units, remainder, eligibility, planned-risk limitation and cancel/confirm meaning when space tightens. Secondary detail may collapse under upstream rules | UIS-ADAPT-001–UIS-ADAPT-004; UIR-SAFE-004 |
| VIS-PRIN-005 | Evidence limits remain visible | Missing, warm-up, stale, partial, provisional, blocked, failed and publication-unknown receive distinct wording; no fake zero or implied finality | UIR-STATE-002–UIR-STATE-005/010; UIS-STATE-033–UIS-STATE-048 |
| VIS-PRIN-006 | The plot has an equivalent readable account | Preserve numeric inspection, explicit anchors and point editing; series, direction, selection and status carry non-color meaning in both themes | UIS-PAT-004; UIR-A11Y-001–UIR-A11Y-006 |

## Hierarchy translation

| Structural role | Visual treatment | Non-color cue / accessibility note | Sources |
|---|---|---|---|
| Primary | Normal high-contrast text; restrained semibold headings/active target; chart evidence dominates chrome through reduced decoration | Named context and persistent selection marker; labels and units remain readable | UIS-REG-001/002/005/006/008/012/014/016/018/019/024–026 |
| Secondary | Smaller supporting role with full text contrast; quiet separators instead of nested cards | Named save/feed scopes remain readable; promote a failure to safety emphasis | UIS-REG-004; UIS-DISC-001/003 |
| Contextual | Explicit target/draft/preview label beside scoped content, with consistent inset separation | Preview uses text plus a dashed outline; candidate is not adopted state | UIS-REG-006/012; IF-DISC-002/003 |
| Diagnostic/on-demand | Readable compact text; monospaced identifiers only; subordinate heading and disclosure marker | Required reason and next action stay outside optional diagnostics | UIS-REG-014/016/020; UIS-DISC-003–UIS-DISC-006 |
| Safety-critical | High-contrast heading/label, explicit target and consequence, distinct border/symbol and separation from ordinary detail | Text states block, uncertainty or destructive effect; never hue alone, flashing or universally red backgrounds | UIS-REG-003/007/009–013/015/017/019/021–023/025; UIR-SAFE-001–UIR-SAFE-005 |

## Typography

Concrete values in this document are canonical design values within the accepted direction. Type size, line height, spacing, radius, border and icon dimensions use CSS pixels as design reference units, not limits on text enlargement. No role uses a proprietary font asset.

| ID | Role / semantic token | Family | Size / weight / line height | Usage | Sources |
|---|---|---|---|---|---|
| VIS-TYPE-001 | type.title | System sans: system-ui, Segoe UI, sans-serif | 20 / 600 / 28 | Task/view title; avoid marketing-scale headings in the workspace | UIS-VIEW-001–UIS-VIEW-008; VIS-DEC-001/002 |
| VIS-TYPE-002 | type.heading | Same sans | 16 / 600 / 24 | Region heading, scope and consequence summary | UIS-REG-001–UIS-REG-026 |
| VIS-TYPE-003 | type.body | Same sans | 14 / 400 / 20 | Forms, reasons, review content, persistent outcomes | UIR-INFO-007–UIR-INFO-016 |
| VIS-TYPE-004 | type.control | Same sans | 14 / 500 / 20 | Commands, field labels, named actions | UIS-ACT-001–UIS-ACT-020 |
| VIS-TYPE-005 | type.data | Same sans, lining tabular numerals | 13 / 400 / 20 | Watchlists, values and results; emphasize selected target at 600 | UIR-INFO-003/004/009/010 |
| VIS-TYPE-006 | type.meta | Same sans | 12 / 400 / 16 | Axis labels, observation times, secondary provenance; never sole treatment for an error or consequence | UIS-REG-002/004/014/019 |
| VIS-TYPE-007 | type.identifier | System monospace: ui-monospace, Consolas, monospace | 12 / 400 / 18 | Safe correlations, retained version identifiers; prose remains sans | UIR-INFO-013/015; UIS-PAT-005 |

Use sentence case, explicit bid/ask and USD/quantity units; avoid long all-capital instructions. Right-align comparable numeric columns and align decimal places through typography/column formatting, without altering stored precision or selecting domain rounding. Signs accompany signed changes; a dash must have an explained absence reason rather than masquerade as zero. No critical identifier, price, remainder or consequence is available only as truncated text. [UIR-INFO-001/003/007–010/014; DEFER-004; UIS-ADAPT-003]

## Color system

Pairs are **light / dark**. Exact colors realize accepted VIS-DEC-003/005/006 and pass the contrast pair checks recorded below. Both themes preserve the same role meanings; a startup-theme policy remains outside this visual decision.

### Neutral/surface/text roles

| ID | Token | Value light / dark | Meaning/use | Contrast/accessibility note |
|---|---|---|---|---|
| VIS-COLOR-001 | color.surface.base | #FFFFFF / #151619 | Application background | Decorative separators may be quieter than required boundaries |
| VIS-COLOR-002 | color.surface.content | #FFFFFF / #151619 | Plot, values, ordinary content | Primary text and chart marks tested on this surface |
| VIS-COLOR-003 | color.surface.raised | #FFFFFF / #151619 | Temporary task/review surface | Distinct edge, not shadow alone |
| VIS-COLOR-004 | color.text.primary | #1E293B / #D1D4DC | Required text, targets and values | Normal text target at least 4.5:1 |
| VIS-COLOR-005 | color.text.secondary | #1E293B / #D1D4DC | Supporting readable text | Same normal-text target; never opacity-only status |
| VIS-COLOR-006 | color.border.control | #D4DAE3 / #2A2B30 | Required control boundary, chart reference edges | User-selected subtle neutral stroke; readable control labels/marks and focus carry identification; never sole essential cue |
| VIS-COLOR-007 | color.border.separator | #D4DAE3 / #2A2B30 | Decorative grouping and nonessential grid | Never sole indicator of control/state/data essential to understanding |

### Action/status roles

| ID | Token | Value light / dark | Meaning | Non-color cue / usage |
|---|---|---|---|---|
| VIS-COLOR-008 | color.action.primary | #1D4ED8 / #93C5FD | Ordinary committing action, selection accent | Explicit verb and target; selected marker independent of focus |
| VIS-COLOR-009 | color.action.onPrimary | #FFFFFF / #0F172A | Text on solid primary action | Do not reuse primary-accent text on its own fill |
| VIS-COLOR-010 | color.focus | #1D4ED8 / #93C5FD | Keyboard focus only | Continuous outer outline and surface-colored separation; coexist with selected marker |
| VIS-COLOR-011 | color.status.success | #166534 / #86EFAC | Confirmed scoped completion | Check symbol plus exact outcome/version; never profitability |
| VIS-COLOR-012 | color.status.warning | #92400E / #FCD34D | Known limitation, unresolved gap, stale/partial evidence | Warning symbol plus specific reason/time/span |
| VIS-COLOR-013 | color.status.error | #B91C1C / #FCA5A5 | Known rejection/failure or destructive command emphasis | Error symbol, explicit reason or destructive verb; never loss alone |
| VIS-COLOR-014 | color.status.uncertain | #6D28D9 / #D8B4FE | Unknown publication/operation outcome | Question symbol and “Outcome unknown”; do not imply failure, success or rollback |
| VIS-COLOR-015 | color.status.neutral | Same as color.text.secondary | Pending, paused, empty, unavailable, closure or read-only descriptions | Distinct text and appropriate symbol; shared neutral hue never erases different meanings |

Status foregrounds use content/raised surfaces rather than untested tinted backgrounds. High-contrast focus treatment must also work beside accent-filled controls. Selected surfaces keep normal text and a visible marker; any tint is supplemental. Destructive commands use explicit verbs, not a red icon alone. No financial direction, entry side or P&L sign uses a status token. [UIR-A11Y-002/004/005; UIS-PAT-001/004; UIR-SAFE-001–005]

## Spacing and density

| ID | Token/tier | Value | Intended use / constraints |
|---|---|---|---|
| VIS-SPACE-001 | space.micro / space.tight / space.compact | 2 / 4 / 8 | Marks, label-to-value groups, related controls; not unrelated action groups |
| VIS-SPACE-002 | space.related / space.group / space.section | 12 / 16 / 24 | Form items, semantic groups and region breaks |
| VIS-DENS-001 | density.evidence | 13/20 data type; 8 related spacing | Plot-adjacent values, lists and tables; preserve readable rows, units and keyboard selection |
| VIS-DENS-002 | density.review | 14/20 body; 12–16 group spacing | Configuration, resolution, confirmation and output; no compressed consequence text |

These tiers apply to task context rather than new user-selectable modes. Control targets should satisfy accepted WCAG 2.2 AA target-size requirements through dimensions or permitted spacing; compact icon artwork does not define the hit target. Text enlargement/reflow overrides nominal row/control size. Do not shrink type to keep both charts and every secondary region simultaneously visible. [VIS-DEC-004; UIR-A11Y-004; UIS-ADAPT-001–004]

## Surfaces and layering

| ID | Role | Treatment | When to use / avoid | Sources |
|---|---|---|---|---|
| VIS-SURF-001 | Persistent work | Content surfaces, quiet separators; no shadow per chart/study row | Separate genuine regions; avoid a card around every number | UIS-REG-001/002/014; VIS-DEC-001 |
| VIS-SURF-002 | Controls and task groups | radius.control = 4; border.control = 1 | Consistent small rounding; avoid pill-shaped ordinary financial fields | VIS-DEC-001/004 |
| VIS-SURF-003 | Temporary focused task | radius.surface = 8; visible boundary; optional restrained shadow | Configuration/review/output if downstream composition uses a temporary layer; do not mandate modality or placement | UIS-VIEW-002/007/008 |
| VIS-SURF-004 | Safety emphasis | Strong heading, explicit symbol/label, separated consequence group | Original block, exact destructive scope and uncertain publication; do not dim the required target or cancellation path | UIS-REG-015/017/021–023; UIS-PAT-003 |

Layer order follows existing task semantics: work, contextual inspection, scoped temporary review, focus/critical labels. Shadows never supply the only boundary. Numeric elevation/shadow values remain downstream decoration within this hierarchy, not new global tokens.

## Interaction and semantic states

These meaning rules are requirements-derived; color references use the canonical palette above. Every status includes scope. Multiple independent statuses can coexist.

| ID | State | Visual treatment / required distinction | Sources |
|---|---|---|---|
| VIS-STATE-001 | Default / hover / focus / selected | Quiet default; hover surface/boundary cue without moving content; focus outline; selected target has marker plus named current identity. Hover, focus and selection remain independently visible | UIS-PAT-004; UIS-ADAPT-002; UIR-A11Y-001/003 |
| VIS-STATE-002 | Disabled / read-only / locked / hidden | Unavailable command remains recognizable with adjacent reason; read-only names authority restriction, locked names annotation restriction, hidden retains object-list identity. Do not fade required reason below contrast target | UIS-STATE-008/016/024/032/040/056; UIR-STATE-006/013 |
| VIS-STATE-003 | Loading / evaluating / submitting | Scope and actual phase in text; optional progress symbol. Retain correctly labelled prior state; no fake percentage or success check | UIS-STATE-002/010/019/027/034/036/042/052/059; UIR-FEED-001/003 |
| VIS-STATE-004 | Empty / unavailable / warm-up / actual end | Distinct plain-language reason beside absent data; no fabricated zero. Archive end differs from unloaded range; no-result history is not zero P&L | UIS-STATE-003/011/018/026/035/044/050/058 |
| VIS-STATE-005 | Preview / committed / invalid | Preview tag and dashed boundary; committed result explicitly labelled; invalid field has symbol, message and boundary, preserving prior valid settings/instruction | UIS-STATE-006/009/012/015/023/029; UIR-STATE-006 |
| VIS-STATE-006 | Unsaved / saving / saved / failed / unknown save | Literal labels with working versus retained version; saved check only for exact acknowledged version; known error and unknown-publication cues differ | UIS-STATE-007/020/021/031; UIR-STATE-007; UIS-PAT-001 |
| VIS-STATE-007 | Playing / paused / blocked / end | Text plus play/pause/blocked/end symbols, explicit cursor and step reference; persistent block reason/next action. Paused is not failed; end is not forced closure | UIS-STATE-001/005/030/033; IF-JRN-005/010 |
| VIS-STATE-008 | Draft / accepted waiting / effective pending / triggered / filled / cancelled | Named instruction state and target; fill has recorded quantity/time/price, not merely stronger color. Save outcome separate; triggered never uses “filled” | UIS-STATE-025/027/028/031; UIR-STATE-009 |
| VIS-STATE-009 | Open / reduced / closed independent position | Identity, remaining quantity and protection readable; reduced/closed state text. Direction and closing action named; selected position not inferred from color | UIS-REG-013; UIR-STATE-011; IF-JRN-009 |
| VIS-STATE-010 | Stale / retained original / superseded draft | Stale identifies observation/time/limitation; retained-original badge names run basis, not an error; superseded estimate is nonactionable and labelled for review | UIS-STATE-013/031/038/040/060; UIR-STATE-012 |
| VIS-STATE-011 | Receiving / no recent receipt / closure / offline / denied / recovery | Separate text conditions with receipt/event-time labels; known closure needs qualification. Recovery shows known span/phase; no connection-green claim of complete history | UIS-STATE-004/014/039/041–048; UIR-STATE-003/004 |
| VIS-STATE-012 | Partial / provisional / completed / final | Literal qualifier plus scoped interval/version; optional dashed provisional edge. Completed period does not mean final provider publication; partial never uses complete-progress styling | UIS-STATE-042/044/047; UIR-STATE-005 |
| VIS-STATE-013 | Blocked prerequisite / incompatible evidence | Persistent original event/time, missing fact and permitted next action; warning symbol and no execution-completion mark; incompatible restart route explicitly distinguished | UIS-STATE-030/033–040; UIR-INFO-011 |
| VIS-STATE-014 | Destructive review / stale target / preparing / cancelled / known replaced / unknown | Exact consequence and target/version retained. Changed scope invalidates review; preparation has no success check; cancelled says unchanged only when known; unknown uses reconciliation label | UIS-STATE-049–056; IF-CONF-001–003 |
| VIS-STATE-015 | Output complete / incomplete / failed / unknown | Name pinned source/kind and actual artifact outcome; check only for verified matching complete output; incomplete and unknown retain explicit labels | UIS-STATE-057–064; UIR-INFO-016 |

## Iconography

| ID | Rule | Treatment / constraints | Sources |
|---|---|---|---|
| VIS-ICON-001 | Consistent functional marks | Simple outline geometry; nominal 16/20/24 artwork family, consistent optical weight; no new logo or proprietary reference marks | VIS-DEC-001; reversible coherence rationale |
| VIS-ICON-002 | Meaning accompanies unfamiliar/consequential actions | Named actions for entry, close, rewind, restart, restore and delete; symbol plus text for unknown, blocked, stale and failure. Routine icons have accessible names and visible explanation on focus as well as hover | UIR-A11Y-001–005; UIR-SAFE-001–004 |
| VIS-ICON-003 | Financial identity differs from status | Buy/sell and rising/falling carry explicit text/shape; success/error marks never stand for gain/loss | UIR-INFO-007/009/010; UIR-A11Y-005 |

## Motion

| ID | Purpose | Treatment / range | Reduced-motion behavior | Sources |
|---|---|---|---|---|
| VIS-MOTION-001 | Optional local affordance continuity | 100–150 ms nonessential hover/disclosure transition; no bouncing, flashing status, chart sweep or decorative price pulse | Immediate state change; same visible outcome | UIR-A11Y-006; UIS-ADAPT-005 |
| VIS-MOTION-002 | Financial progression and processing | Render actual coherent updates without cosmetic interpolation of prices, fills or cursor; pending text persists independently of animation | Preserve explicit play/pause/speed/step semantics and event ordering; optional progress animation becomes a static mark plus phase | IF-JRN-005; UIR-FEED-002/003; ORDER-005 via UIS-PAT-002 |

## Data visualization

| ID | Concern | Visual rule / semantic meaning | Accessibility / uncertainty | Sources |
|---|---|---|---|---|
| VIS-DATA-001 | Financial direction | data.direction.up = #16A34A / #22C55E; down = #DC2626 / #F87171. Border/wick up = #15803D / #16A34A; down = #C91F1F / #EF4444. Filled Bid bodies use direction fill with slightly darker same-hue border; Ask bodies remain hollow on the plot surface with corresponding direction edges. Quote side owns body fill: Bid filled; Ask hollow, as explicitly requested on 21 October 2026. Direction retains the up/down palette and open-left / close-right ticks with explicit OHLC; flat bars are neutral and identified numerically | Direction uses open/close geometry, left open/right close ticks and readable OHLC/signs, not hue. Hollow/filled denotes quote side, never rising/falling. Direction is relative open/close, not account success/failure; user candle-color settings must preserve non-color reading | VIS-DEC-006; UIR-INFO-003; UIR-A11Y-005; FR-10 via UIR-TASK-004 |
| VIS-DATA-002 | Studies and comparison identity | data.series.1 blue #1D4ED8 / #93C5FD; data.series.2 violet #6D28D9 / #C4B5FD; data.series.3 ochre #92400E / #FCD34D. Retain instance label, line pattern and legend sample; additional instances vary pattern with explicit identity | Stable identity across chart/legend/numeric inspector/themes; avoid hue-only distinction or inventing new study families. Bands have outlined boundaries; fill is supplemental | UIR-INFO-003/005; UIS-REG-002; UIR-A11Y-005 |
| VIS-DATA-003 | Axes, grids and crosshair | Readable axis text, quiet optional grid, stronger crosshair/reference line with numeric labels; essential line edges meet non-text contrast target | Grid is decorative; crosshair is not replay cursor. No display-timezone change to source UTC buckets | UIR-INFO-003/006; UIS-REG-001–003; UIR-TASK-004 |
| VIS-DATA-004 | Cursor, selection and active chart | Explicit run cursor label/reference, selected observation marker and active-chart edge/label use separate roles | Neither shared color nor hover movement can re-identify run boundary or command target; numeric selection alternative retained | UIS-ADAPT-002; UIS-PAT-002/004 |
| VIS-DATA-005 | Annotation versus execution | User drawings retain object/type identity and visible selected handles/lock/hidden list indicators; position-measurement text says analysis/measurement. Execution facts carry order/position identity and recorded state | Distinct line patterns/labels distinguish reference levels, pending terms and recorded effects; no invented order from drawing, inferred intrabar path or automatic trading marker capability | UIR-INFO-005/009/010; IF-JRN-003/008/009 |
| VIS-DATA-006 | Missing and qualified evidence | Explain unavailable/warm-up/gap intervals; do not interpolate missing price history into apparent continuity. Provisional/partial evidence retains explicit qualifier and boundary treatment | Proven closure distinguished from unresolved gap; no fake zero volume or substituted latest value. No shading/annotation exposes post-cursor facts | UIR-STATE-002–005; UIR-CONT-005; UIS-PAT-002/005 |
| VIS-DATA-007 | Recorded financial results | Tabular numeric alignment, explicit signed USD/units, separate fees and scoped aggregate/result labels. Gains/losses use financial direction roles with sign; zero neutral | Unavailable metrics show reason, not zero. Explicit stop-first/full-fill/bar-touch and original FX/specification/evidence labels remain where upstream requires | UIR-INFO-009/010; UIS-REG-014/025; IF-JRN-011; ASM-01/02 |
| VIS-DATA-008 | Coverage/progress | Distinguish requested span, qualified subset, unresolved spans, local receipt, display and retained publication | Known phase and counts only; no invented provider deadline/percentage; retained-run basis remains independent of revised catalog | UIS-REG-018–020; UIS-STATE-041–048; DEFER-002/006 |

| VIS-DATA-009 | Quote-side identity and overlap | Explicit user direction, 21 October 2026: Bid candle bodies filled; Ask bodies hollow. Preserve this grammar in single-side and dual-side modes. Both-visible candles occupy stable adjacent Bid-left / Ask-right slots within the same UTC bucket, with no artificial timestamp shift. Corresponding volume bars use the same aligned slots: Bid filled, Ask hollow. A legend and named inspector identify each side | Both selected exposes separate Bid and Ask O/H/L/C/V readouts for the same selected bucket and two provider-qualified volume bars per bucket. Volume is each side's own provider value, not duplicated from the calculation basis; missing-side values retain their reason. Studies still name the independently selected calculation basis. Candle direction uses open-left / close-right ticks, OHLC and existing direction palette, not body fill. Same semantics in both themes; retained replay boundary and original price/time units unchanged | Direct user request, 21 October 2026; UIR-INFO-018; UIS-PAT-012; VIS-DATA-001; VIS-A11Y-003 |

## Semantic design tokens

The tables above are the canonical semantic token registry. Downstream technical standards may map these tokens to their chosen mechanism while preserving the meanings and approved values. Action, focus, series and status roles remain separate even where a hue is reused: labels, patterns and scoped marks disambiguate meaning, and separate roles allow later semantic changes without conflating categories.

| Token ID | Token family | Value/reference | Semantic role / scope |
|---|---|---|---|
| VIS-TOKEN-001 | type.title/heading/body/control/data/meta/identifier | VIS-TYPE-001–007 | Reusable typography across eight views and relevant output labels |
| VIS-TOKEN-002 | color.surface.*, color.text.*, color.border.* | VIS-COLOR-001–007 | Neutral hierarchy; shared light/dark mapping |
| VIS-TOKEN-003 | color.action.*, color.focus | VIS-COLOR-008–010 | Action contrast, selected cue and independent keyboard focus |
| VIS-TOKEN-004 | color.status.* | VIS-COLOR-011–015 | Named scoped outcomes with VIS-STATE non-color grammar |
| VIS-TOKEN-005 | space.*, density.evidence/review | VIS-SPACE-001/002; VIS-DENS-001/002 | Related-item rhythm and contextual density; no fixed screen geometry |
| VIS-TOKEN-006 | radius.control/surface, border.control | VIS-SURF-002/003 | Reusable edge language; values in design pixels |
| VIS-TOKEN-007 | data.direction.*, data.series.* | VIS-DATA-001/002 | Financial/series identity distinct from action/status |
| VIS-TOKEN-008 | motion.affordance | VIS-MOTION-001 | Optional short continuity; zero with reduced motion |

## Accessibility realization and verification obligations

- **VIS-A11Y-001:** Under accepted UIR-A11Y-004/005, normal text at least 4.5:1, large text at least 3:1 and required non-text control/meaningful graphical distinctions at least 3:1 against adjacent colors. Evaluate actual state/background pairs and both themes; decorative grids do not carry essential information. Palette arithmetic is not a conformance certificate.
- **VIS-A11Y-002:** Focus remains visible and unobscured through selected/hover/error states and temporary layers; focus is a 2-pixel continuous outline with a 2-pixel surface-colored separation. Preserve target label and selected cue independently. [UIR-A11Y-001/003/004; UIS-PAT-004]
- **VIS-A11Y-003:** No color-only financial direction, series, status, selection or uncertainty. Distinguish every state in the state matrix by words and appropriate mark/pattern. Numeric/anchor/point alternatives and explicit units remain available. [UIR-A11Y-002/003/005]
- **VIS-A11Y-004:** Allow text enlargement, wrapping and sequential non-chart reflow without fixed-size clipping; both charts and primary actions remain reachable. Check required target/risk/consequence content at enlargement rather than merely checking base type size. [UIS-ADAPT-001–004]
- **VIS-A11Y-005:** Reduced motion removes optional transitions and animated processing marks; retain phase text, critical feedback and replay controls. [UIR-A11Y-006; UIS-ADAPT-005]

## Existing-interface visual continuity

| ID | Continuity need | Retain / consolidate / replace | Treatment | Evidence/authority |
|---|---|---|---|---|
| VIS-CONT-001 | Chart-led technical reading | Retain useful convention, subject to VIS-DEC-001 | Compact sans values, quiet grid, recognizable plot/legend hierarchy | E01-load-chart.png; evidence, not exact-parity authority |
| VIS-CONT-002 | Light/dark and candle customization | Consolidate into paired semantic roles | Both themes preserve state and numeric meaning; improve required contrast rather than copying faint labels | E07-settings-ready.png, E18-dark-state.png; FR-10 via UIR-TASK-004 |
| VIS-CONT-003 | Local application identity | Replace reference-specific brand/account affordances | No TradingView mark, upgrade/cloud/account decoration or unselected menu capability becomes part of this system | UIS scope; screenshots are reference evidence only |
| VIS-CONT-004 | Recovery/simulation meaning | Extend visual clarity within approved scope | Independent accepted/executed/saved labels, original-event reason and exact review scope | UIS-PAT-001–005; no runtime replication claimed |

No inventory of implemented local styling exists: this is a greenfield application with reference screenshots. Near-duplicate runtime values cannot be audited or claimed consolidated. No licensed font or brand asset is required by the accepted direction.

## Accepted visual assumptions

None. Upstream ASM-01/ASM-02 remain accepted simulation assumptions, not new visual assumptions; their visibility is preserved by VIS-DATA-007.

## Upstream blockers and contradictions

No new blocking structure, accessibility or architecture contradiction was identified. Part III is the explicit standalone-structure substitute, not a missing-input blocker. All six visual-direction decisions are accepted; no unresolved material VIS-DEC or new VIS-GAP/VIS-CON remains.

Preserve DEFER-001/002 provider/session/finality evidence, DEFER-003 study/tool/step/output conventions, DEFER-004 monetary conventions, DEFER-005 bounded UX defaults, DEFER-006 timing/retry configuration, DEFER-007 technical realization and ADV-VER-001 persistence race verification. They remain prerequisites for their affected work. This artifact chooses no numerical defaults, staleness thresholds, provider behavior, architecture guarantee or storage technology. If a later conflict appears, route structural semantics to the interface-structure owner, interaction semantics to the interaction-flow owner, accessibility capability scope to the interface-requirements owner, and domain/security/resilience changes to architecture; do not solve them by color or hiding information.

## Downstream composition freedom

Wireframe/mockup stages own exact region placement, widths/heights, chart split orientation, disclosure geometry, temporary-surface geometry, field ordering within approved semantic groups and concrete screen compositions. They preserve all UIS view responsibilities, reading/focus/context rules, required co-presence and adaptation. This document does not assign screen coordinates or select new capabilities. Detailed icon artwork remains downstream within the approved icon language.

## Traceability summary

| Visual family | Material upstream authority |
|---|---|
| VIS-PRIN-001/002; VIS-STATE-006–010 | UIR-INFO-001/006/009/013; UIR-CONT-001/003/005; UIS-PAT-001–003 |
| Hierarchy; VIS-PRIN-003/004; VIS-SURF-* | UIS-REG-001–026; UIS-ACT-001–020; UIS-DISC-001–008; UIR-SAFE-001–005 |
| VIS-STATE-001–015 | UIR-STATE-001–014; UIS-STATE-001–064; IF-JRN-001–014 |
| VIS-TYPE-*; VIS-DATA-* | UIR-INFO-003–011/016; UIS-REG-002/012–020/025; IF-JRN-003/005/008–012 |
| VIS-A11Y-*; VIS-ICON-*; VIS-MOTION-* | UIR-A11Y-001–006; UIS-PAT-004; UIS-ADAPT-001–006 |
| Concrete type/color/density/theme values | Accepted VIS-DEC-001–006; derived coherence values within that direction |

## Historical initial quality-gate assessment

| Gate | Result / evidence |
|---|---|
| Source authority / structure readiness | PASS: canonical UI revision 2 Parts I–III; full Part III reviewed; no invented standalone artifact or source approval |
| Semantic/hierarchy/state traceability | PASS for requirements-derived rules: eight views, five hierarchy roles and all 64 state rows mapped above; financial and durability meanings remain separate |
| Human direction checkpoint | PASS: VIS-DEC-001–006 explicitly accepted on 19 October 2026; exact acceptance evidence recorded in every row |
| Typography / palette / density / surfaces / data grammar | PASS: role scales, paired semantic colors, two contextual density tiers, edge/layer hierarchy, redundant series/direction grammar and reusable tokens finalized within the accepted direction |
| Contrast / accessibility | PASS as design: accepted targets translated; normal-text foregrounds checked on base/content/raised surfaces in both themes: minimum 5.91:1; required boundary/data foregrounds: minimum 4.34:1; filled-action text: 6.70:1 light and 9.90:1 dark. These arithmetic checks pass; rendered state/zoom/non-color verification remains necessary for conformance claims |
| Scope and token discipline | PASS: semantic tokens only; no screen geometry, framework, library, code, new brand asset or task capability |
| Assumptions / upstream prerequisites | PASS: no new accepted assumption fabricated; existing deferred evidence retained |
| Readiness | PASS: coherent canonical hierarchy, typography, palette, density, surfaces, states, icons, motion and chart grammar; no material visual choice left for the wireframe designer |

## Historical initial handoff (superseded by revision 6)

Next stage: `ui-screen-designer`, low-fidelity wireframes and G4 review, followed by high-fidelity artifacts/verification and G5. Pass this canonical visual-system.md revision 2, ui-dossier.md revision 2 Parts I–III, upstream requirements/domain/architecture sources and relevant reference evidence. The standalone interface filenames in the skill template are supplied by the canonical UI dossier parts, as that dossier explicitly directs. Both themes, state distinctions, numeric alternatives, scope/target co-presence and accepted adaptation remain binding. Screen geometry remains downstream freedom. G4/G5 are not reached by visual-direction acceptance; existing scoped implementation prerequisites remain outstanding.

### Revision 3 propagation and quality check

The side pattern/legend/overlap rule is a derived data-identity detail under the already approved robust default, paired themes and candle direction grammar (VIS-DEC-003/005/006); no new subjective high-propagation palette/type/theme decision is introduced. UX owns independent calculation-side selection in dossier revision 17. WF-104 supplies a grayscale both-visible composition; applied-color/contrast/readback verification in both themes remains Stage 2D. All r3 mockups predate explicit basis labels and are stale. Source traceability, non-color identity, missing-data wording and unchanged G2/G3 direction pass as specification checks, not rendered color or runtime evidence.

### Revision 4 user-directed override

The user explicitly requests both toggles selected, adjacent Bid/Ask candles, both OHLCV readouts and both volume bars, with filled Bid and hollow Ask candles. This supersedes the former direction-based body fill and dashed Ask proposal. It selects no new financial formula or volume unit. WF-104 realizes the scenario; old high-fidelity samples remain stale and retain their historical fill treatment until Stage 2D.

### Revision 5 — direction shades in wireframes

Explicit user refinement, 21 October 2026: direction must be visible in grayscale wireframes. Bullish/rising Bid candles use light gray filled bodies (#BBBBBB); bearish/falling Bid candles use dark gray filled bodies (#444444). Ask bodies remain hollow: bullish wick/border #777777 and bearish wick/border #222222. Both side-specific volume series follow their corresponding candle shade and retain filled Bid / hollow Ask. These are low-fidelity grayscale equivalents of VIS-DATA-001 direction roles, not a new production palette. Quote side and direction are independent visual dimensions; open/close ticks and numerical OHLC preserve non-shade reading. WF-104 demonstrates all four combinations.

### Revision 6 — explicit high-fidelity user override

**VIS-DEC-007:** User, 21 October 2026: “I want long candles green and short candles red. The full bid candles must have a border of the same candle color but a slightly darker shade. I want all toolbars with a white background.” In the chart grammar, long/short is realized as rising/falling candle direction relative to open/close, not an order-side rule. This supersedes the teal/rose hues of VIS-DEC-006; G4 r11 geometry and quote-side semantics remain authoritative. Both themes retain independently named financial/status tokens even when values coincide.

**VIS-SURF-005 — theme-matching toolbar scope:** top chart controls, left drawing strip, right feature-launch rail, per-chart range/calendar strips, bottom status/action chrome and floating replay capsule use the active theme background: light #FFFFFF, dark #151619. Foreground and neutral borders use the same active theme roles as the workspace: light #1E293B / #D4DAE3; dark #D1D4DC / #2A2B30. This revision supersedes revision 6's white-in-both-themes toolbar instruction. Selection/focus and scoped status marks retain their semantic roles; Buy/Sell follow VIS-COLOR-016/017. Settings and ordinary content share the same neutral palette, with hierarchy conveyed by geometry, text weight and separators.

**VIS-DATA-010 — candle edges:** upward light body #16A34A / edge #15803D; upward dark body #22C55E / edge #16A34A. Downward light body #DC2626 / edge #C91F1F; downward dark body #F87171 / edge #EF4444. Border and wick match; Ask uses the same edge with plot-colored interior. Bid/Ask volume bars retain filled/hollow side identity and matching direction roles. No fill-based direction inference: open-left / close-right ticks and separate numeric OHLCV remain binding. Colors do not change executable bid/ask or calculation basis.

The earlier contrast assessment is historical for revision 2. Revision 6 arithmetic checks must cover actual body/edge versus plot pairs, toolbar text/selection/focus on white, and both themes. This design check is not runtime WCAG conformance. Next: review MP-SET-001-r4 at G5; no G5 approval is implied by this palette request.

Revision 6 observed palette arithmetic (21 October 2026): direction body/edge
contrast against plot: light up 3.30/5.02, down 4.83/5.68; dark up 7.79/5.38,
down 6.41/4.71. All meaningful candle marks exceed 3:1 against their plot.
White-toolbar primary/secondary text 17.85/7.58, boundary 4.76 and blue
selection/focus 6.70 against white. Body-versus-border is a subtle shade cue;
side/direction do not depend on distinguishing those two shades. These are
computed color-pair checks, not rendered WCAG or runtime accessibility passes.

### Revision 7 — exact theme neutrals and trade buttons

**VIS-DEC-008:** Explicit user revision, 21 October 2026: dark toolbars must match the background; dark bg #151619, fg #D1D4DC, borders #2A2B30; light bg #FFFFFF, fg #1E293B, borders #D4DAE3. Base/content/raised and toolbar surfaces share bg; primary/secondary normal text share fg; control/grid separators use borders. This supersedes previous neutral colors and the white-only toolbar override. Existing green/red candles and darker Bid borders remain unchanged.

| ID | Token | Both-theme values | Meaning / non-color cue |
|---|---|---|---|
| VIS-COLOR-016 | color.trade.buy.background / foreground / border | #DCFCE7 / #14532D / #14532D | Buy uses dark green text and boundary over light green; explicit Buy label and selection mark; not application success |
| VIS-COLOR-017 | color.trade.sell.background / foreground / border | #FEE2E2 / #7F1D1D / #7F1D1D | Sell uses dark red text and boundary over light red; explicit Sell label and selection mark; not application failure |

**VIS-STATE-016:** All Buy/Sell controls, including sidebar direction selectors and replay submission controls, use their side-specific palette in both themes. Disabled controls retain aria-disabled and existing blocked reason and gain dashed borders; colors never grant permission or imply execution. Selected direction retains its marker/edge; focus remains independently visible. Other buttons use theme-native neutral surfaces with the existing action/focus grammar.

The specified neutral borders are subtle separators, not a standalone essential state cue or a new accessibility conformance claim. Readable labels, selected markers, focus, disabled reasons and numeric/shape alternatives remain required. Historical contrast observations above apply to their recorded revisions; revision 7 uses the new actual background pairs. No geometry or domain behavior changes, no G5 approval inferred.

Revision 7 computed normal foreground/background contrast: 14.63:1 light,
12.20:1 dark. Buy text/fill 8.30:1; Sell text/fill 8.20:1, identical in both
themes. These arithmetic checks establish readable specified pairs only;
runtime focus, state, zoom and accessibility evidence remains required.
