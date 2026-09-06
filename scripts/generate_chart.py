import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#0f172a", "figure.facecolor": "#0f172a", "grid.color": "#334155"})

labels = ['5-Priority Heuristic', 'No-Gust Variant', 'Greedy Baseline']
win_rates = [40.9, 41.2, 59.1]
colors = ['#f43f5e', '#8b5cf6', '#38bdf8']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, win_rates, color=colors, width=0.6, edgecolor='white', linewidth=1.5)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval}%', ha='center', va='bottom', fontsize=14, fontweight='bold', color='white')

ax.set_ylim(0, 70)
ax.set_ylabel('Win Rate (%)', fontsize=14, fontweight='bold', color='#cbd5e1')
ax.set_title('A/B Batch Results: Tempo Dominance (1,000 Games)', fontsize=18, fontweight='bold', color='white', pad=20)
ax.tick_params(axis='x', labelsize=13, colors='#cbd5e1')
ax.tick_params(axis='y', labelsize=12, colors='#cbd5e1')

ax.annotate('Optimal Strategy (+18.2% EV)', xy=(2, 59.1), xytext=(1.0, 65),
            arrowprops=dict(facecolor='#38bdf8', shrink=0.05, width=2, headwidth=8),
            fontsize=12, fontweight='bold', color='#38bdf8',
            bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec="#38bdf8", lw=2))

plt.tight_layout()
plt.savefig('public/winrate_chart.png', dpi=300, bbox_inches='tight', transparent=True)
print('Chart generated successfully.')
