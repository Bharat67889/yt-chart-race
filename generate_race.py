import json
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race as bcr

MODE = os.environ.get("RENDER_MODE", "LONG").upper()
print(f"[Engine] Mode: {MODE}")

# Modern Sleek Palettes (No dull 90s default colors)
MODERN_PALETTES = [
    ['#38bdf8', '#818cf8', '#c084fc', '#f472b6', '#fb7185', '#34d399', '#fbbf24', '#a78bfa', '#4ade80', '#2dd4bf'],
    ['#00f2fe', '#4facfe', '#43e97b', '#38f9d7', '#fa709a', '#fee140', '#30cfd0', '#330867', '#a8edea', '#fed6e3'],
    ['#f12711', '#f5af19', '#11998e', '#38ef7d', '#8e2de2', '#4a00e0', '#ff0084', '#33001b', '#00c6ff', '#0072ff']
]

BG_DARK = '#0a0d14'
chosen_colors = random.choice(MODERN_PALETTES)

if MODE == "LONG":
    FIGSIZE = (16, 9)
    DPI = 120
    N_BARS = 10
    TITLE_SIZE = 22
    PERIOD_SIZE = 36
    FPS = 30
    PERIOD_LENGTH = 1800
    STEPS = 20
    LEFT_MARGIN = 0.22
    OUTPUT_FILE = "output_long.mp4"
    timeline = pd.date_range(start='2020-01-01', end='2026-12-01', freq='MS').strftime('%b %Y')
else:
    # 9:16 Vertical for Shorts
    FIGSIZE = (7.2, 12.8)
    DPI = 150
    N_BARS = 7
    TITLE_SIZE = 16
    PERIOD_SIZE = 24
    FPS = 60  # Ultra smooth 60 FPS
    PERIOD_LENGTH = 1400
    STEPS = 24
    LEFT_MARGIN = 0.38  # Name cut hone se rokne ke liye left padding
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

# Setup Clean Figure
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
fig.set_facecolor(BG_DARK)
ax.set_facecolor(BG_DARK)

# Margins adjust karein taaki naam screen se bahar na jayein
fig.subplots_adjust(left=LEFT_MARGIN, right=0.92, top=0.88, bottom=0.12)

# Remove 90s border lines (spines)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.tick_params(left=False, bottom=False)

# Render Race
bcr.bar_chart_race(
    df=df,
    filename=OUTPUT_FILE,
    fig=fig,
    n_bars=N_BARS,
    steps_per_period=STEPS,
    period_length=PERIOD_LENGTH,
    title={
        'label': f"{active_topic['topic'].upper()}",
        'color': '#ffffff',
        'size': TITLE_SIZE,
        'weight': 'bold',
        'pad': 20
    },
    bar_kwargs={'alpha': 0.95, 'lw': 0},
    colors=chosen_colors,
    period_label={
        'x': 0.92, 'y': 0.04, 'ha': 'right', 'va': 'bottom',
        'size': PERIOD_SIZE, 'weight': 'heavy', 'color': '#38bdf8'
    },
    bar_label_font={'color': '#ffffff', 'size': 11, 'weight': 'bold'},
    tick_label_font={'color': '#e2e8f0', 'size': 12, 'weight': 'bold'},
    shared_fontdict={'family': 'sans-serif'},
    filter_column_colors=True
)

print(f"[Engine] Render complete: {OUTPUT_FILE}")
