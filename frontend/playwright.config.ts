import { defineConfig } from '@playwright/test';
import { homedir } from 'node:os';
import { existsSync } from 'node:fs';
import { chromium } from '@playwright/test';

const installed = chromium.executablePath();
const browser =
  process.env.STRAT_SCOPE_BROWSER ??
  (existsSync(installed)
    ? installed
    : `${homedir()}/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`);
const browserId = process.env.STRAT_SCOPE_BROWSER_ID ?? 'chromium';
if (!/^[a-z0-9-]+$/i.test(browserId)) throw new Error('Invalid STRAT_SCOPE_BROWSER_ID');

export default defineConfig({
  testDir: './tests/browser',
  workers: 1,
  timeout: 60000,
  use: {
    browserName: 'chromium',
    viewport: { width: 1600, height: 1000 },
    launchOptions: {
      executablePath: browser,
      args: browserId === 'vivaldi' ? ['--no-first-run', '--no-default-browser-check'] : [],
    },
  },
  webServer: {
    command: 'npm exec vite -- --host 127.0.0.1 --port 4112 --strictPort',
    url: 'http://127.0.0.1:4112/tests/browser/probe.html',
    reuseExistingServer: false,
  },
  reporter: [['list']],
});
