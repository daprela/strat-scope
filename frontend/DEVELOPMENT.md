# Development Standards (frontend/)

- **Status:** `ACTIVE`; version 1, approved at Gate G6 on 22/10/2026.
- **Last Reviewed:** 22/10/2026.
- **Scope Root & Governed Paths:** frontend/, including future TypeScript/TSX, authored HTML, CSS Modules, build configuration and tests.
- **Separately Governed Nested Scopes:** None. Generated transport declarations, build output and caches are not manually maintained source.
- **Authority:** [implementation-standards.md](../analysis/tradingview/implementation-standards.md), revision 3; [UI-DEVELOPMENT.md](UI-DEVELOPMENT.md); G6-DEC-002/003/004/006/007/009/010.
- **Readiness:** Governance is active; application manifests, dependencies and commands await foundation bootstrap under an implementation brief.

## Language Standards Summary

| Language | Version / context | Adopted primary profile | Maintaining authority / edition | Enforcement alignment |
|---|---|---|---|---|
| TypeScript / TSX | TS 6.x, React 19.x | Google TypeScript Style Guide | Google, living guide accessed 21/10/2026 | tsc strict, ESLint/typescript-eslint/React hooks, Prettier |
| HTML | Semantic authored HTML / JSX in approved modern desktop browser baseline | Google HTML/CSS Style Guide | Google, living guide accessed 21/10/2026 | Prettier plus semantic/component/browser checks |
| CSS | CSS Modules and custom properties | Google HTML/CSS Style Guide | Google, living guide accessed 21/10/2026 | Prettier and UI token/visual checks |

## TypeScript and TSX Operational Rules

Primary source: [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html), accessed 21/10/2026. Supplementary official guidance: [React TypeScript](https://react.dev/learn/typescript), [TypeScript strict](https://www.typescriptlang.org/tsconfig/strict) and [indexed access](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html), from the same research round.

Use ES modules, named exports, camelCase values/functions and PascalCase types/components. Prefer type-only imports for type dependencies. Untrusted data starts as unknown and must be narrowed/decoded before use. Avoid any, non-null assertions and broad lint suppression. Use explicit variants for meaningful outcomes and preserve semantic identity/units separately from display strings and renderer handles.

React function components, hooks and JSX are approved profile adaptations. Follow hooks rules; effects subscribe and clean up for the current context rather than duplicate canonical state. Use hooks/reducers/context for local shell state. The service owns run/catalog/calculation/durability truth; render callbacks cannot compute authoritative fees/fills, advance replay or declare saved success. Generation checks discard stale views.

Use TradingView Lightweight Charts through one adapter, targeting the approved 5.2.x API line with an exact released pin at bootstrap. Keep its types/instances out of core contracts and saved drawing values. Dispose chart instances/subscriptions and resize existing instances correctly. Custom series/primitives, timestamp mapping, paired Bid/Ask geometry, numeric alternatives and attribution follow IS-UI-002 and UI-DEVELOPMENT.md. No React wrapper package, vendor fork or substitute chart engine is approved.

Comments explain contracts, units and context invariants. Map explicit semantic errors to readable contextual outcomes; do not turn missing values into zero or uncertainty into known failure. Generated OpenAPI transport types are regenerated from their canonical schema, not edited manually; declarations do not validate incoming runtime data. Keep capability/provider secrets outside persistent browser storage, URLs, diagnostics and build variables.

Tests describe observable outcomes with independent expected values. Prefer accessible role/name queries, stable exceptional chart selectors and controlled async barriers. Component tests cover local behavior; browser tests cover wiring, focus, keyboard/reflow and material visual states. Do not duplicate financial arithmetic in E2E tests or infer physical durability from screenshots.

## HTML and CSS Operational Rules

Primary source for each language: [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html), accessed 21/10/2026. The approved adaptations are explicit HTML closing tags, React className/JSX syntax, CSS Module local naming and canonical VIS tokens; Prettier controls mechanical layout.

Use semantic elements, valid nesting, named controls, explicit field labels and safe text insertion. Associate errors and reasons with their controls. Preserve actual disabled/pressed/selected behavior, visible independent focus and keyboard equivalents. Never insert captured target markup as live UI.

Use CSS Modules for local selectors and central semantic CSS custom properties for design roles. Color/spacing/type/radius/motion literals belong only in the canonical token map; approved layout/financial geometry, zero, structural percentages, dimensionless calculations and DPR scaling are documented exceptions. Lightweight Charts options/custom drawing code consume the same resolved semantic roles. No global feature selector overrides or additional component-theme framework is selected.

## Approved Formatting, Tools and Continuity

Prettier profile: two spaces, 100-column target, single quotes and semicolons. Enable TypeScript strict, noUncheckedIndexedAccess and exactOptionalPropertyTypes; use ESLint with typescript-eslint and React hooks rules. These conventions apply within frontend/ and explicitly supplement the root's dossier Python guidance.

Use Node 24.x and one npm package/lockfile; Vite 8 builds local assets. Record exact compatible versions in foundation evidence. Required commands after the foundation defines their scripts, run within frontend/:

```bash
npm ci
npm run typecheck
npm run lint
npm run format:check
npm run test -- --run
npm run build
npm run test:e2e
```

Vitest/Testing Library serve local behavior and Playwright Chromium serves selective browser journeys. Record browser versions and actual evidence limits. Runtime assets remain local. Apply these standards to touched code within the active brief; do not reformat generated artifacts, install speculative libraries or expand the implementation scope.
