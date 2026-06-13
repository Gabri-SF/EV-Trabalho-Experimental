from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path(__file__).with_name("EV_2026.C24")
CSV_OUTPUT_FILE = DATA_FILE.with_name("EV_2026.C24_g_values")
GRAPH_OUTPUT_FILE = DATA_FILE.with_name("EV_2026.C24_g_values.png")

G_0 = 9.80665  # m/s^2

df = pd.read_csv(DATA_FILE, sep=";")

required_columns = {"t", "a_z"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing columns in {DATA_FILE.name}: {sorted(missing_columns)}")

for column in required_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=required_columns).sort_values("t").reset_index(drop=True)
df["a_z_g"] = df["a_z"] / G_0

g_values = df[["t", "a_z", "a_z_g"]]
g_values.to_csv(CSV_OUTPUT_FILE, sep=";", index=False)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(g_values["t"], g_values["a_z_g"], color="green", linewidth=1)
ax.axhline(1.0, color="black", linestyle="--", linewidth=1, label="1 g")
ax.set_title("Variação temporal da aceleração vertical")
ax.set_xlabel("t [s]")
ax.set_ylabel("a_z [g]")
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()
fig.savefig(GRAPH_OUTPUT_FILE, dpi=300)

print(g_values.to_string(index=False))
print(f"\nCalculated {len(g_values)} g values.")
print(f"Saved results to {CSV_OUTPUT_FILE.name}.")
print(f"Saved graph to {GRAPH_OUTPUT_FILE.name}.")

plt.show()
