# Plan — "Is dit reg?" label checker

*Spec written 2026-08-25 (Fable design pass). Build not started. Scope: one card, no backend,
no storage, food logic only — nothing personal or medical goes in this public repo.*

## What it is

A card on the **Meal Plan** tab. She copies **three numbers** off the back of any packet —
per-portion **Koolhidrate**, **Proteïen**, **Vesel** — and the app answers in the kinders
voice with a verdict AND the reason. It replaces "photograph it and ask Megan" for the
common cases, and every use teaches her which three numbers matter.

Explicitly rejected alternative (decision, 2026-08-25): a photo-AI "yay/nay" scanner.
Reasons: needs a paid AI key that can't live in a public repo (so a serverless proxy +
billing), a binary verdict is the wrong shape (most real answers are "yes, IF…"), and it
removes the label-reading skill instead of building it. A barcode-scan v2 that only
*fills in* the three numbers (BarcodeDetector / OpenFoodFacts) may come later; SA coverage
is patchy, so it assists, never replaces, the typed path.

## UI

- Card title: **Is dit reg om te eet?** Placement: on `#s-plan`, directly under the
  "Wat eet ek nou?" card (above the rules — checking a packet is an in-the-moment task).
- Three numeric inputs, one row, same `.meta label` styling as the targets card:
  `Koolhidrate (g)` · `Proteïen (g)` · `Vesel (g)`.
  - Accept comma decimals ("1,9") — SA labels use commas. `inputmode="decimal"`.
- One hint line above the inputs, always visible:
  **"Gebruik die PER PORSIE kolom — nie die 100 g kolom nie. Kyk ook hoeveel porsies in
  die pak is."** (The wafers lesson: 1 porsie = 1 wafer, 5 in die pak.)
- One button: **Sê vir my** → verdict block appears under it (no page change).
- Verdict block: coloured like the app's verdict line (`--ok` green / `--warn` amber /
  `--meal` red), big Fraunces one-liner + 1–2 plain sentences of reason/pairing advice.
- Stateless. No localStorage key, no migration, nothing saved.

## Rules engine

Let `C` = carbs (g), `P` = protein (g), `V` = fibre (g), all per portion.
Define the **rem** (brake): `R = P + V`.

| # | Condition | Verdict tier | Voice (gist — builder polishes) |
|---|-----------|--------------|--------------------------------|
| 1 | `C <= 5` | GROEN | "Byna geen koolhidrate — die kinders sal dit skaars agterkom. Eet gerus." |
| 2 | `C <= 12` en `R >= C/2` | GROEN | "Klein porsie, en die proteïen/vesel is die rem. Reg so." |
| 3 | `C <= 12` en `R < C/2` | GEEL | "Klein, maar vinnig — eet 'n stukkie kaas of 'n paar neute saam." |
| 4 | `C <= 25` en `R >= C/2` | GEEL | "Dit is 'n ETE se koolhidrate, met 'n goeie rem ingebou. Eet dit as 'n ete, nie as 'n happie nie." |
| 5 | `C <= 25` en `R < C/2` | ROOI | "Ete se koolhidrate met byna geen rem — nooit alleen nie. Neute, kaas of eier daarby, en nie op 'n leë maag nie." |
| 6 | `C > 25` | ROOI | "Te veel op een slag. Halveer die porsie, en eet proteïen saam." |

First matching row wins (top to bottom). Test vectors from real packets read this session
(these become the Playwright fixtures — expected tier in brackets):

| Product (per porsie) | C | P | V | Expect |
|---|---|---|---|---|
| Mozzarella (30 g) | 0,5 | 6 | 0 | 1 GROEN |
| Body Fit Nougat bar (50 g) | 3 | 15 | 15 | 1 GROEN |
| Canderel wafer, EEN (9 g) | 3 | 0,4 | 0,1 | 1 GROEN |
| Canderel wafers, hele pak (45 g) | 15 | 2 | 0,4 | 5 ROOI |
| Jungle Lite bar (40 g) | 15 | 3,7 | 3,1 | 5 ROOI (R=6,8 < 7,5) |
| Futurelife Zero (50 g) | 20 | 9,1 | 6,3 | 4 GEEL "ete" (R=15,4 ≥ 10) |
| Replace shake (± porsie) | ±19 | ±10 | ±6 | 4 GEEL "ete" |

Note Jungle lands ROOI-nooit-alleen and Futurelife lands GEEL-ete — matching the
hand verdicts given this session. If tuning ever changes a fixture's tier, the fixture
is the law: re-derive the threshold, don't bend the fixture.

## Validation & edge cases

- Empty/invalid C → disable the button (P and V may default to 0 if left blank — labels
  sometimes omit fibre).
- Comma → dot before `parseFloat`, same as the keypad convention elsewhere.
- If `C > 60`: extra amber line "Is dit dalk die 100 g-kolom? Kyk weer op die pakkie." —
  don't block, just nudge (some real portions are big).
- Numbers stay ≥ 0; cap silly values (>150) with the same nudge.

## Ship checklist

1. Edit `index.html` only (card markup + ±40 lines JS + reuse existing CSS classes; new
   CSS only if truly needed).
2. Bump `sw.js` to **v12**.
3. Extend `verify.py`-style Playwright run: type each fixture, assert tier colour + a
   keyword of the voice line; plus the comma-decimal case and the 100 g nudge.
4. Screenshot at 360 px, LOOK at it, then commit → push → confirm live `sw.js` v12.
5. Effort: one short session. Routine well-scoped work — Sonnet can build it end-to-end
   from this file; Opus fine too.

## Out of scope (v2 candidates, only on Megan's say-so)

- Barcode scan to auto-fill the three numbers (BarcodeDetector, OpenFoodFacts fallback
  zxing-wasm; SA coverage patchy — always leave the typed path primary).
- "Stuur vir Megan" share shortcut for the photo-and-ask flow.
- Optional fourth field for Suiker if real use shows the three numbers misjudge sweets.
