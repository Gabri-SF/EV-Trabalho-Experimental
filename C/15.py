from pathlib import Path

import pandas as pd

DATA_FILE = Path(__file__).with_name("EV_2026.C24_g_values.csv")
OUTPUT_FILE = Path(__file__).with_name("picos_vales.csv")

#limtes para ignorar pequenas oscilações da aeronava
LIMITE_PICO = 1.1
LIMITE_VALE = 0.9

# Ler dados
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

a_z_g = df["a_z_g"]

maximos_locais = (a_z_g > a_z_g.shift(1)) & (a_z_g > a_z_g.shift(-1))
minimos_locais = (a_z_g < a_z_g.shift(1)) & (a_z_g < a_z_g.shift(-1))

picos = maximos_locais & (a_z_g > LIMITE_PICO)
vales = minimos_locais & (a_z_g < LIMITE_VALE)

df["tipo"] = ""
df.loc[picos, "tipo"] = "pico"
df.loc[vales, "tipo"] = "vale"

# Guardar apenas os extremos locais relevantes. Os limites so filtram ruido.
picos_vales = df.loc[picos | vales, ["tipo", "t", "a_z", "a_z_g"]]

picos_vales.to_csv(OUTPUT_FILE, sep=";", index=False)


# Resumo
numero_picos = (picos_vales["tipo"] == "pico").sum()
numero_vales = (picos_vales["tipo"] == "vale").sum()

print(f"Picos da trajetoria encontrados: {numero_picos}")
print(f"Vales da trajetoria encontrados: {numero_vales}")
print(f"Total de eventos encontrados: {len(picos_vales)}")
print(f"Resultados guardados em: {OUTPUT_FILE.name}")
