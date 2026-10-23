import { createChart, customSeriesDefaultOptions, ColorType, LineSeries } from 'lightweight-charts';
import type {
  CustomData,
  CustomSeriesWhitespaceData,
  ICustomSeriesPaneView,
  ICustomSeriesPaneRenderer,
  PaneRendererCustomData,
  PriceToCoordinateConverter,
  UTCTimestamp,
  Time,
  IChartApi,
  ISeriesPrimitive,
  SeriesAttachedParameter,
} from 'lightweight-charts';

// Original strings stay outside chart coordinates. These are synthetic feasibility values.
export interface Quote {
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
}
export interface Bucket {
  instant: string;
  unit: 'ns';
  bid: Quote | null;
  ask: Quote | null;
}
interface PlotQuote {
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
interface QuoteData extends CustomData<UTCTimestamp> {
  source: Bucket;
  bid: PlotQuote | null;
  ask: PlotQuote | null;
}
interface Roles {
  font: string;
  axisTextSize: number;
  surface: string;
  text: string;
  border: string;
  up: string;
  upEdge: string;
  down: string;
  downEdge: string;
  study: string;
}

export function roles(element: HTMLElement): Roles {
  const css = getComputedStyle(element);
  const get = (name: string) => css.getPropertyValue(name).trim();
  return {
    font: get('--font'),
    axisTextSize: Number.parseFloat(get('--axis-text-size')),
    surface: get('--surface'),
    text: get('--text'),
    border: get('--border'),
    up: get('--up'),
    upEdge: get('--up-edge'),
    down: get('--down'),
    downEdge: get('--down-edge'),
    study: get('--study'),
  };
}

export function timeCoordinate(instant: string): UTCTimestamp {
  const ns = BigInt(instant);
  if (ns % 1_000_000_000n !== 0n) throw new Error('Fixture bucket must be an exact UTC second');
  const seconds = ns / 1_000_000_000n;
  if (seconds > BigInt(Number.MAX_SAFE_INTEGER) || seconds < BigInt(Number.MIN_SAFE_INTEGER)) {
    throw new Error('Time outside safe plot range');
  }
  return Number(seconds) as UTCTimestamp;
}

function micros(value: string): bigint {
  if (!/^[0-9]+\.[0-9]{6}$/.test(value)) throw new Error('Fixture requires six-place exact input');
  return BigInt(value.replace('.', ''));
}

export function plotOffset(value: string, anchor: string): number {
  const delta = micros(value) - micros(anchor);
  if (delta > BigInt(Number.MAX_SAFE_INTEGER) || delta < BigInt(Number.MIN_SAFE_INTEGER)) {
    throw new Error('Relative plot value exceeds safe integer range');
  }
  return Number(delta);
}

function project(quote: Quote | null, anchor: string): PlotQuote | null {
  if (!quote) return null;
  const volume = Number(quote.volume);
  if (!Number.isSafeInteger(volume) || volume < 0) throw new Error('Unsafe fixture volume');
  return {
    open: plotOffset(quote.open, anchor),
    high: plotOffset(quote.high, anchor),
    low: plotOffset(quote.low, anchor),
    close: plotOffset(quote.close, anchor),
    volume,
  };
}

type Hit = { instant: string; side: 'bid' | 'ask'; quote: Quote };
type Target = Parameters<ICustomSeriesPaneRenderer['draw']>[0];
interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
  hit: Hit;
}

