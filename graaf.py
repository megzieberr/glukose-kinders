"""Monthly doctor's graph — her mom's preferred layout.

Usage:  python graaf.py <lesings.csv> [Titel]
Reads the CSV exported from the app (Meer -> Deel / stoor alle lesings) or the
Desktop glukose-aug2026.csv, writes <csv-name>.pdf and .png next to it.
A4 landscape: line graph (band 4,5-6,0; days without readings are skipped)
plus a per-day lowest/highest/average strip.
"""
import csv, sys, datetime as dt
from collections import OrderedDict
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

LO, HI = 4.5, 6.0
AF_MON = ['Jan','Feb','Mrt','Apr','Mei','Jun','Jul','Aug','Sep','Okt','Nov','Des']
src = sys.argv[1] if len(sys.argv) > 1 else 'glukose-aug2026.csv'
title = sys.argv[2] if len(sys.argv) > 2 else 'Glukose-lesings'
f = lambda n: f'{n:.1f}'.replace('.', ',')
lab = lambda d: f'{d.day} {AF_MON[d.month-1]}'

pts = []
for r in csv.DictReader(open(src, encoding='utf-8')):
    pts.append((dt.datetime.strptime(r['datum'] + ' ' + r['tyd'], '%Y-%m-%d %H:%M'), float(r['glukose_mmol_L'])))
pts = sorted(set(pts))
days = OrderedDict()
for t, v in pts: days.setdefault(t.date(), []).append(v)
dlist = list(days)
xs = [dlist.index(t.date()) + (t.hour*60 + t.minute)/1440 for t, v in pts]
vs = [v for t, v in pts]

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(11.69, 8.27), gridspec_kw={'height_ratios': [3, 1.3]}, constrained_layout=True)
ax.axhspan(LO, HI, color='#c8e6c9', alpha=0.6, lw=0, label=f'Teiken {f(LO)}–{f(HI)} mmol/L')
ax.plot(xs, vs, '-', color='#1565c0', lw=1.2, marker='o', ms=3.5, mfc='white', mec='#1565c0')
for i in range(1, len(dlist)): ax.axvline(i, color='#bbb', lw=0.6, ls=':')
ax.set_xlim(0, len(dlist)); ax.set_ylim(min(3.5, min(vs)-0.5), max(10, max(vs)+0.5))
ax.set_xticks([i+0.5 for i in range(len(dlist))]); ax.set_xticklabels([lab(d) for d in dlist], fontsize=10)
ax.set_ylabel('Glukose (mmol/L)')
ax.set_title(f'{title} — {lab(dlist[0])} tot {lab(dlist[-1])} ({len(pts)} lesings, dae sonder lesings weggelaat)', fontsize=14, weight='bold')
ax.grid(axis='y', color='#ddd', lw=0.6); ax.legend(loc='upper right', fontsize=9, frameon=False)

lo = [min(v) for v in days.values()]; hi = [max(v) for v in days.values()]; av = [sum(v)/len(v) for v in days.values()]
x = range(len(dlist))
ax2.axhspan(LO, HI, color='#c8e6c9', alpha=0.6, lw=0)
ax2.vlines(x, lo, hi, color='#90a4ae', lw=5, alpha=0.8); ax2.plot(x, av, 'o', color='#1565c0', ms=6, label='Gemiddeld')
for i, (l, h) in enumerate(zip(lo, hi)):
    ax2.text(i, h+0.15, f(h), ha='center', fontsize=7, color='#555'); ax2.text(i, l-0.45, f(l), ha='center', fontsize=7, color='#555')
ax2.set_xticks(list(x)); ax2.set_xticklabels([f'{lab(d)}\n({len(days[d])} lesings)' for d in dlist], fontsize=7.5)
ax2.set_ylim(3.2, 10); ax2.set_ylabel('mmol/L'); ax2.set_title('Per dag: laagste – hoogste (balk) en gemiddeld (kol)', fontsize=10)
ax2.grid(axis='y', color='#ddd', lw=0.6); ax2.legend(loc='upper right', fontsize=8, frameon=False)
for a in (ax, ax2):
    for sp in ('top', 'right'): a.spines[sp].set_visible(False)

out = src.rsplit('.', 1)[0]
fig.savefig(out + '.pdf'); fig.savefig(out + '.png', dpi=200)
print(f'{len(pts)} lesings, {len(dlist)} dae -> {out}.pdf')
