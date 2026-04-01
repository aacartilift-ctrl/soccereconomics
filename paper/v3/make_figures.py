"""
Create two new figures for the v3 soccer sections.
Reuses v2 figures for distributions, goal_timing, time_series.
"""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── Style ──────────────────────────────────────────────────────
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'serif',
})

BLUE = '#4878A8'
CORAL = '#E07060'
GRAY = '#999999'

# ═══════════════════════════════════════════════════════════════
#  FIGURE 1: Enforcement Gradient (dot plot)
# ═══════════════════════════════════════════════════════════════

with open('../v2/results.json') as f:
    data = json.load(f)

enforcement = data['enforcement']

# League labels and metadata
league_labels = {
    'E0': 'Premier League',
    'F1': 'Ligue 1',
    'D1': 'Bundesliga',
    'SC0': 'Scottish Prem.',
    'SP1': 'La Liga',
    'B1': 'Belgian Pro League',
    'E1': 'Championship',
    'D2': '2. Bundesliga',
    'P1': 'Primeira Liga',
    'F2': 'Ligue 2',
    'G1': 'Greek Super League',
    'I1': 'Serie A',
    'N1': 'Eredivisie',
    'I2': 'Serie B',
}

big_five = {'E0', 'F1', 'D1', 'SP1', 'I1'}

# Build sorted list (exclude SP2 — no post data)
leagues = []
for code, vals in enforcement.items():
    if code == 'SP2' or vals['cohens_d'] is None or np.isnan(vals['cohens_d']):
        continue
    leagues.append({
        'code': code,
        'label': league_labels.get(code, code),
        'd': vals['cohens_d'],
        'diff': vals['diff'],
        'treated': code in big_five,
    })

leagues.sort(key=lambda x: x['d'])  # ascending so top of plot = highest

fig, ax = plt.subplots(figsize=(7, 5.5))

y_pos = np.arange(len(leagues))
colors = [CORAL if l['treated'] else BLUE for l in leagues]

ax.barh(y_pos, [l['d'] for l in leagues], color=colors, height=0.65,
        edgecolor='white', linewidth=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels([l['label'] for l in leagues])
ax.set_xlabel("Cohen's $d$")
ax.axvline(x=0, color='black', linewidth=0.5, linestyle='-')

# Add diff annotation on the right
for i, l in enumerate(leagues):
    sign = '+' if l['diff'] > 0 else ''
    ax.text(max(l['d'] + 0.03, 0.05), i, f"{sign}{l['diff']:.2f} min",
            va='center', fontsize=8.5, color='#444444')

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=CORAL, label='Big Five (treated)'),
    Patch(facecolor=BLUE, label='Other leagues (control)'),
]
ax.legend(handles=legend_elements, loc='lower right', frameon=True,
          edgecolor='#cccccc', fancybox=False)

ax.set_xlim(-0.15, 1.45)
plt.tight_layout()
fig.savefig('figures/fig_enforcement_gradient.pdf')
fig.savefig('figures/fig_enforcement_gradient.png')
plt.close()
print("✓ fig_enforcement_gradient")


# ═══════════════════════════════════════════════════════════════
#  FIGURE 2: Game-Changing Goals (grouped bars)
# ═══════════════════════════════════════════════════════════════

with open('../v2/results_v3_onpitch.json') as f:
    onpitch = json.load(f)

gc = onpitch['game_changing_goals']

categories = [
    ('Result changed\nin stoppage', gc['result_changed_in_stoppage']),
    ('Late\nequalizer', gc['late_equalizer']),
    ('Late\nwinner', gc['late_winner']),
    ('Game-changing\ngoal 85+', gc['game_changing_85plus']),
]

fig, ax = plt.subplots(figsize=(7, 4.5))

x = np.arange(len(categories))
width = 0.35

pre_vals = [c[1]['pre_mean'] * 100 for c in categories]
post_vals = [c[1]['post_mean'] * 100 for c in categories]
labels = [c[0] for c in categories]

bars1 = ax.bar(x - width/2, pre_vals, width, label='Pre-directive',
               color=BLUE, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, post_vals, width, label='Post-directive',
               color=CORAL, edgecolor='white', linewidth=0.5)

# Add value labels on bars
for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.3,
            f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, color='#444444')
for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., h + 0.3,
            f'{h:.1f}%', ha='center', va='bottom', fontsize=8.5, color='#444444')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=9.5)
ax.set_ylabel('Share of matches (%)')
ax.legend(frameon=True, edgecolor='#cccccc', fancybox=False)
ax.set_ylim(0, max(post_vals) * 1.2)

plt.tight_layout()
fig.savefig('figures/fig_game_changing.pdf')
fig.savefig('figures/fig_game_changing.png')
plt.close()
print("✓ fig_game_changing")

print("\nDone. Two new figures in figures/")