class PairedView implements ICustomSeriesPaneView<UTCTimestamp, QuoteData> {
  private data: PaneRendererCustomData<UTCTimestamp, QuoteData> | undefined;
  boxes: Box[] = [];
  frames = 0;
  destroyed = false;
  constructor(
    private palette: Roles,
    private volume = false,
  ) {}
  update(data: PaneRendererCustomData<UTCTimestamp, QuoteData>) {
    this.data = data;
  }
  defaultOptions() {
    return { ...customSeriesDefaultOptions, color: this.palette.text };
  }
  isWhitespace(
    data: QuoteData | CustomSeriesWhitespaceData<UTCTimestamp>,
  ): data is CustomSeriesWhitespaceData<UTCTimestamp> {
    return !('source' in data) || (!data.bid && !data.ask);
  }
  priceValueBuilder(row: QuoteData): number[] {
    const sides = [row.bid, row.ask].filter((side) => side !== null);
    if (this.volume) return [0, ...sides.map((side) => side.volume), 0];
    return sides.flatMap((side) => [side.low, side.high, side.close]);
  }
  private draw(target: Target, converter: PriceToCoordinateConverter) {
    const data = this.data;
    this.boxes = [];
    this.frames += 1;
    if (!data?.visibleRange) return;
    const visibleRange = data.visibleRange;
    target.useMediaCoordinateSpace(({ context: ctx }) => {
      // VIS-DATA-009: each true bucket has stable left/right half slots.
      const slot = data.barSpacing * 0.36;
      for (let index = visibleRange.from; index < visibleRange.to; index++) {
        const bar = data.bars[index];
        if (!bar) continue;
        for (const side of ['bid', 'ask'] as const) {
          const quote = bar.originalData[side];
          const original = bar.originalData.source[side];
          if (!quote || !original) continue;
          const x = bar.x + (side === 'bid' ? -slot / 2 : slot / 2);
          const open = converter(this.volume ? 0 : quote.open);
          const close = converter(this.volume ? quote.volume : quote.close);
          const high = converter(quote.high);
          const low = converter(quote.low);
          if (open === null || close === null) continue;
          const up = quote.close >= quote.open;
          ctx.strokeStyle = up ? this.palette.upEdge : this.palette.downEdge;
          ctx.fillStyle =
            side === 'bid' ? (up ? this.palette.up : this.palette.down) : this.palette.surface;
          // One media pixel is fixture line geometry; canvas handles device pixel ratio.
          ctx.lineWidth = 1;
          if (!this.volume && high !== null && low !== null) {
            ctx.beginPath();
            ctx.moveTo(x, high);
            ctx.lineTo(x, low);
            ctx.stroke();
          }
          const width = Math.max(1, slot * 0.8);
          const y = Math.min(open, close);
          const height = Math.max(1, Math.abs(close - open));
          ctx.fillRect(x - width / 2, y, width, height);
          ctx.strokeRect(x - width / 2, y, width, height);
          if (!this.volume) {
            ctx.beginPath();
            ctx.moveTo(x - width, open);
            ctx.lineTo(x - width / 2, open);
            ctx.moveTo(x + width / 2, close);
            ctx.lineTo(x + width, close);
            ctx.stroke();
          }
          this.boxes.push({
            x: x - width / 2,
            y,
            width,
            height,
            hit: { instant: bar.originalData.source.instant, side, quote: original },
          });
        }
      }
    });
  }
  renderer(): ICustomSeriesPaneRenderer {
    return {
      draw: (target, converter) => this.draw(target, converter),
      hitTest: (x, y) => {
        const box = this.boxes.find(
          (box) => x >= box.x && x <= box.x + box.width && y >= box.y && y <= box.y + box.height,
        );
        return box
          ? {
              distance: 0,
              objectId: `${box.hit.instant}:${box.hit.side}`,
              type: 'custom',
              hitTestData: box.hit,
            }
          : null;
      },
    };
  }
  destroy() {
    this.destroyed = true;
    this.boxes = [];
    this.data = undefined;
  }
}

class AnchorPrimitive implements ISeriesPrimitive<Time> {
  visible = false;
  private attachedTo: SeriesAttachedParameter<Time> | undefined;
  constructor(
    private time: UTCTimestamp,
    private price: number,
    private color: string,
  ) {}
  attached(parameter: SeriesAttachedParameter<Time>) {
    this.attachedTo = parameter;
  }
  detached() {
    this.attachedTo = undefined;
  }
  paneViews() {
    return [
      {
        renderer: () => ({
          draw: (target: Target) => {
            this.visible = false;
            const parameter = this.attachedTo;
            if (!parameter) return;
            const x = parameter.chart.timeScale().timeToCoordinate(this.time);
            const y = parameter.series.priceToCoordinate(this.price);
            if (x === null || y === null) return;
            target.useMediaCoordinateSpace(({ context, mediaSize }) => {
              this.visible = x >= 0 && x < mediaSize.width && y >= 0 && y < mediaSize.height;
              context.strokeStyle = this.color;
              context.beginPath();
              context.moveTo(x - 4, y - 4);
              context.lineTo(x + 4, y + 4);
              context.stroke();
            });
          },
        }),
      },
    ];
  }
}

export interface Probe {
  chart: IChartApi;
  navigate(from: number, to: number): void;
  selected(): string | undefined;
  renderedFrames(): number;
  visibleDrawings(): number;
  boxes(): readonly Box[];
  update(bucket: Bucket): void;
  inspect(instant: string, side: 'bid' | 'ask'): Quote | null;
  resize(width: number, height: number): void;
  exportImage(): string;
  dispose(): boolean;
}

