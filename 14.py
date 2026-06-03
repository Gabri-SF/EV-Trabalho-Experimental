# Import the necessary modules
from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).with_name("EV_2026.C24")

g_0 = 9.80665  # m/s^2

df = pd.read_csv(DATA_FILE, sep=";")

df["a_z_g"] = df["a_z"] / g_0

g_values = df[["t", "a_z", "a_z_g"]]
output_file = DATA_FILE.with_name("EV_2026.C24_g_values.csv")

g_values.to_csv(output_file, sep=";", index=False)

print(g_values.to_string(index=False))
print(f"\nCalculated {len(g_values)} g values.")
print(f"Saved results to {output_file.name}.")
