# Import the necessary modules
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path(__file__).with_name("EV_2026.C24")


def make_plot(t, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, y, color="g")
    ax.set_title(title)
    ax.set_xlabel("tempo - s")
    ax.set_ylabel(ylabel)
    ax.grid(True)
    fig.tight_layout()


df = pd.read_csv(DATA_FILE, sep=";")

t = df["t"]

plots = [
    ("EAS", "EAS - kn", "Variação temporal da EAS"),
    ("QNE", "QNE - ft", "Variação temporal da QNE"),
    ("a_z", "a_z - m/s^2", "Variação temporal da a_z"),
    ("N2_rh", "N2_rh - %", "Variação temporal da N2_rh"),
    ("EGT_rh", "EGT_rh - K", "Variação temporal da EGT_rh"),
    ("FF_rh", "FF_rh - kg/h", "Variação temporal da FF_rh"),
    ("N2_lt", "N2_lt - %", "Variação temporal da N2_lt"),
    ("EGT_lt", "EGT_lt - K", "Variação temporal da EGT_lt"),
    ("FF_lt", "FF_lt - kg/h", "Variação temporal da FF_lt"),
]

for column, ylabel, title in plots:
    make_plot(t, df[column], title, ylabel)

plt.show()
