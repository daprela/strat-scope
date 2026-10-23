import { createProbe } from '../../src/chart/adapter';
import type { Bucket, Probe } from '../../src/chart/adapter';
import styles from '../../src/Foundation.module.css';
import '../../src/tokens.css';

const anchor = '12345678901234567890.000000';
function price(value: number) {
  return `12345678901234567890.${String(value).padStart(6, '0')}`;
}
function bucket(index: number): Bucket {
  const open = 1000 + (index % 100);
  return {
    instant: String((1700000000n + BigInt(index) * 60n) * 1000000000n),
    unit: 'ns',
    bid: {
      open: price(open),
      high: price(open + 12),
      low: price(open - 8),
      close: price(open + (index % 2 === 0 ? 6 : -4)),
      volume: '123',
    },
    ask: {
      open: price(open + 3),
      high: price(open + 18),
      low: price(open - 6),
      close: price(open + (index % 2 === 0 ? 9 : -2)),
      volume: '237',
    },
  };
}
const paint = () =>
  new Promise<void>((resolve) =>
    requestAnimationFrame(() => requestAnimationFrame(() => resolve())),
  );

// Native invalidation queues its rAF before this fence. Frame counters prove the
// custom canvases were drawn; there is no extra idle display frame in the latency.
const rendered = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));

export interface Harness {
  probes: Probe[];
  initialMs: number;
  interactions(): Promise<number[]>;
  receipt(): Promise<number>;
  absence(): Promise<boolean>;
  dispose(): boolean;
}
declare global {
  interface Window {
    foundationProbe: Harness | undefined;
  }
}

async function main() {
  const root = document.getElementById('probe');
  if (!root) throw new Error('Missing fixture root');
  document.documentElement.dataset.theme =
    new URLSearchParams(location.search).get('theme') ?? 'light';
  root.className = styles.charts ?? '';
  const start = performance.now();
  const data = Array.from({ length: 100000 }, (_, index) => bucket(index));
  const probes = Array.from({ length: 2 }, () => {
    const element = document.createElement('div');
    element.className = styles.chart ?? '';
    root.append(element);
    return createProbe(element, [...data], anchor);
  });
  await paint();
  const initialMs = performance.now() - start;
  window.foundationProbe = {
    probes,
    initialMs,
    interactions: async () => {
      const samples: number[] = [];
      for (let index = 0; index < 60; index++) {
        const before = probes.map((probe) => probe.renderedFrames());
        const start = performance.now();
        probes.forEach((probe) => probe.navigate(99900 + (index % 30), 100000));
        await rendered();
        if (probes.some((probe, index) => probe.renderedFrames() <= (before[index] ?? -1))) {
          throw new Error('Interaction did not complete a canvas draw');
        }
        samples.push(performance.now() - start);
      }
      return samples;
    },
    receipt: async () => {
      probes.forEach((probe) => probe.navigate(99900, 100000));
      await rendered();
      const received = performance.now();
      const latest = bucket(100000);
      probes.forEach((probe) => {
        probe.update(latest);
        probe.navigate(99901, 100001);
      });
      await rendered();
      if (
        !probes.every((probe) => probe.boxes().some((box) => box.hit.instant === latest.instant))
      ) {
        throw new Error('Received bucket was not drawn');
      }
      return performance.now() - received;
    },
    absence: async () => {
      const missing = { ...bucket(100001), bid: null };
      probes.forEach((probe) => {
        probe.update(missing);
        probe.navigate(99960, 100002);
      });
      await paint();
      return probes.every(
        (probe) =>
          probe.inspect(missing.instant, 'bid') === null &&
          probe.inspect(missing.instant, 'ask')?.volume === '237',
      );
    },
    dispose: () => probes.every((probe) => probe.dispose()),
  };
}
void main();
