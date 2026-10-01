// Smoke driver for the static guides site. Serves the repo root, drives headless Chromium.
// Usage (from repo root): node .claude/skills/run-guides-dansmrtcoaching/driver.mjs [--port 8099] [--out /tmp/shots]
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const port = arg('--port', '8099');
const out = arg('--out', '/tmp/shots');
const base = `http://localhost:${port}`;
mkdirSync(out, { recursive: true });

const server = spawn('python3', ['-m', 'http.server', port, '--bind', '127.0.0.1'], { stdio: 'ignore' });
let failed = 0;
const check = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${msg}`); if (!ok) failed++; };

try {
  for (let i = 0; i < 50; i++) {
    try { if ((await fetch(base)).ok) break; } catch {}
    await new Promise(r => setTimeout(r, 200));
  }
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  // Brevo iframe + external fonts are unreachable/blocked in the sandbox; only count same-origin failures.
  page.on('requestfailed', r => { if (r.url().startsWith(base)) errors.push('requestfailed ' + r.url()); });

  // Home -> each pillar
  await page.goto(base + '/');
  check((await page.title()).includes('Free Guides'), 'home title');
  await page.screenshot({ path: `${out}/home.png` });
  for (const p of ['diet', 'exercise', 'sleep', 'stress']) {
    await page.goto(base + '/');
    await page.click(`a[href="${p}/"]`);
    await page.waitForURL(`**/${p}/`);
    check(await page.locator('iframe.signup-frame').count() === 1, `${p}: Brevo signup iframe present`);
    await page.screenshot({ path: `${out}/${p}.png`, fullPage: true });
  }

  // Prompter: create a script, open it, press play, confirm scroll
  await page.goto(base + '/prompter/');
  await page.click('#btn-new-script');
  await page.fill('#editor-title', 'Smoke test');
  await page.fill('#editor-body', Array.from({ length: 80 }, (_, i) => `Line ${i + 1} of the smoke test script.`).join('\n\n'));
  await page.click('#btn-editor-save');
  await page.locator('.script-card, .script-title').first().waitFor();
  await page.screenshot({ path: `${out}/prompter-library.png` });
  await page.locator('.script-title', { hasText: 'Smoke test' }).first().click();
  await page.locator('#view-prompter').waitFor({ state: 'visible' });
  await page.click('#btn-play-toggle');
  await page.waitForTimeout(2500);
  const top = await page.evaluate(() => { const s = document.getElementById('stage'); return s.scrollTop || window.scrollY; });
  check(top > 0, `prompter auto-scroll moved (scrollTop=${top})`);
  await page.screenshot({ path: `${out}/prompter-running.png` });

  check(errors.length === 0, `no page errors${errors.length ? ': ' + errors.join(' | ') : ''}`);
  await browser.close();
} finally {
  server.kill();
}
console.log(`screenshots in ${out}`);
process.exit(failed ? 1 : 0);
