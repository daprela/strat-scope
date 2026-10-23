# UI Implementation Standards (frontend/)

- **Status:** `ACTIVE`; version 1, approved at Gate G6 on 22/10/2026.
- **Scope Root:** frontend/; all future UI components, chart adapters, local styles, fixtures and UI verification support.
- **Governing Authorities:** [architecture-dossier.md](../analysis/tradingview/architecture-dossier.md), [ui-dossier.md](../analysis/tradingview/ui-dossier.md) revision 28, [visual-system.md](../analysis/tradingview/visual-system.md) revision 7 and [implementation-standards.md](../analysis/tradingview/implementation-standards.md) revision 3.
- **Approval:** G6-DEC-003/004/007/009/010. UI_DERIVED and IMPLEMENTATION_DERIVED retain source provenance; APPROVED_PROPOSAL identifies UIS-DEC-001/002 accepted by the user. UI visuals remain G4 r13 / G5 r7; standards activation does not revise them.
- **Coding profile:** Follow [DEVELOPMENT.md](DEVELOPMENT.md) for TSX/HTML/CSS conventions. No nested component-specific guides are required.

## Mandatory UI Realization Rules

Each row is mandatory within its applicable implemented scope. Keep the same rule identity and source traceability when standards evolve. A rule referring to a blocked feature does not authorize that feature's implementation.

| Rule | Classification / sources | Operational requirement and verification |
|---|---|---|
| UIS-REAL-001 | UI_DERIVED: UI-IMPL-002/016; UIS-PAT-006–013; UIV-STRUCT-001 | Preserve central chart, left drawing strip, top controls, right rail/drawers, scoped docks, range/calendar strip and floating Settings/Go to/replay capsule. Side panels start below the top toolbar and end above status chrome; bodies scroll inside those bounds. Future bundle launcher stays disabled. Verify all implemented view/state compositions against approved UI-ART entries. |
| UIS-REAL-002 | IMPLEMENTATION_DERIVED: IS-UI-001/002; UI-FREEDOM-001/004 | Shared controls own semantics, focus and styling; feature-local composition owns task assembly. Renderer only maps coordinates/presentation, not domain decisions. Reuse shared state/error/target presentations without merging independent conditions into one global status. |
| UIS-REAL-003 | UI_DERIVED: UI-IMPL-007/012/014; VIS-TOKEN-001–008, VIS revision 7 overrides | Consume semantic typography, colors, spacing, density, edge and motion roles. Exact light/dark neutrals, green/red candles/darker Bid edges and Buy/Sell palette follow the latest canonical values. Distinct financial/action/status/focus roles remain distinct tokens even when values coincide. UIV-VIS-001/002 compare actual roles in both themes. |
| UIS-REAL-004 | APPROVED_PROPOSAL: UIS-DEC-001; IS-UI-001; user-selected IS-UI-002 | Central CSS custom-property definitions map canonical VIS IDs to runtime role names; Lightweight Charts options/custom series/primitives and any SVG overlays read the same resolved roles. Raw color/spacing/type/radius/motion design literals are prohibited outside that map. Approved layout/financial geometry, dimensionless calculations, DPR scaling, zero and structural 100% are not substitute visual tokens; document their source. CSS Modules encapsulate selectors; no global feature overrides or new component-theme framework. |
| UIS-REAL-005 | UI_DERIVED: UI-IMPL-003/004; UIV-STATE-001–003; UIS-STATE-001–064 | Render loading, empty/absent, invalid, warm-up, error, stale, UNCERTAIN, conflict and restricted states from explicit contextual outcomes. Preserve correctly labelled prior views. Separate accepted waiting, triggered, whole execution, working version and acknowledged retained version. No fabricated zero, optimistic fill or false save success. |
| UIS-REAL-006 | UI_DERIVED: UI-IMPL-004/006; WF-ANN; UID-002/004/005 | Pending submission 027 retains original run/request/boundary/terms and a blocking reason; evaluation 092 is distinct. Failed save 015 uses error cues and retention-only retry; unknown publication 077 uses uncertainty and blocks progression/mutation pending reconciliation, unlike resolved 037. Test compound states rather than one flag at a time. |
| UIS-REAL-007 | UI_DERIVED: IF-JRN-002/007–010; UIR-ERR-001; UI-IMPL-005/006 | Keep draft and committed values separate. Validate using declared field/commit rules, associate errors with named fields and focus the relevant invalid context. Invalid edits preserve previous valid terms; superseded estimates are non-actionable. Exact target/version/remainder/units/risk and consequence remain co-present with actions. No unapproved opposite-side behavior or numerical bounds; UIADV-INT-002 and DEFER-003/004 gate affected work. |
| UIS-REAL-008 | UI_DERIVED: IF-CONF-001–003; UI-IMPL-005/008; IF-A11Y | Confirm destructive operation-specific scope, destination/replacement/discarded suffix and drawings independence; cancel preserves work. Changed versions require renewed review. A floating surface is not automatically modal: trap focus only for the approved modal interaction, restore invoke/surviving-context focus, and retain keyboard access to nonmodal task surfaces. No new confirmation step. |
| UIS-REAL-009 | UI_DERIVED: UIR-A11Y-001–006; VIS-A11Y-001–005; UIV-A11Y-001–003 | Use semantic HTML before ARIA, names and pressed/selected/disabled semantics with actual matching activation guards. Keep blocked reasons discoverable, focus independently visible, primary tasks keyboard-completable and drawings editable through numeric financial anchors/brush points. Verify both themes, non-color cues, actual contrast and reduced motion; optional animation cannot change replay order or processing. |
| UIS-REAL-010 | UI_DERIVED: UI-IMPL-009/016; UIS-ADAPT-001–006; UIV-ADAPT-001 | Preserve target/terms/reasons/actions at 1280×800 CSS baseline and enlargement/reflow. Panel bodies scroll while actions remain reachable. Do not shrink critical text to reproduce an SVG or infer a mandatory 640px/mobile breakpoint. Test zoom, two charts, long names/errors and the approved dock variants. |
| UIS-REAL-011 | UI_DERIVED: UI-IMPL-013/014; VIS-DATA-001–010; UIV-INT-003/DATA-003/VIS-002 | Independent Bid/Ask visibility does not select calculation basis, executable side or replay cursor. Both visible uses filled Bid-left / hollow Ask-right candles and side-specific volumes in one real bucket; both hidden preserves axes/drawings/named calculation context. Separate labelled OHLCV/absence reasons and direction ticks/numerics remain. |
| UIS-REAL-012 | UI_DERIVED: UI-IMPL-010/011/015; UIV-CONT-001/ACC-001/JRN-015 | Pin export source, retain boundary/units/assumptions/absence labels, reconcile unknown output, and exclude secrets/private evidence. Implement Data location only after its architecture contract; saved-run originals never silently follow a folder edit. |
| UIS-REAL-013 | APPROVED_PROPOSAL: UIS-DEC-002; IMPLEMENTATION_DERIVED IS-QA-001; UI-IMPL-011 | Prefer role/name semantic selectors; add stable data-testid only for otherwise ambiguous chart/layer targets. Fixture manifests identify relevant UI-ART, UIV and context versions; control async barriers without arbitrary sleeps. Collect runtime evidence for the implemented subset across both themes and material states. Do not conflate static artifact checks, pixel similarity, keyboard proof, financial truth, durability or P3. |

