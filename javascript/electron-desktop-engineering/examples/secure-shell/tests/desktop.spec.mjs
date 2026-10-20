// NOT EXECUTED during authoring. Requires installed Electron and @playwright/test.
import { test, expect } from '@playwright/test';
import { _electron as electron } from 'playwright';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
test('narrow bridge smoke test in actual Electron', async () => {
  const app = await electron.launch({ args: [appRoot] });
  try {
    const page = await app.firstWindow();
    await expect(page.getByRole('heading', { name: 'Constrained desktop bridge' })).toBeVisible();
    await page.getByLabel('Theme').selectOption('dark');
    await page.getByRole('button', { name: 'Apply theme', exact: true }).click();
    await expect(page.getByRole('status')).toContainText('Theme: dark');
    expect(await page.evaluate(() => typeof window.require)).toBe('undefined');
    expect(await page.evaluate(() => typeof window.process)).toBe('undefined');
    expect(await page.evaluate(() => Object.keys(window.desktop).sort())).toEqual(['getPreferences','onPreferencesChanged','openDocumentation','setTheme'].sort());
    expect(await page.evaluate(async () => { try { await window.desktop.setTheme('invalid'); return 'accepted'; } catch { return 'rejected'; } })).toBe('rejected');
  } finally { await app.close(); }
});
