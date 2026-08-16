# guides.dansmrtcoaching.com

Static site, hosted free on GitHub Pages. Four pillar landing pages (Diet, Exercise, Sleep, Stress), each a short teaser for a 30-day reset. The full week-by-week content is delivered as a 4-email weekly sequence per pillar via Brevo — the pages themselves reveal nothing, they capture the signup.

## Status (2026-08-16)

- [x] Repo scaffolded locally
- [x] 4 pillar pages converted to teasers (`/diet`, `/exercise`, `/sleep`, `/stress`) — curiosity-gap week titles, no on-page content, no on-page apply CTA
- [x] Shared homepage (`/index.html`) linking all four
- [x] 16 companion emails written (4 per pillar) — delivered separately, NOT in this repo
- [x] `CNAME` file set for `guides.dansmrtcoaching.com`
- [ ] Push to GitHub, enable Pages
- [ ] Add the DNS record at Hostinger
- [ ] Build the real Brevo signup form + swap in the embed code (currently placeholder forms)
- [ ] Build 4 Brevo automations (the weekly email sequences) behind each form
- [ ] `/apply` page — still to be built; the week-4 emails link to it
- [ ] Dan's review/sign-off before any guide link goes into video copy

## Structure

```
/
├── index.html          homepage, links to all 4 guides
├── styles.css          shared stylesheet
├── CNAME               custom domain for GitHub Pages
├── diet/index.html
├── exercise/index.html
├── sleep/index.html
└── stress/index.html
```

Each guide page is reachable as a clean URL once on GitHub Pages: `guides.dansmrtcoaching.com/diet`, `/exercise`, `/sleep`, `/stress`.

The 16 companion emails live outside this repo (delivered as markdown, loaded into Brevo by hand): `guides/<pillar>/week-1.md` through `week-4.md`.

## To go live

1. **Create the GitHub repo** (public — Pages on the free tier needs public). From inside this folder:
   ```
   git init
   git add .
   git commit -m "Convert pillar pages to teasers, finalize copy"
   git branch -M main
   git remote add origin https://github.com/danielsmrt-cmd/guides-dansmrtcoaching.git
   git push -u origin main
   ```
2. **Enable Pages**: repo Settings → Pages → Deploy from branch → `main` / root.
3. **DNS at Hostinger**: add a `CNAME` record — host `guides`, value `danielsmrt-cmd.github.io`.
4. **Brevo signup form** (per pillar): Contacts → Forms → Create a form (EMAIL, FIRSTNAME), tag by pillar, paste the embed code between `<!-- BREVO_FORM_START -->` and `<!-- BREVO_FORM_END -->` in each guide's `index.html`.
5. **Brevo automation** (per pillar): Automations → Form submitted → send the 4-email weekly sequence (7-day waits). Since the guide content now lives in the emails, the automation IS the delivery — the form can't just be a placeholder before this exists.
6. **Review**: don't add any guide's URL to a video description, pinned comment, or outro until that page resolves live AND its Brevo automation exists behind the form — otherwise a signup starts a 7-day clock with nothing to send.

## Notes

- Brevo's connected MCP tools can read account data and draft/schedule campaigns, but **cannot create lists, forms, or automations** — those are manual in the Brevo web UI.
- Sender on the Brevo account is currently `thesmrtbusiness@gmail.com` — a `@dansmrtcoaching.com` sender would land better once that domain has DNS access (you'll already be in there for the CNAME).
- Free Brevo plan = 300 email sends/month total. Watch this once multiple guide lists are growing.
