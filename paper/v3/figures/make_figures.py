#!/usr/bin/env python3
"""
Generate publication-quality figures for FIFA stoppage-time paper (v3).
Outputs 4 PDF figures to /home/aacar/gt/907/paper/v3/figures/
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
import csv
import os
from scipy import stats

# ── Global style ──────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'lines.linewidth': 1.5,
    'patch.linewidth': 0.5,
    'axes.grid': False,
})

OUTDIR = '/home/aacar/gt/907/paper/v3/figures'

# Colors: restrained two-color palette
C_PRE = '#4878A8'   # Steel blue
C_POST = '#D4694A'  # Coral / burnt orange


# ══════════════════════════════════════════════════════════════════════════
# Figure 1: Pre vs Post Stoppage-Time Distributions
# ══════════════════════════════════════════════════════════════════════════
def fig_distributions():
    """Simulate and plot pre/post stoppage-time density curves."""
    # Parameters from data
    pre_mean, pre_sd, pre_n = 4.99, 1.786, 10763
    post_mean, post_sd, post_n = 6.558, 2.243, 4596

    # Generate synthetic samples from gamma distributions
    # (Gamma better matches right-skewed, non-negative stoppage time)
    # Match mean and variance: shape = (mean/sd)^2, scale = sd^2/mean
    np.random.seed(42)
    pre_shape = (pre_mean / pre_sd) ** 2
    pre_scale = pre_sd ** 2 / pre_mean
    post_shape = (post_mean / post_sd) ** 2
    post_scale = post_sd ** 2 / post_mean

    pre_data = np.random.gamma(pre_shape, pre_scale, pre_n)
    post_data = np.random.gamma(post_shape, post_scale, post_n)

    # Clip to reasonable range
    pre_data = np.clip(pre_data, 0, 20)
    post_data = np.clip(post_data, 0, 20)

    # KDE
    x = np.linspace(0, 18, 500)
    pre_kde = stats.gaussian_kde(pre_data, bw_method=0.25)
    post_kde = stats.gaussian_kde(post_data, bw_method=0.25)

    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.fill_between(x, pre_kde(x), alpha=0.25, color=C_PRE)
    ax.plot(x, pre_kde(x), color=C_PRE, lw=1.8,
            label=f'Pre-directive (mean = {pre_mean:.1f} min, $N$ = {pre_n:,})')

    ax.fill_between(x, post_kde(x), alpha=0.25, color=C_POST)
    ax.plot(x, post_kde(x), color=C_POST, lw=1.8,
            label=f'Post-directive (mean = {post_mean:.1f} min, $N$ = {post_n:,})')

    # Threshold markers
    for thresh, y_offset in [(7, 0.02), (10, 0.01)]:
        ax.axvline(thresh, color='#555555', ls='--', lw=0.9, alpha=0.7)

    # Annotate thresholds
    ymax = max(pre_kde(x).max(), post_kde(x).max())
    ax.annotate('7 min\n14.8% $\\rightarrow$ 39.2%',
                xy=(7, ymax * 0.92), fontsize=8.5,
                ha='left', va='top',
                xytext=(7.3, ymax * 0.95))
    ax.annotate('10 min\n1.8% $\\rightarrow$ 7.8%',
                xy=(10, ymax * 0.65), fontsize=8.5,
                ha='left', va='top',
                xytext=(10.3, ymax * 0.68))

    ax.set_xlabel('Second-half stoppage time (minutes)')
    ax.set_ylabel('Density')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, None)
    ax.legend(frameon=False, loc='upper right')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_distributions.pdf'))
    plt.close(fig)
    print('  [OK] fig_distributions.pdf')


# ══════════════════════════════════════════════════════════════════════════
# Figure 2: League-by-League Enforcement Gradient (Cohen's d)
# ══════════════════════════════════════════════════════════════════════════
def fig_time_series():
    """Horizontal dot-plot of Cohen's d by league."""
    # Data from tab_enforcement_intensity.csv (excluding SP2 which has no data)
    leagues = []
    csv_path = '/home/aacar/gt/907/paper/v2/tables/tab_enforcement_intensity.csv'
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Cohen's d"].strip() == '':
                continue
            leagues.append({
                'code': row['league_code'],
                'name': row['League'],
                'd': float(row["Cohen's d"]),
                'intensity': row['Intensity'],
            })

    # Sort by Cohen's d descending
    leagues.sort(key=lambda x: x['d'])

    names = [l['name'] for l in leagues]
    ds = [l['d'] for l in leagues]
    intensities = [l['intensity'] for l in leagues]

    # Big Five treated leagues
    big5_codes = {'E0', 'D1', 'F1', 'SP1', 'I1'}
    is_big5 = [l['code'] in big5_codes for l in leagues]

    fig, ax = plt.subplots(figsize=(7, 4.5))

    y_pos = np.arange(len(leagues))

    for i, (name, d, big5) in enumerate(zip(names, ds, is_big5)):
        color = C_POST if big5 else C_PRE
        marker = 'D' if big5 else 'o'
        ax.plot(d, i, marker=marker, color=color, markersize=8,
                markeredgecolor='white', markeredgewidth=0.5, zorder=3)
        # Horizontal line from 0 to dot
        ax.hlines(i, 0, d, color=color, lw=1.2, alpha=0.5, zorder=2)

    ax.axvline(0, color='#888888', lw=0.8, ls='-', zorder=1)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlabel("Cohen's $d$ (pre- vs. post-directive)")
    ax.set_xlim(-0.2, 1.25)

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='D', color='w', markerfacecolor=C_POST,
               markersize=8, label='Big Five (treated)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=C_PRE,
               markersize=8, label='Other leagues'),
    ]
    ax.legend(handles=legend_elements, frameon=False, loc='lower right',
              fontsize=9.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_time_series.pdf'))
    plt.close(fig)
    print('  [OK] fig_time_series.pdf')


# ══════════════════════════════════════════════════════════════════════════
# Figure 3: Game-Changing Goals (Pre vs Post grouped bars)
# ══════════════════════════════════════════════════════════════════════════
def fig_result_changes():
    """Grouped bar chart of game-changing goal rates."""
    categories = [
        ('Result changed\nin stoppage', 0.07280, 0.10329),
        ('Late\nequalizer', 0.05285, 0.06484),
        ('Late\nwinner', 0.07518, 0.08777),
        ('Game-changing\n85+ min', 0.17910, 0.21445),
    ]

    labels = [c[0] for c in categories]
    pre_vals = [c[1] * 100 for c in categories]
    post_vals = [c[2] * 100 for c in categories]

    x = np.arange(len(categories))
    width = 0.32

    fig, ax = plt.subplots(figsize=(7, 4.5))

    bars_pre = ax.bar(x - width / 2, pre_vals, width, color=C_PRE,
                      label='Pre-directive', edgecolor='white', linewidth=0.5)
    bars_post = ax.bar(x + width / 2, post_vals, width, color=C_POST,
                       label='Post-directive', edgecolor='white', linewidth=0.5)

    # Value labels on bars
    for bar in bars_pre:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
                f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, color='#333333')
    for bar in bars_post:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.3,
                f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, color='#333333')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Share of matches (%)')
    ax.set_ylim(0, max(post_vals) * 1.2)
    ax.legend(frameon=False, loc='upper left')

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_result_changes.pdf'))
    plt.close(fig)
    print('  [OK] fig_result_changes.pdf')


