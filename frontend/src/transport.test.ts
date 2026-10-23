import { describe, expect, it } from 'vitest';
import { decodeExact, decodeUpdate } from './transport';
import { plotOffset, timeCoordinate } from './chart/adapter';

describe('exact adapter boundaries', () => {
  it('retains exact strings and rejects unsafe wire numbers and stale epochs', () => {
    const original = {
      instant: '9007199254740993',
      unit: 'ns',
      occurrence: '18446744073709551616',
      value: '12345678901234567890.000000000000000001',
    };
    expect(decodeExact(original)).toEqual(original);
    expect(() => decodeExact({ ...original, instant: Number('9007199254740993') })).toThrow();
    expect(() => decodeExact({ ...original, value: 'NaN' })).toThrow();
    expect(() =>
      decodeUpdate(
        {
          kind: 'foundation-status',
          epoch: 'old',
          status: 'infrastructure-ready',
          business_features: 'not-implemented',
        },
        'new',
      ),
    ).toThrow();
  });
  it('maps relative coordinates without rounding original prices or shifting time', () => {
    expect(plotOffset('12345678901234567890.000003', '12345678901234567890.000001')).toBe(2);
    expect(timeCoordinate('1700000000000000000')).toBe(1700000000);
    expect(() => timeCoordinate('1700000000000000001')).toThrow();
    expect(() => plotOffset('99999999999999999999.000000', '0.000000')).toThrow();
  });
});
