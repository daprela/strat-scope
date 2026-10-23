import { afterEach, expect, it, vi } from 'vitest';
import { render, screen, cleanup } from '@testing-library/react';
import { Foundation } from './Foundation';

vi.mock('./transport', () => ({ connectStatus: vi.fn(() => Promise.reject(new Error('denied'))) }));
afterEach(cleanup);
it('does not present unimplemented trading features as available', async () => {
  render(<Foundation />);
  expect(screen.getByText(/features are not implemented/)).toBeDefined();
  expect(screen.getByRole('status')).toBeDefined();
  await screen.findByText(/Authority unavailable/);
});
