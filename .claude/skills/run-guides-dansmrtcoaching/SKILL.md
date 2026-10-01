---
name: run-guides-dansmrtcoaching
description: Run, start, serve, test, or screenshot the guides.dansmrtcoaching.com static site (home, /diet /exercise /sleep /stress pillar pages, /prompter teleprompter). Use when asked to run the site, take screenshots of its pages, or smoke-test the prompter.
---

Static HTML/CSS site (no build, no deps) for GitHub Pages. Drive it with `.claude/skills/run-guides-dansmrtcoaching/driver.mjs`: it serves the repo root with `python3 -m http.server`, drives headless Chromium via Playwright, runs checks, and saves screenshots. Paths are relative to the repo root.

## Prerequisites

Already present in the cloud container: `python3`, Node 22, and Playwright at `/opt/node22/lib/node_modules/playwright` with Chromium in `/opt/pw-browsers`. Nothing to install.

## Run (agent path)

```bash
node .claude/skills/run-guides-dansmrtcoaching/driver.mjs
node .claude/skills/run-guides-dansmrtcoaching/driver.mjs --port 8123 --out /tmp/my-shots
```

Flags: `--port` (default 8099), `--out` (default `/tmp/shots`). Exit code is 0 if every check passed, 1 otherwise. The server is started and killed by the driver.

It does one pass:
1. Home page loads, title contains "Free Guides" (`home.png`).
2. Clicks each pillar card (diet, exercise, sleep, stress), checks the `iframe.signup-frame` exists (`<pillar>.png`, full page).
3. `/prompter/`: creates a script via `+ New script`, saves it, opens it, presses play, waits 2.5 s and checks `#stage` scrolled (`prompter-library.png`, `prompter-running.png`).
4. Fails if any `pageerror` or same-origin failed request occurred.

Screenshots land in `/tmp/shots/` by default.

## Run (human path)

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

Ctrl-C to stop. Useless headless; use the driver.

## Gotchas

- **`chromium-cli` is not installed** here, and Python has no `playwright` module. The driver loads Node Playwright through `createRequire('/opt/node22/lib/node_modules/')`; a bare `import 'playwright'` fails.
- **The signup box is blank in screenshots.** The forms are Brevo (`sibforms.com`) iframes and outbound access to that host is blocked in the sandbox. The driver therefore only checks the iframe element exists. The dark empty rectangle is expected, not a CSS bug.
- **Never submit the signup form** from a driver run; on a networked machine it would create a real Brevo contact.
- **Mic/voice mode is untestable headless.** The driver covers the steady-speed ▶ scroll only. Voice control needs a real microphone and `SpeechRecognition`.
- **Prompter scripts live in `localStorage`** per browser profile. Each driver run uses a fresh context, so nothing persists between runs.
- **`/apply/` redirects off-site** to `apply.dansmrtcoaching.com`, so the driver does not visit it.
- **`PROJECT-BRIEF.md` says the repo lives at `C:\repos\...`** (Dan's Windows machine). In this container it is under `/home/user/`.