export function createProbe(element: HTMLElement, buckets: Bucket[], anchor: string): Probe {
  const palette = roles(element);
  const chart = createChart(element, {
    width: element.clientWidth,
    height: element.clientHeight,
    layout: {
      fontFamily: palette.font,
      fontSize: palette.axisTextSize,
      background: { type: ColorType.Solid, color: palette.surface },
      textColor: palette.text,
      attributionLogo: false,
    },
    grid: { vertLines: { color: palette.border }, horzLines: { color: palette.border } },
    rightPriceScale: { borderColor: palette.border },
    timeScale: { borderColor: palette.border },
  });
  const candles = new PairedView(palette);
  const volumes = new PairedView(palette, true);
  const series = chart.addCustomSeries(candles, {
    priceLineVisible: false,
    lastValueVisible: false,
  });
  const volume = chart.addCustomSeries(
    volumes,
    { priceLineVisible: false, lastValueVisible: false },
    1,
  );
  const mapped = (source: Bucket): QuoteData => ({
    time: timeCoordinate(source.instant),
    source,
    bid: project(source.bid, anchor),
    ask: project(source.ask, anchor),
  });
  // Retain the complete 100k resident set per chart, while paging only visible geometry
  // into the vendor buffers. All windows remain accessible by their original UTC buckets.
  const original = new Map(buckets.map((bucket) => [bucket.instant, bucket]));
  const studies = [2, 3].map((pane) =>
    chart.addSeries(
      LineSeries,
      { color: palette.study, priceLineVisible: false, lastValueVisible: false },
      pane,
    ),
  );
  let pageStart = Math.max(0, buckets.length - 500);
  let rows = buckets.slice(pageStart).map(mapped);
  function setRows() {
    series.setData(rows);
    volume.setData(rows);
    const values = rows
      .filter((row) => row.bid || row.ask)
      .map((row) => ({ time: row.time, value: (row.bid ?? row.ask)?.close ?? 0 }));
    studies.forEach((line) => line.setData(values));
  }
  setRows();
  function navigate(from: number, to: number) {
    if (from < 0 || to > buckets.length || from >= to) throw new Error('Invalid fixture window');
    if (from < pageStart || to > pageStart + rows.length) {
      pageStart = Math.max(0, from - 200);
      rows = buckets.slice(pageStart, Math.min(buckets.length, to + 200)).map(mapped);
      setRows();
    }
    chart.timeScale().setVisibleLogicalRange({ from: from - pageStart, to: to - pageStart });
  }
  let selection: string | undefined;
  chart.subscribeCrosshairMove((event) => {
    const id = event.hoveredInfo?.objectId;
    selection = typeof id === 'string' ? id : undefined;
  });
  const primitives: AnchorPrimitive[] = [];
  for (let index = 0; index < 50; index++) {
    const row = rows[rows.length - 1 - index];
    if (!row) continue;
    const primitive = new AnchorPrimitive(row.time, row.bid?.close ?? 0, palette.study);
    series.attachPrimitive(primitive);
    primitives.push(primitive);
  }
  chart
    .timeScale()
    .setVisibleLogicalRange({ from: Math.max(0, rows.length - 100), to: rows.length });
  return {
    chart,
    navigate,
    selected: () => selection,
    renderedFrames: () => candles.frames,
    visibleDrawings: () => primitives.filter((primitive) => primitive.visible).length,
    boxes: () => candles.boxes,
    update: (bucket) => {
      const index = buckets.findIndex((item) => item.instant === bucket.instant);
      if (index < 0) buckets.push(bucket);
      else buckets[index] = bucket;
      original.set(bucket.instant, bucket);
      if (pageStart + rows.length >= buckets.length - 1) {
        const row = mapped(bucket);
        series.update(row);
        volume.update(row);
        if (index < 0) rows.push(row);
      }
    },
    inspect: (instant, side) => original.get(instant)?.[side] ?? null,
    resize: (width, height) => chart.resize(width, height),
    exportImage: () => chart.takeScreenshot().toDataURL('image/png'),
    dispose: () => {
      primitives.forEach((primitive) => series.detachPrimitive(primitive));
      chart.removeSeries(series);
      chart.removeSeries(volume);
      studies.forEach((line) => chart.removeSeries(line));
      chart.remove();
      // Release adapter buffers explicitly; chart-wide teardown is not a plugin callback contract.
      candles.destroy();
      volumes.destroy();
      return candles.destroyed && volumes.destroyed;
    },
  };
}
