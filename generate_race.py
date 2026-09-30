import json
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race as bcr

MODE = os.environ.get("RENDER_MODE", "SHORT").upper()
print(f"[Engine] Mode: {MODE}")

BG_DARK = '#0a0d14'

if MODE == "LONG":
    FIGSIZE = (16, 9)
    DPI = 120
    N_BARS = 10
    TITLE_SIZE = 20
    STEPS = 20
    PERIOD_LENGTH = 1800
    OUTPUT_FILE = "output_long.mp4"
    timeline = pd.date_range(start='2020-01-01', end='2026-12-01', freq='MS').strftime('%b %Y')
else:
    FIGSIZE = (6.75, 12)  # 9:16 vertical
    DPI = 144
    N_BARS = 8
    TITLE_SIZE = 14
    STEPS = 25
    PERIOD_LENGTH = 1200
    OUTPUT_FILE = "output_short.mp4"
    timeline = pd.date_range(start='2020-01-01', end='2026-10-01', freq='2MS').strftime('%b %Y')

# Load Data
with open('topics.json', 'r') as f:
    topics_list = json.load(f)

active_topic = topics_list[0]
entities = active_topic['entities']

np.random.seed(random.randint(1, 99999))
base_scores = np.sort(np.random.randint(310, 390, size=len(entities)))
data_matrix = []

for _ in timeline:
    shifts = np.random.normal(loc=1.5, scale=2.8, size=len(entities))
    base_scores = np.maximum(base_scores, base_scores + np.clip(shifts, 0, 7.5))
    data_matrix.append(base_scores.copy())

df = pd.DataFrame(data_matrix, index=timeline, columns=entities)
df.index.name = 'Date'

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
fig.set_facecolor(BG_DARK)
ax.set_facecolor(BG_DARK)

# Spines aur border hataye
for s in ax.spines.values():
    s.set_visible(False)

ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.tick_params(left=False, bottom=False, labelsize=10, colors='#e2e8f0')

bcr.bar_chart_race(
    df=df,
    filename=OUTPUT_FILE,
    fig=fig,
    n_bars=N_BARS,
    steps_per_period=STEPS,
    period_length=PERIOD_LENGTH,
    title={
        'label': f"{active_topic['topic'].upper()}\n",
        'color': '#ffffff',
        'size': TITLE_SIZE,
        'weight': 'bold'
    },
    bar_kwargs={'alpha': 0.9, 'lw': 0},
    cmap='plasma',
    period_label={
        'x': 0.88, 'y': 0.08, 'ha': 'right', 'va': 'bottom',
        'size': 20, 'weight': 'bold', 'color': '#38bdf8'
    },
    bar_label_font={'color': '#ffffff', 'size': 10, 'weight': 'bold'},
    tick_label_font={'color': '#ffffff', 'size': 11, 'weight': 'bold'},
    shared_fontdict={'family': 'sans-serif'},
    filter_column_colors=True
)

print(f"[Done] Rendered to {OUTPUT_FILE}")
