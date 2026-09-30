import json
import random
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bar_chart_race as bcr

# 0. Format Selection via Environment Variable (Default: LONG)
MODE = os.environ.get("RENDER_MODE", "LONG").upper()
print(f"[Engine] Selected Mode: {MODE}")

# 1. Visual Permutations (Unique styling per run)
PALETTES = [
    'dark12', 'spectral', 'tab20b', 'tab20c', 
    'plasma', 'viridis', 'magma', 'inferno', 'mako', 'rocket'
]

BG_COLORS = [
    '#0b0f19', '#111827', '#09090b', '#022c22', 
    '#1e1b4b', '#172554', '#1f1305', '#170b21'
]

FONTS = ['DejaVu Sans', 'sans-serif', 'Liberation Sans', 'Ubuntu']
BAR_OPACITIES = [0.85, 0.9, 0.95, 1.0]

chosen_palette = random.choice(PALETTES)
chosen_bg = random.choice(BG_COLORS)
chosen_font = random.choice(FONTS)
chosen_alpha = random.choice(BAR_OPACITIES)

# 2. Ratio & Speed Settings
if MODE == "LONG":
    FIGSIZE = (16, 9)
    DPI = 120
    N_BARS = 10
    TITLE_SIZE = 22
    PERIOD_LABEL_SIZE = 34
    PERIOD_LABEL_POS = {'x': 0.95, 'y': 0.15, 'ha': 'right', 'va': 'center'}
    STEPS_PER_PERIOD = 24
    PERIOD_LENGTH = 2000
    OUTPUT_FILE = "output_long.mp4"
else:  # SHORT (Under 60 seconds)
    FIGSIZE = (5.06, 9)
    DPI = 144
    N_BARS = 7
    TITLE_SIZE = 14
    PERIOD_LABEL_SIZE = 20
    PERIOD_LABEL_POS = {'x': 0.85, 'y': 0.12, 'ha': 'right', 'va': 'center'}
    STEPS_PER_PERIOD = 20
    PERIOD_LENGTH = 1500
    OUTPUT_FILE = "output_short.mp4"

print(f"[Engine] Visual Configuration: BG={chosen_bg}, Palette={chosen_palette}, Dimensions={FIGSIZE}")

# 3. Load Topic & Generate Dynamic Timeline Data
with open('topics.json', 'r') as f:
    topics_list = json.load(f)

active_topic = topics_list[0]
entities = active_topic['entities']

if MODE == "LONG":
    # 2020 to 2026 Monthly sequence (~3 to 4 mins)
    timeline = pd.date_range(start='2020-01-01', end='2026-12-01', freq='MS').strftime('%b %Y')
else:
    # 2020 to 2026 Quarterly sequence (~45 to 50 secs)
    timeline = pd.date_range(start='2020-01-01', end='2026-10-01', freq='QS').strftime('%b %Y')

np.random.seed(random.randint(1, 99999))
base_scores = np.sort(np.random.randint(310, 420, size=len(entities)))
data_matrix = []

for _ in timeline:
    shifts = np.random.normal(loc=1.2, scale=2.5, size=len(entities))
    base_scores = np.maximum(base_scores, base_scores + np.clip(shifts, 0, 8))
    data_matrix.append(base_scores.copy())

df = pd.DataFrame(data_matrix, index=timeline, columns=entities)
df.index.name = 'Date'

# 4. Matplotlib Setup
plt.rcParams['font.family'] = chosen_font
plt.rcParams['text.color'] = '#ffffff'
plt.rcParams['axes.labelcolor'] = '#ffffff'
plt.rcParams['xtick.color'] = '#ffffff'
plt.rcParams['ytick.color'] = '#ffffff'

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
fig.set_facecolor(chosen_bg)
ax.set_facecolor(chosen_bg)

# 5. Render Video (fig pass kiya hai direct)
bcr.bar_chart_race(
    df=df,
    filename=OUTPUT_FILE,
    fig=fig,
    n_bars=N_BARS,
    steps_per_period=STEPS_PER_PERIOD,
    period_length=PERIOD_LENGTH,
    title={
        'label': f"{active_topic['topic']}\n", 
        'color': '#ffffff', 
        'size': TITLE_SIZE, 
        'weight': 'bold'
    },
    bar_kwargs={'alpha': chosen_alpha, 'lw': 0},
    cmap=chosen_palette,
    period_label={
        **PERIOD_LABEL_POS, 
        'size': PERIOD_LABEL_SIZE, 
        'weight': 'bold', 
        'color': '#f59e0b'
    },
    shared_fontdict={'family': chosen_font, 'color': '#ffffff'},
    filter_column_colors=True
)

print(f"[Done] Rendered {MODE} video to {OUTPUT_FILE}")
