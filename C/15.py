from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

DATA_FILE = Path(__file__).with_name("EV_2026.C24_g_values")
OUTPUT_FILE = Path(__file__).with_name("maximos_minimos")
PLOT_FILE = Path(__file__).with_name("maximos_minimos.png")

df = pd.read_csv(DATA_FILE, sep=";")

colunas_necessarias = {"t", "a_z", "a_z_g"}
colunas_em_falta = colunas_necessarias - set(df.columns)

if colunas_em_falta:
    raise ValueError(
        f"Faltam as seguintes colunas no ficheiro: {sorted(colunas_em_falta)}"
    )

for coluna in colunas_necessarias:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df = df.dropna(subset=colunas_necessarias).reset_index(drop=True)

valores_a_z_g = df["a_z_g"].to_numpy()

indices_maximos, _ = find_peaks(valores_a_z_g, plateau_size=(None, 1))
indices_minimos, _ = find_peaks(-valores_a_z_g, plateau_size=(None, 1))

df["tipo"] = ""
df.loc[indices_maximos, "tipo"] = "max"
df.loc[indices_minimos, "tipo"] = "min"

maximos_minimos = df.loc[df["tipo"] != "", ["tipo", "t", "a_z", "a_z_g"]]

maximos_minimos.to_csv(OUTPUT_FILE, sep=";", index=False)

dados_maximos = df.loc[indices_maximos]
dados_minimos = df.loc[indices_minimos]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    df["t"],
    df["a_z_g"],
    color="green",
    linewidth=0.9,
    label="Aceleracao vertical",
)
ax.axhline(1.0, color="black", linestyle="--", linewidth=1, label="1 g")
ax.scatter(
    dados_maximos["t"],
    dados_maximos["a_z_g"],
    color="red",
    marker="^",
    s=24,
    zorder=3,
    label=f"maximos ({len(dados_maximos)})",
)
ax.scatter(
    dados_minimos["t"],
    dados_minimos["a_z_g"],
    color="blue",
    marker="v",
    s=24,
    zorder=3,
    label=f"minimos ({len(dados_minimos)})",
)

ax.set_title("Variação temporal dos extremos da aceleração vertical")
ax.set_xlabel("t [s]")
ax.set_ylabel("a_z [g]")
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig(PLOT_FILE, dpi=200)

numero_maximos = (maximos_minimos["tipo"] == "max").sum()
numero_minimos = (maximos_minimos["tipo"] == "min").sum()

print(f"maximos da trajetoria encontrados: {numero_maximos}")
print(f"minimos da trajetoria encontrados: {numero_minimos}")
print(f"Total de eventos encontrados: {len(maximos_minimos)}")
print(f"Resultados guardados em: {OUTPUT_FILE.name}")
print(f"Grafico guardado em: {PLOT_FILE.name}")

plt.show()
