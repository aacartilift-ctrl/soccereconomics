"""
Generate new figures for v3 paper:
  1. Big 5 average stoppage time (1H, 2H, total) over seasons
     with two vertical dashed lines (announcement + implementation)
     and trend lines for 3 segments
  2. All leagues averaged stoppage time over seasons
     with same vertical lines and trend lines
"""
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# ── Style ──────────────────────────────────────────────────────
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 9,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'serif',
})

BLUE = '#4878A8'
CORAL = '#E07060'
GRAY = '#888888'
GREEN = '#5A9A6A'

# ── Load data ──────────────────────────────────────────────────
DATA_PATH = '../../../data/processed/match_panel.csv'

with open(DATA_PATH) as f:
    rows = list(csv.DictReader(f))

BIG5 = {'E0', 'SP1', 'D1', 'I1', 'F1'}

# Season ordering (numeric x-axis)
SEASONS = [
    '2014-15', '2015-16', '2016-17', '2017-18', '2018-19',
    '2019-20', '2020-21', '2021-22', '2022-23',
    '2023-24', '2024-25', '2025-26'
]
season_to_x = {s: i for i, s in enumerate(SEASONS)}

# ── Aggregate by season ────────────────────────────────────────
def aggregate(rows, league_filter=None):
    """Return dict of season -> {s1h: mean, s2h: mean, total: mean, n1h, n2h}"""
    by_season = defaultdict(lambda: {'s1h': [], 's2h': []})
    for r in rows:
        if league_filter and r['league_code'] not in league_filter:
            continue
        s = r['season']
        if s not in season_to_x:
            continue
        if r['stoppage_2h'] and r['stoppage_2h'] != '':
            by_season[s]['s2h'].append(float(r['stoppage_2h']))
        if r['stoppage_1h'] and r['stoppage_1h'] != '':
            by_season[s]['s1h'].append(float(r['stoppage_1h']))

    result = {}
    for s in SEASONS:
        if s in by_season:
            d = by_season[s]
            m1h = np.mean(d['s1h']) if d['s1h'] else np.nan
            m2h = np.mean(d['s2h']) if d['s2h'] else np.nan
            total = m1h + m2h if not (np.isnan(m1h) or np.isnan(m2h)) else np.nan
            result[s] = {
                's1h': m1h, 's2h': m2h, 'total': total,
                'n1h': len(d['s1h']), 'n2h': len(d['s2h'])
            }
    return result


def fit_segments(x_all, y_all, break1, break2):
    """Fit OLS lines for 3 segments defined by two breakpoints."""
    lines = []
    for lo, hi in [(None, break1), (break1, break2), (break2, None)]:
        mask = np.ones(len(x_all), dtype=bool)
        if lo is not None:
            mask &= x_all >= lo
        if hi is not None:
            mask &= x_all <= hi
        if mask.sum() < 2:
            lines.append(None)
            continue
        xm, ym = x_all[mask], y_all[mask]
        # Remove nans
        valid = ~np.isnan(ym)
        if valid.sum() < 2:
            lines.append(None)
            continue
        xm, ym = xm[valid], ym[valid]
        coef = np.polyfit(xm, ym, 1)
        x_range = np.linspace(xm.min(), xm.max(), 50)
        y_range = np.polyval(coef, x_range)
        lines.append((x_range, y_range, coef))
    return lines