## Chart Adapter, Data and Lifecycle

IS-UI-002 requires the locally bundled `lightweight-charts` package and its documented 5.2.x API line, with an exact compatible released pin at bootstrap. Use native TypeScript APIs rather than an unselected wrapper/fork. The adapter owns chart instances, subscriptions, coordinate mapping, custom series/primitives and disposal; application semantics and saved drawing anchors remain outside library handles. Follow the canonical standards' presentation section for attribution, lossless time mapping and export composition.

Use custom series where necessary for filled Bid-left / hollow Ask-right candles and their independent volumes within the same true UTC bucket. Two normal series sharing timestamps are not proof of adjacent geometry. Verify autoscale, side/bucket hit testing, crosshair/readouts and absence cases. Default library colors/options cannot replace VIS roles. Plot values are already bounded to the common replay context; never feed future facts to legend/autoscale. Preserve original precision outside the renderer and prevent chart callbacks from advancing or executing replay.

Library canvas interactions do not establish keyboard or screen-reader completion. Provide the approved named controls, bar inspection and numeric/financial-anchor drawing alternatives. Export checks must include the intended custom and separately overlaid layers plus pinned source labels. A library screenshot alone does not prove complete export.

(Source: IMPLEMENTATION_DERIVED IS-UI-002; UI_DERIVED UI-IMPL-003/008/010/013/014, UIV-DATA-003 and UIV-A11Y-001–003.)

## Forms, Confirmations and Focus

Apply the approved validation triggers and association rules from the governing journey; do not invent domain parameter limits or a new universal confirmation. Destructive reviews keep exact scope/version/consequence and cancel/confirm co-present. Modal focus containment applies only where the approved interaction is modal; nonmodal drawers and the replay capsule keep their surrounding task access. Restore focus to the invoker or surviving context. Supplementary [WAI modal-dialog APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) guidance (accessed 21/10/2026) cannot override that distinction.

(Source: UI_DERIVED IF-CONF-001–003, IF-A11Y and UI-IMPL-005/008; UIS-REAL-007/008.)

## Scoped Prerequisites and Verification

UIADV-INT-002 remains with ux-architecture-designer DELTA: opposite-side activation, direction-specific draft/estimate validity, readback and commitment need upstream resolution before affected entry work. UISYN-MOD-004 / UI-IMPL-015 require architecture-owned Data location preference/validation/publication/catalog-adoption semantics. DEFER-001–007 and ADV-VER-001 apply to affected work; fixture values never settle them.

Link each implemented view/state/journey to relevant UI-ART/UID/UIV identities and actual evidence under UIV-EVID-001–009. Exercise material compound states, both themes, enlargement/reflow, reduced motion, two-chart context and allowed/denied authority. Distinguish structural/pixel checks from keyboard interaction, runtime accessibility, domain arithmetic, durability and recorded-hardware P3 results. Source/approval hashes do not prove behavior.

(Source: UI_DERIVED UI-IMPL-001/011/015, UID-001–008 and UIV-EVID-001–009; IMPLEMENTATION_DERIVED IS-QA-001.)

## Approved Deviations

None. UIS-DEC-001/002 are approved engineering standards, not deviations from approved UX or VIS rules. Any behavior/token/geometry conflict returns to its owning upstream authority before affected implementation.
