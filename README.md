# Glukose Kinders

Single-file PWA for logging glucose readings (mmol/L) — all data in the phone's localStorage, no backend.

- `index.html` — the app. `seed.js` — the 139 August 2026 readings baked in as "Ouer lesings" (grey) on first run only.
- Targets (default 4,5–6,0) editable under Meer. Reading kinds: `fast` (Vastend) / `meal` (Een uur na ete, default; auto-picks Vastend before 10:00).
- Graph skips days with no readings (her ask). Range buttons 7/14/30/Alles; print = Grafiek as PDF for the doctor.
- Export: CSV via Web Share / download, copy-as-text; import by pasting `YYYY-MM-DD HH:MM value [vastend]` lines.
- Deploy: Netlify drag-and-drop of this folder (no repo). Bump `C` in sw.js on every change.
