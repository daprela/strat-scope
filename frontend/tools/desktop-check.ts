import { chromium, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import { existsSync } from 'node:fs';

const base = `${homedir()}/.local/share/strat-scope`;
const browserId = process.env.STRAT_SCOPE_BROWSER_ID ?? 'chromium';
if (!/^[a-z0-9-]+$/i.test(browserId)) throw new Error('Invalid STRAT_SCOPE_BROWSER_ID');
const profile = browserId === 'chromium' ? 'browser-profile' : `${browserId}-profile`;
const evidencePath = (name: string) =>
  `../foundation-evidence/${browserId === 'chromium' ? name : `${browserId}-${name}`}`;
await mkdir(`${base}/${profile}`, { recursive: true });
const installed = chromium.executablePath();
const executablePath =
  process.env.STRAT_SCOPE_BROWSER ??
  (existsSync(installed)
    ? installed
    : `${homedir()}/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome`);
const context = await chromium.launchPersistentContext(`${base}/${profile}`, {
  executablePath,
  headless: false,
  viewport: { width: 1280, height: 800 },
  args: browserId === 'vivaldi' ? ['--no-first-run', '--no-default-browser-check'] : [],
});
const page = context.pages()[0] ?? (await context.newPage());
try {
  const response = await page.goto('https://127.0.0.1:4111');
  await expect(page.getByRole('status')).toHaveText('Infrastructure ready');
  const details = await response?.securityDetails();
  if (!details) throw new Error('Missing desktop TLS details');
  const evidence = {
    profile: `~/.local/share/strat-scope/${profile} (persistent ${browserId} profile)`,
    browser: browserId,
    browserVersion: context.browser()?.version(),
    origin: page.url(),
    secureContext: await page.evaluate(() => isSecureContext),
    tls: details,
    certificateBypass: false,
    trust: 'Installed host user NSS database; no profile-only CA bundle',
    limits: `This verified profile can be reopened with make browser${browserId === 'chromium' ? '' : `-${browserId}`}.`,
  };
  if (!evidence.secureContext) throw new Error('Desktop origin is not secure');
  await page.screenshot({ path: evidencePath('desktop-https.png') });
  await writeFile(evidencePath('desktop-https.json'), JSON.stringify(evidence, null, 2) + '\n');
  console.log(`${browserId}: normal TLS and authenticated readiness passed`);
} finally {
  await context.close();
}