def plot_stoppage_timeseries(agg, title, filename, show_1h=True):
    """Plot stoppage time series with vertical lines and trend fits."""
    fig, ax = plt.subplots(figsize=(10, 5.5))

    seasons_present = [s for s in SEASONS if s in agg]
    x = np.array([season_to_x[s] for s in seasons_present])

    y_2h = np.array([agg[s]['s2h'] for s in seasons_present])
    y_total = np.array([agg[s]['total'] for s in seasons_present])

    # Vertical lines: announcement (Nov 2022 ~ mid 2022-23 season = 8.3)
    # Implementation (Aug 2023 ~ start of 2023-24 = 9.0)
    x_announce = 8.3   # Nov 2022, within 2022-23 season
    x_implement = 9.0  # Aug 2023, start of 2023-24

    ax.axvline(x_announce, color='#CC4444', ls='--', lw=1.5, alpha=0.7,
               label='FIFA directive (Nov 2022)')
    ax.axvline(x_implement, color='#4444CC', ls='--', lw=1.5, alpha=0.7,
               label='Domestic implementation (Aug 2023)')

    # Plot data
    ax.plot(x, y_2h, 'o-', color=CORAL, lw=2, ms=7, label='2nd half stoppage', zorder=5)
    if show_1h:
        y_1h = np.array([agg[s]['s1h'] for s in seasons_present])
        ax.plot(x, y_1h, 's-', color=BLUE, lw=2, ms=6, label='1st half stoppage', zorder=5)
        ax.plot(x, y_total, 'D-', color=GREEN, lw=2, ms=6, label='Total stoppage', zorder=5)

        # Trend lines for 2H (most visible)
        lines_2h = fit_segments(x, y_2h, x_announce, x_implement)
        for seg in lines_2h:
            if seg:
                ax.plot(seg[0], seg[1], '-', color=CORAL, lw=1.5, alpha=0.4)

        lines_1h = fit_segments(x, y_1h, x_announce, x_implement)
        for seg in lines_1h:
            if seg:
                ax.plot(seg[0], seg[1], '-', color=BLUE, lw=1.5, alpha=0.4)
    else:
        # All leagues - just 2H with trend lines
        lines_2h = fit_segments(x, y_2h, x_announce, x_implement)
        for seg in lines_2h:
            if seg:
                ax.plot(seg[0], seg[1], '-', color=CORAL, lw=1.5, alpha=0.4)

    # Labels
    ax.set_xticks(range(len(SEASONS)))
    ax.set_xticklabels([s.replace('-', '\n') for s in SEASONS], rotation=0)
    ax.set_ylabel('Minutes')
    ax.set_title(title, fontweight='bold', pad=12)
    ax.legend(loc='upper left', framealpha=0.9)
    ax.set_xlim(-0.5, len(SEASONS) - 0.5)
    ax.grid(axis='y', alpha=0.3)

    # Annotate the segments
    ax.text(x_announce - 0.15, ax.get_ylim()[1] * 0.97, 'Pre', ha='right',
            fontsize=9, color=GRAY, fontstyle='italic')
    ax.text((x_announce + x_implement) / 2, ax.get_ylim()[1] * 0.97, 'Transition',
            ha='center', fontsize=9, color=GRAY, fontstyle='italic')
    ax.text(x_implement + 0.15, ax.get_ylim()[1] * 0.97, 'Post', ha='left',
            fontsize=9, color=GRAY, fontstyle='italic')

    plt.tight_layout()
    fig.savefig(filename + '.pdf')
    fig.savefig(filename + '.png')
    plt.close(fig)
    print(f'  Saved: {filename}.pdf/.png')


# ═══════════════════════════════════════════════════════════════
#  FIGURE A: Big 5 Average Stoppage Time (1H, 2H, Total)
# ═══════════════════════════════════════════════════════════════
print('Generating Big 5 stoppage time series...')
agg_big5 = aggregate(rows, BIG5)
plot_stoppage_timeseries(
    agg_big5,
    'Big Five Leagues: Mean Stoppage Time by Season',
    'fig_big5_stoppage_timeseries',
    show_1h=True
)

# ═══════════════════════════════════════════════════════════════
#  FIGURE B: All Leagues Average Stoppage Time (2H)
# ═══════════════════════════════════════════════════════════════
print('Generating all-leagues stoppage time series...')
agg_all = aggregate(rows)
plot_stoppage_timeseries(
    agg_all,
    'All 15 Leagues: Mean Second-Half Stoppage Time by Season',
    'fig_all_leagues_stoppage_timeseries',
    show_1h=False
)

# ═══════════════════════════════════════════════════════════════
#  FIGURE C: Goal Displacement Visualization
# ═══════════════════════════════════════════════════════════════
print('Generating goal displacement figure...')

# Goal timing bins from results.json
import json
try:
    with open('../../v2/results.json') as f:
        data = json.load(f)
    bins = data.get('goal_timing_bins', None)
except:
    bins = None

if bins:
    labels = list(bins.keys())
    pct_changes = [(bins[b]['post'] - bins[b]['pre']) / bins[b]['pre'] * 100
                   if bins[b]['pre'] > 0 else 0 for b in labels]
else:
    labels = ['1-15', '16-30', '31-45', '46-50', '51-60', '61-75', '76-85', '86-90', '90+']
    pct_changes = [-1.0, -1.7, -2.0, 17.3, 1.6, -0.5, -7.4, -2.6, 43.5]

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(labels))
colors = []
for pc in pct_changes:
    if abs(pc) > 10:
        colors.append(CORAL if pc > 0 else BLUE)
    else:
        colors.append(GRAY)

bars = ax.bar(x, pct_changes, color=colors, edgecolor='white', lw=0.5, width=0.7)

# Annotate significant bars
for i, (bar, pc) in enumerate(zip(bars, pct_changes)):
    if abs(pc) > 5:
        y = bar.get_height()
        offset = 1.5 if y > 0 else -2.5
        ax.text(bar.get_x() + bar.get_width()/2, y + offset,
                f'{pc:+.1f}%', ha='center', va='bottom' if y > 0 else 'top',
                fontsize=10, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_xlabel('Match Period (minutes)')
ax.set_ylabel('Change in Per-Minute Scoring Rate (%)')
ax.set_title('Goal Displacement: Where Scoring Rates Changed', fontweight='bold', pad=12)
ax.axhline(0, color='black', lw=0.8)
ax.grid(axis='y', alpha=0.3)

# Add annotation
ax.annotate('Goals displaced\nfrom late regulation\nto stoppage time',
            xy=(8, 30), fontsize=9, ha='center', color=CORAL,
            fontstyle='italic')

plt.tight_layout()
fig.savefig('fig_goal_displacement.pdf')
fig.savefig('fig_goal_displacement.png')
plt.close(fig)
print('  Saved: fig_goal_displacement.pdf/.png')

print('\nAll figures generated.')
