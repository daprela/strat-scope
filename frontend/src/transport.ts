import type { components } from './generated/api';

export type Capability = components['schemas']['Capability'];
export type Update = components['schemas']['UpdateEnvelope'];
export type ExactObservation = components['schemas']['ExactObservation'];

function object(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Invalid transport object');
  }
  return value as Record<string, unknown>;
}

function keys(value: Record<string, unknown>, expected: string[]) {
  if (Object.keys(value).length !== expected.length || expected.some((key) => !(key in value))) {
    throw new Error('Unexpected transport fields');
  }
}

export function decodeCapability(value: unknown): Capability {
  const row = object(value);
  keys(row, ['token', 'epoch', 'purpose', 'expires_in_seconds']);
  if (
    typeof row.token !== 'string' ||
    typeof row.epoch !== 'string' ||
    row.purpose !== 'foundation-status' ||
    row.expires_in_seconds !== 300
  ) {
    throw new Error('Invalid capability');
  }
  return {
    token: row.token,
    epoch: row.epoch,
    purpose: row.purpose,
    expires_in_seconds: row.expires_in_seconds,
  };
}

export function decodeUpdate(value: unknown, epoch: string): Update {
  const row = object(value);
  keys(row, ['kind', 'epoch', 'status', 'business_features']);
  if (
    row.kind !== 'foundation-status' ||
    row.epoch !== epoch ||
    row.status !== 'infrastructure-ready' ||
    row.business_features !== 'not-implemented'
  ) {
    throw new Error('Invalid or obsolete update');
  }
  return { kind: row.kind, epoch, status: row.status, business_features: row.business_features };
}

export function decodeExact(value: unknown): ExactObservation {
  const row = object(value);
  keys(row, ['instant', 'unit', 'occurrence', 'value']);
  if (
    typeof row.instant !== 'string' ||
    row.instant.length > 40 ||
    !/^-?(0|[1-9][0-9]*)$/.test(row.instant) ||
    typeof row.occurrence !== 'string' ||
    row.occurrence.length > 40 ||
    !/^-?(0|[1-9][0-9]*)$/.test(row.occurrence) ||
    typeof row.value !== 'string' ||
    row.value.length > 100 ||
    !/^-?(0|[1-9][0-9]*)(\.[0-9]+)?$/.test(row.value) ||
    (row.unit !== 'ns' && row.unit !== 'ms')
  ) {
    throw new Error('Invalid exact representation');
  }
  return { instant: row.instant, unit: row.unit, occurrence: row.occurrence, value: row.value };
}

export async function connectStatus(onUpdate: (update: Update) => void): Promise<() => void> {
  const response = await fetch('/api/bootstrap', {
    method: 'POST',
    headers: { 'X-Foundation-Bootstrap': '1' },
  });
  if (!response.ok)
    throw new Error('Foundation authority unavailable; restart the service to reclaim');
  const capability = decodeCapability(await response.json());
  const status = await fetch('/api/status', {
    headers: {
      Authorization: `Bearer ${capability.token}`,
      'X-Owner-Epoch': capability.epoch,
      'X-Capability-Purpose': capability.purpose,
    },
  });
  if (!status.ok) throw new Error('Foundation status denied');
  onUpdate(decodeUpdate(await status.json(), capability.epoch));
  const socket = new WebSocket(`${location.origin.replace('https:', 'wss:')}/api/updates`);
  socket.onopen = () =>
    socket.send(
      JSON.stringify({
        token: capability.token,
        epoch: capability.epoch,
        purpose: capability.purpose,
      }),
    );
  socket.onmessage = (event: MessageEvent<string>) => {
    try {
      onUpdate(decodeUpdate(JSON.parse(event.data), capability.epoch));
    } catch {
      socket.close();
    }
  };
  return () => socket.close();
}
