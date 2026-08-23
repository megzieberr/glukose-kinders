# Glukose Kinders — PROJECT STATUS

**Last session:** 2026-08-23 (built, deployed, three fix rounds — all live)
**Live:** https://megzieberr.github.io/glukose-kinders/ (GitHub Pages, repo `megzieberr/glukose-kinders`, PUBLIC)
**Installed on:** Megan's mom's phone (Brave, Android) — via the browser menu "Add to home screen"

## What it is
Glucose logger (mmol/L) for Megan's mom. One `index.html`, no backend, no login. Every reading lives in the phone's localStorage only.
Name from her doctor's story: beta cells are "stout kinders" who skip their homework then overcompensate. The verdict line under the number keeps that voice:
- within target → "Binne teiken — die kinders doen hul huiswerk ✓"
- above → "Bo teiken — die kinders oordryf nou"
- below → "Bietjie laag — die kinders slaap"

## Her rulings (don't undo)
- Targets **4,5–6,0** (her doctor's numbers; editable under Meer).
- Two kinds only: **Vastend** (once, before breakfast) and **Een uur na ete** (the default; auto-picks Vastend before 10:00).
- **Graph skips days with no readings** — days sit side by side, no gap. "7 dae" = last 7 days *with readings*.
- Friendliest possible UI: keypad entry (no phone keyboard), big text, one screen to save. Base font 18px; chart drawn at true pixel width so labels stay 15–16px.
- Dots shrink on days with >8 / >14 readings (August had 17–22/day); normal days keep big dots.
- PDF for the doctor = one A4 page: wide chart + stats row + per-day table. Print uses its own chart geometry (`printMode`).
- Netlify avoided on purpose (WhenWorks eats her credits) → GitHub Pages.

## Data / privacy — the one hard rule
**No readings ever go into the repo.** `*.csv` is gitignored. Her August 2026 history lives only in `Desktop\glukose-aug2026.csv` (139 readings, duplicates already removed), sent to her mom by WhatsApp and loaded via *Meer → Bring lêer in (CSV)*. Import de-duplicates on date+time+value, so re-importing is safe. Imported August rows are kind `hist` ("Ouer lesings", grey).

## Files
- `index.html` — whole app (CSS + JS inline). Sections: entry / today / chart / list / more / install sheet / edit sheet.
- `sw.js` — cache name `glukose-vN`. **Bump N on every change** or phones keep the old version. Currently **v6**.
- `manifest.json`, `icons/` — PWA bits. `README.md` — short public description.
- Storage keys: `glukose.v1` (readings array `{id,t:'YYYY-MM-DDTHH:MM',v,k:'fast'|'meal'|'hist',n?}`), `glukose.targets`, `glukose.installLater`.

## How to ship a change
1. Edit `index.html`; bump `C` in `sw.js`.
2. Check locally: `python -m http.server 8766 --directory .` + Playwright at 360px (screenshots in the Browser pane don't work — use headless Playwright).
3. `git commit -F msgfile` (PowerShell quoting gotcha) → `git push origin main`. Pages goes live in ~40 s; confirm with `curl .../sw.js`.
4. Tell her: close and reopen the app twice to pick up the new version. Readings survive updates.

## Monthly doctor's graph (her mom prefers THIS over the app's PDF)
She likes the original matplotlib A4 landscape PDF (line graph + per-day min/max/avg strip), not the in-app print. Routine: her mom sends the CSV from *Meer → Deel / stoor alle lesings*; run `python graaf.py <die.csv>` (in this folder; band 4,5–6,0; missed days skipped) → `Desktop\Glukose_grafiek_<month>.pdf`. The in-app print can stay as is; don't spend more time on it.

## Pending on Megan
- Nothing. (Optional, some day: ask her mom to send a CSV backup via *Meer → Deel / stoor alle lesings* every few weeks.)

## Ideas not built (only on her say-so)
- Weekly summary line ("hierdie week: gem. 5,8, 80% binne teiken").
- Reminder push for the morning vastend reading (would need a server — currently nothing online, keep it that way unless asked).
