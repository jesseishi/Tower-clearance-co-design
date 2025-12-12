import matplotlib.pyplot as plt
import numpy as np

# Plot settings
text_width_in = 455.24408 / 64
default_fig_width = 0.8 * text_width_in
default_aspect_ratio = 1 / (0.5 * (1 + np.sqrt(5)))

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Latin Modern Roman"],
        "font.size": 10,
        "text.usetex": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "figure.figsize": [default_fig_width, default_fig_width * default_aspect_ratio],
        "image.cmap": "cmc.batlow",
    }
)