import { test, expect } from '@playwright/test';
import type { Harness } from './probe';
import { writeFile } from 'node:fs/promises';
import { cpus, totalmem, platform } from 'node:os';

const browserId = process.env.STRAT_SCOPE_BROWSER_ID ?? 'chromium';
if (!/^[a-z0-9-]+$/i.test(browserId)) throw new Error('Invalid STRAT_SCOPE_BROWSER_ID');
const evidence = (name: string) =>
  `../foundation-evidence/${browserId === 'chromium' ? name : `${browserId}-${name}`}`;

declare global {
  interface Window {
    foundationProbe: Harness | undefined;
  }
}

test('HTTPS local assets, capability isolation and secure WS', async ({ page, context }) => {
  const requests: string[] = [];
  const failures: string[] = [];
  page.on('request', (request) => requests.push(request.url()));
  page.on('pageerror', (error) => failures.push(error.message));
  const wsMessage = page
    .waitForEvent('websocket')
    .then((socket) => socket.waitForEvent('framereceived'));
  await page.goto('https://127.0.0.1:4111');
  await expect(page.getByRole('status')).toHaveText('Infrastructure ready');
  const frame = await wsMessage;
  expect(String(frame.payload)).toContain('not-implemented');
  expect(await page.evaluate(() => window.isSecureContext)).toBe(true);
  expect(requests.every((url) => url.startsWith('https://127.0.0.1:4111/'))).toBe(true);
  expect(failures).toEqual([]);
  expect(
    await page.evaluate(() => ({ local: localStorage.length, session: sessionStorage.length })),
  ).toEqual({ local: 0, session: 0 });
  const second = await context.newPage();
  await second.goto('https://127.0.0.1:4111');
  await expect(second.getByRole('status')).toContainText('Authority unavailable');
  const foreign = await context.newPage();
  await foreign.goto('http://127.0.0.1:4112/tests/browser/probe.html');
  expect(
    await foreign.evaluate(async () => {
      try {
        const response = await fetch('https://127.0.0.1:4111/api/bootstrap', {
          method: 'POST',
          headers: { 'X-Foundation-Bootstrap': '1' },
        });
        return response.ok;
      } catch {
        return false;
      }
    }),
  ).toBe(false);
  await page.screenshot({ path: evidence('https-entry.png') });
});

for (const theme of ['light', 'dark']) {
  test(`native paired renderer, lifecycle and P3 fixture (${theme})`, async ({ page, browser }) => {
    const errors: string[] = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(`http://127.0.0.1:4112/tests/browser/probe.html?theme=${theme}`);
    await page.waitForFunction(() => window.foundationProbe !== undefined);
    const target = await page.evaluate(() => {
      const box = window.foundationProbe?.probes[0]
        ?.boxes()
        .find(
          (box) =>
            box.hit.side === 'bid' && box.x > 80 && box.x < 300 && box.y > 20 && box.height > 3,
        );
      const rect = document.querySelector('#probe > div')?.getBoundingClientRect();
      if (!box || !rect) throw new Error('No visible native hit-test target');
      return {
        x: rect.left + box.x + box.width / 2,
        y: rect.top + box.y + box.height / 2,
        id: `${box.hit.instant}:bid`,
      };
    });
    await page.mouse.move(target.x, target.y);
    await expect
      .poll(() => page.evaluate(() => window.foundationProbe?.probes[0]?.selected()))
      .toBe(target.id);
    const result = await page.evaluate(async () => {
      const harness = window.foundationProbe;
      if (!harness) throw new Error('Missing probe');
      const boxes = harness.probes[0]?.boxes() ?? [];
      const bid = boxes.find((box) => box.hit.side === 'bid');
      const ask = boxes.find(
        (box) => box.hit.instant === bid?.hit.instant && box.hit.side === 'ask',
      );
      const image = harness.probes[0]?.exportImage();
      const visibleDrawings = harness.probes.reduce(
        (count, probe) => count + probe.visibleDrawings(),
        0,
      );
      const samples = await harness.interactions();
      samples.sort((a, b) => a - b);
      const receiptMs = await harness.receipt();
      const absence = await harness.absence();
      harness.probes.forEach((probe) => probe.resize(640, 600));
      return {
        initialMs: harness.initialMs,
        nativeHover: true,
        visibleDrawings,
        exportPng: image,
        interactionP95: samples[Math.ceil(samples.length * 0.95) - 1],
        receiptMs,
        absence,
        paired: bid !== undefined && ask !== undefined && bid.x < ask.x,
        originalPrice: bid?.hit.quote.open,
        sameBucket: bid?.hit.instant === ask?.hit.instant,
        panes: harness.probes.map((probe) => probe.chart.panes().length),
        exportPresent: image?.startsWith('data:image/png;base64,') && image.length > 10000,
      };
    });
    const { exportPng, ...metrics } = result;
    if (!exportPng) throw new Error('Missing native export');
    await writeFile(
      evidence(`renderer-export-${theme}.png`),
      Buffer.from(exportPng.slice(exportPng.indexOf(',') + 1), 'base64'),
    );
    await writeFile(
      evidence(`renderer-${theme}.json`),
      JSON.stringify(
        {
          ...metrics,
          browser: browserId,
          browserVersion: browser.version(),
          cpu: cpus()[0]?.model,
          logicalCpus: cpus().length,
          memoryBytes: totalmem(),
          platform: platform(),
          viewport: { width: 1600, height: 1000 },
          fixture: {
            charts: 2,
            residentBarsPerChart: 100000,
            studyPanesTotal: 4,
            drawingPrimitives: 100,
          },
          limitations:
            'Synthetic renderer-only fixture; no provider, financial or product UI acceptance',
        },
        null,
        2,
      ) + '\n',
    );
    await page.screenshot({ path: evidence(`renderer-${theme}.png`) });
    expect(errors).toEqual([]);
    expect(result.paired && result.sameBucket && result.absence && result.exportPresent).toBe(true);
    expect(result.panes).toEqual([4, 4]);
    expect(result.visibleDrawings).toBe(100);
    expect(result.originalPrice).toMatch(/^12345678901234567890\./);
    expect(result.initialMs).toBeLessThan(2000);
    expect(result.interactionP95).toBeLessThan(50);
    expect(result.receiptMs).toBeLessThan(1000);
    expect(await page.evaluate(() => window.foundationProbe?.dispose())).toBe(true);
    await expect(page.locator('canvas')).toHaveCount(0);
  });
}
