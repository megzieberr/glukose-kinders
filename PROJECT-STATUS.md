# Glukose Kinders — PROJECT STATUS

**Last session:** 2026-08-25 (sw v11 shipped: 58-icon food logging + feeling chip + Meal Plan tab. Afternoon: label verdicts for her products, two WhatsApp rule-cards on the Desktop, and the “Is dit reg?” checker SPEC'd — see `PLAN-is-dit-reg.md`, build not started)
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
- Two kinds only: **Voor ete** (before ANY meal, any time of day — her mom's ruling later on 2026-08-24; button small-text says "voor 'n maaltyd"; renamed from "Vastend" earlier that day — internal key stays `fast`) and **Een uur na ete** (the default; still auto-picks Voor ete before 10:00 as a convenience, only the label changed).
- Phone back button (2026-08-24): with the edit or install sheet open, back CLOSES the sheet instead of leaving the app (history.pushState on open, popstate closes; button-closes call history.back() to keep the stack clean).
- Notes with icons (2026-08-24, her mom's ask): ☕ Koffie and 💊 Nuwe medisyne tap-buttons on the entry form append those words to the note; icons are derived from the note TEXT (koffie/coffee → ☕, medisyne/medikasie/pil → 💊) and show on the Vandag chips, the Lesings list and the chart tooltip. "Note didn't save" was investigated: notes always saved, they were just invisible on the home screen — no data loss.
- **One day at a time** (2026-08-24, her mom's ask): a **"1 dag"** button first in the range row, plus a `‹ Donderdag 20 Aug ›` bar that steps through days *with readings* (arrows disable at the oldest/newest day; the bar only shows in 1-dag mode). In that view the x-axis becomes **hours of the day** — labels 06:00/12:00/18:00, faint grid every 3 h — and dots stay large. Stats, the in-target line and the per-day table all follow the selection, and *Grafiek as PDF* prints the single day with a full 00:00–24:00 axis. Midnight labels are deliberately left off the phone chart: five time labels crowd each other at 360 px.
- **Graph skips days with no readings** — days sit side by side, no gap. "7 dae" = last 7 days *with readings*.
- Friendliest possible UI: keypad entry (no phone keyboard), big text, one screen to save. Base font 18px; chart drawn at true pixel width so labels stay 15–16px.
- Dots shrink on days with >8 / >14 readings (August had 17–22/day); normal days keep big dots.
- PDF for the doctor = `renderPrint()` → `#printpage`, one A4 **landscape** page in the matplotlib style she approved (blue line, white dots, per-day low–high bar + average). Prints whatever range is selected (Alles for the full month). Screen chart untouched.
- Netlify avoided on purpose (WhenWorks eats her credits) → GitHub Pages.
- **Food + feeling on every reading** (2026-08-25, her mom's ask): a *"Wat het jy geëet of gedrink?"* text box on the entry screen with live icons appearing as she types, plus a tap-grid of the whole **58-icon pack** (every icon labelled). Words are matched in **Afrikaans AND English**; food with no icon simply saves as plain text — that is deliberate, never drop the typed name. Stored as `f` on the reading. Under it, a one-tap **😀 Goed / 😐 So-so / 🤢 Sleg** row, stored as `m`. Both show on the Vandag chips, the Lesings list and the chart tooltip, and both are editable in the edit sheet.
  - The old ☕/💊 tag buttons are GONE — they folded into the icon pack (Koffie and Medisyne are entries in the grid). Icons still derive from the note text too, so older readings keep theirs.
  - Regex gotcha, already fixed: unbounded patterns matched inside other words — `hake` matched "s**hake**", `ys` matched "r**ys**", `nuts` matched "do**nuts**". Any new food word that is a substring of another word needs `\b` boundaries.
- **Meal Plan tab** (2026-08-25): a fifth nav tab. Her mom asked for the name to stay **"Meal Plan"** in English even though the rest of the app is Afrikaans — do not translate it. Contents:
  - *Wat eet ek nou?* — reads the clock and shows only the meal slot she is in (Ontbyt / voormiddag / Middagete / namiddag / Aandete / voor slaaptyd); outside 05:00–22:00 it says Slaaptyd and offers breakfast. The whole day sits behind *Wys my die hele dag*.
  - 23 meal options, each with a one-line reason and a 👍/👎 she can tap (saved in `glukose.planfb`).
  - *Die vier reëls*, a 10-item **Ruil om** swap list, and an **Inkopielys** with tick-off items (`glukose.shop`) plus a share button that lists only what is NOT yet ticked.
  - *Stuur my week vir Megan* → a .txt with the last 7 days of readings + food + feelings + which meals she liked + her free-text note. That is the feedback loop: her mom exports, Megan sends it here, the plan gets updated.
- **Photo-AI “yay/nay” scanner DECLINED** (Fable design ruling, accepted 2026-08-25): needs a paid key that can't live in a public repo, a binary verdict is the wrong shape (real answers are “yes, IF…”), and it kills the label-reading skill. Approved instead: the typed three-number **“Is dit reg?” checker** — full spec + rule table + test fixtures in `PLAN-is-dit-reg.md`. Barcode auto-fill is a v2 candidate only.
- **Plan content is food-only, on purpose** (her ruling 2026-08-25): no diagnosis, no medicine names, no personal details anywhere in the repo. The medical reasoning behind the plan (why certain proteins were chosen, why there are no-appetite options, the product notes, the questions for the doctor) lives OUTSIDE the repo, in `Desktop\glukose-mamma-notas.md`. Keep it that way.

## Data / privacy — the one hard rule
**No readings ever go into the repo.** `*.csv` is gitignored. Her August 2026 history was in `Desktop\glukose-aug2026.csv` (139 readings, duplicates already removed) — **that file went to the Recycle Bin with the old Desktop folder on 2026-08-24** and is only recoverable until the bin is emptied; her mom still has the data on her phone plus the WhatsApped copy. The app folder now lives at `Desktop\Claude Code Projects\glukose-app` (fresh clone). Import stays *Meer → Bring lêer in (CSV)*. Import de-duplicates on date+time+value, so re-importing is safe. Imported August rows are kind `hist` ("Ouer lesings", grey).

## Files
- `index.html` — whole app (CSS + JS inline). Sections: entry / today / chart / list / more / install sheet / edit sheet.
- `sw.js` — cache name `glukose-vN`. **Bump N on every change** or phones keep the old version. Currently **v11**.
- CSV import now also reads the `nota` column (was dropped before 2026-08-24) and maps tipe "Voor ete" back to `fast`.
- `manifest.json`, `icons/` — PWA bits. `README.md` — short public description.
- Storage keys: `glukose.v1` (readings array `{id,t:'YYYY-MM-DDTHH:MM',v,k:'fast'|'meal'|'hist',n?,f?,m?}`), `glukose.targets`, `glukose.installLater`, `glukose.planfb` (👍/👎 per meal), `glukose.shop` (ticked shopping items), `glukose.fbnote` (her note to Megan).
- CSV is now **7 columns**: `datum,tyd,glukose_mmol_L,tipe,nota,kos,gevoel`. Import accepts BOTH the old 5-column files and the new ones, and still de-duplicates on date+time+value. `graaf.py` uses `csv.DictReader`, so the extra columns do not affect the monthly doctor's graph.

## How to ship a change
1. Edit `index.html`; bump `C` in `sw.js`.
2. Check locally: `python -m http.server 8766 --directory .` + Playwright at 360px (screenshots in the Browser pane don't work — use headless Playwright).
3. `git commit -F msgfile` (PowerShell quoting gotcha) → `git push origin main`. Pages goes live in ~40 s; confirm with `curl .../sw.js`.
4. Tell her: close and reopen the app twice to pick up the new version. Readings survive updates.

## Monthly doctor's graph (her mom prefers THIS over the app's PDF)
The in-app *Grafiek as PDF* now produces the same layout (v7), so the script is the fallback only. Routine if needed: her mom sends the CSV from *Meer → Deel / stoor alle lesings*; run `python graaf.py <die.csv>` (in this folder; band 4,5–6,0; missed days skipped) → `Desktop\Glukose_grafiek_<month>.pdf`. The in-app print can stay as is; don't spend more time on it.

## Pending on Megan
- 📱 5 min **[blocking]**: after the deploy, open the app on her mom's phone twice, then check the **Meal Plan** tab loads and that one reading saves with food + a feeling.
- 💻 1 min **[whenever]**: if the binned `glukose-aug2026.csv` wasn't meant to go, restore it from the Recycle Bin before emptying — after that her mom's phone + WhatsApp are the only copies.
- (Optional, some day: ask her mom to send a CSV backup via *Meer → Deel / stoor alle lesings* every few weeks.)

## Next up
- **Build the “Is dit reg?” checker** from `PLAN-is-dit-reg.md` (one card on Meal Plan, no storage, sw → v12; fixtures in the plan are the Playwright tests). Routine, well-scoped — Sonnet can take it end-to-end.
- After ~2 weeks of food logging: rank her real meals by what they did to her (the app will have the data — show "hierdie ontbyt: gem. 6,1 na ete" next to each plan option). This was always the point of the icons.
- Her mom exports her week from the Meal Plan tab → Megan sends the .txt here → the plan gets adjusted to what she actually liked and what actually worked.
- Still open: nothing in the plan yet accounts for what a dietitian might change. The reasoning file on the Desktop is the thing to hand to the doctor at the follow-up.

## Ideas not built (only on her say-so)
- Weekly summary line ("hierdie week: gem. 5,8, 80% binne teiken").
- Reminder push for the morning vastend reading (would need a server — currently nothing online, keep it that way unless asked).
