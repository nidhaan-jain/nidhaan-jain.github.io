"""
Dynamic DiD: share of Eastern Enlargement workers, firms with vs. without a
works council in 2010 (firm and year FE, no individual controls).

Coefficients and 95% CIs are from GRAPH 3 of nj01_wc_ct_pres.log (lines 559-572).
2010 is the omitted base year: coefficient zero, no confidence interval.
Styling follows the event-study plots in RTW/prog/rtw/analysis/event_study_fs_v2.do.
"""

from pathlib import Path

import matplotlib.pyplot as plt

OUTPUT = Path(__file__).with_suffix(".png")

# year: (coefficient, CI low, CI high)
RESULTS = {
    2005: (0.0005031, -0.0015255, 0.0025317),
    2006: (0.0005176, -0.0014633, 0.0024985),
    2007: (-0.0000309, -0.0016590, 0.0015972),
    2008: (0.0007304, -0.0007393, 0.0022000),
    2009: (0.0006485, -0.0004387, 0.0017358),
    2010: (0.0, None, None),  # omitted base year
    2011: (0.0000766, -0.0010137, 0.0011669),
    2012: (-0.0025256, -0.0040989, -0.0009523),
    2013: (-0.0037812, -0.0056610, -0.0019015),
    2014: (-0.0047040, -0.0069478, -0.0024603),
    2015: (-0.0062577, -0.0097463, -0.0027691),
    2016: (-0.0069328, -0.0098364, -0.0040292),
    2017: (-0.0099098, -0.0138054, -0.0060141),
    2018: (-0.0111643, -0.0156618, -0.0066669),
    2019: (-0.0103010, -0.0148360, -0.0057661),
}

YTICKS = [0.015, 0.01, 0.005, 0, -0.005, -0.01, -0.015]
YTICK_LABELS = [".015", ".01", ".005", "0", "-.005", "-.01", "-.015"]  # Stata number format

years = list(RESULTS)
coefs = [RESULTS[y][0] for y in years]

plt.rcParams["font.family"] = ["Arial", "Helvetica", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(10, 6))

# Reference lines and grid, behind the estimates
for tick in YTICKS:
    if tick != 0:
        ax.axhline(tick, color="#eeeeee", linestyle=(0, (6, 4)), linewidth=1.2, zorder=0)
ax.axhline(0, color="#bdbdbd", linewidth=1.3, zorder=1)
ax.axvline(2010.5, color="#bdbdbd", linewidth=1.3, zorder=1)

# Capped 95% CIs (the omitted year has none)
for year, (_, low, high) in RESULTS.items():
    if low is not None:
        ax.vlines(year, low, high, color="black", linewidth=0.9, zorder=2)
        ax.hlines([low, high], year - 0.05, year + 0.05, color="black", linewidth=0.9, zorder=2)

# Connected point estimates
ax.plot(years, coefs, color="black", linewidth=1.0, marker="o", markersize=7, zorder=3)

ax.set_xlim(2004.82, 2019.18)
ax.set_ylim(-0.0164, 0.0164)
ax.set_xticks(years)
ax.set_yticks(YTICKS)
ax.set_yticklabels(YTICK_LABELS)
ax.tick_params(labelsize=15, length=7, width=1.0)
ax.set_xlabel("Year", fontsize=16, labelpad=8)
ax.set_ylabel("Share of workers", fontsize=16, labelpad=10)
ax.set_title("Share of workers in the firm from 2004 EU entrant countries", fontsize=19, pad=14)

for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_linewidth(1.0)

fig.tight_layout()
fig.savefig(OUTPUT, dpi=300, facecolor="white")
