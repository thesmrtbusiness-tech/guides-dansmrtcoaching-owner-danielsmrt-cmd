# Project Brief — DanSmrtCoaching

> Paste-in context for any Claude surface (esp. the claude.ai web app, which can't read local memory files). Keep this current when the durable facts change.

## Who
**Dan** runs the **DanSmrtCoaching** YouTube channel. Framework: **K.I.S.S. of D.E.S.S.** — coaching adults **40+** across four pillars: **Diet, Exercise, Sleep, Stress**.

## The two places work happens
| What | Where | Notes |
|------|-------|-------|
| Content & scripts | `G:\My Drive\contentpipeline` | Google Drive folder, **not** a git repo. Shorts/long-form scripts, batches, teleprompter files. |
| Guides / lead-magnet site | `C:\repos\guides-dansmrtcoaching` | Git repo. Remote: `thesmrtbusiness-tech/guides-dansmrtcoaching-owner-danielsmrt-cmd`, branch `main`. |

Ignore `contentpipeline\_system\guides-dansmrtcoaching-OLD-donotuse\` — stale copy, do not edit.

## The guides site
One landing page per pillar — `diet/`, `exercise/`, `sleep/`, `stress/` (plus `apply/`). Each signup form lives inside a `<!-- BREVO_FORM_START --> / <!-- BREVO_FORM_END -->` block and POSTs to a **per-pillar Brevo (sibforms.com) endpoint**. All four wired to Brevo as of **2026-08-19**.

**Form convention (match this, don't paste Brevo's raw grey-box embed):**
- Keep the site's own `signup-form` and `btn` CSS classes and each page's existing button text.
- `method="POST"`, `target="_blank"`, `action` = that pillar's Brevo URL.
- Inputs named exactly `FIRSTNAME` and `EMAIL`.
- Two Brevo hidden fields at the end: visually-hidden honeypot `email_address_check` + `<input type="hidden" name="locale" value="en">`.
- `diet/index.html` is the reference implementation.

## Working with Claude
- **Claude Code & Cowork** share memory files (`~/.claude/projects/G--My-Drive-contentpipeline/memory/`) and skills — they already know all of the above; no need to re-explain.
- **Relevant skills** (auto-load): `batch-scripts`, `my-audience-avatar`, `audience-insights`, `make-captions`, `video-edit`.
- **claude.ai web app** can't read local memory — paste this file (or add it to a claude.ai Project) to bring it up to speed.