# ══════════════════════════════════════════════════════════════════════════
# Figure 4: Per-Minute Goal Rates by Time Bin
# ══════════════════════════════════════════════════════════════════════════
def fig_goal_timing():
    """Paired bar chart of per-minute scoring rates by time bin."""
    # Data from results_v3_onpitch.json
    bins_data = [
        ('1--15',    0.02707, 0.02694,  -0.49),
        ('16--30',   0.02881, 0.02832,  -1.70),
        ('31--45',   0.02761, 0.02691,  -2.52),
        ('45+',      0.06780, 0.07751, +14.32),
        ('46--60',   0.02536, 0.02615,  +3.13),
        ('61--75',   0.03303, 0.03287,  -0.48),
        ('76--84',   0.03414, 0.03121,  -8.56),
        ('85--89',   0.03286, 0.03196,  -2.73),
        ('90+',      0.03367, 0.04562, +35.52),
    ]

    labels = [b[0] for b in bins_data]
    pre_rates = [b[1] for b in bins_data]
    post_rates = [b[2] for b in bins_data]
    pct_changes = [b[3] for b in bins_data]

    x = np.arange(len(bins_data))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4.5))

    bars_pre = ax.bar(x - width / 2, pre_rates, width, color=C_PRE,
                      label='Pre-directive', edgecolor='white', linewidth=0.5)
    bars_post = ax.bar(x + width / 2, post_rates, width, color=C_POST,
                       label='Post-directive', edgecolor='white', linewidth=0.5)

    # Annotate key changes: 76-84 decline and 90+ surge
    # 76-84 is index 6, 90+ is index 8
    for idx, pct in [(6, pct_changes[6]), (8, pct_changes[8])]:
        bar = bars_post[idx]
        h = bar.get_height()
        sign = '+' if pct > 0 else ''
        fontweight = 'bold'
        ax.annotate(f'{sign}{pct:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8.5, fontweight=fontweight,
                    color='#333333',
                    arrowprops=dict(arrowstyle='-', color='#999999', lw=0.6))

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9.5)
    ax.set_xlabel('Match minute')
    ax.set_ylabel('Goals per minute per match')
    ax.legend(frameon=False, loc='upper left')

    # Format y-axis
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, 'fig_goal_timing.pdf'))
    plt.close(fig)
    print('  [OK] fig_goal_timing.pdf')


# ══════════════════════════════════════════════════════════════════════════
# Run all
# ══════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('Generating figures...')
    fig_distributions()
    fig_time_series()
    fig_result_changes()
    fig_goal_timing()
    print('Done. All figures saved to', OUTDIR)
