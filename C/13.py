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
    ("EAS", "velocidade ar equivalente - kn"),
    ("QNE", "altitude barometrica - ft"),
    ("a_z", "aceleracao vertical - m/s^2"),
    ("N2_rh", "velocidade de rotacao N2 do motor direito - %"),
    ("EGT_rh", "temperatura dos gases de escape do motor direito - K"),
    ("FF_rh", "consumo de combustivel do motor direito - kg/h"),
    ("N2_lt", "velocidade de rotacao N2 do motor esquerdo - %"),
    ("EGT_lt", "temperatura dos gases de escape do motor esquerdo - K"),
    ("FF_lt", "consumo de combustivel do motor esquerdo - kg/h"),
]

for column, ylabel in plots:
    make_plot(t, df[column], column, ylabel)

plt.show()
