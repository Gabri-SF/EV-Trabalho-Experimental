from pathlib import Path

import pandas as pd


DATA_FILE = Path(__file__).with_name("EV_2026.C24_g_values.csv")
OUTPUT_FILE = Path(__file__).with_name("ciclos_az.csv")

N_PAIRS = [
    (2.5, 2.2),
    (4, 3.7),
    (5.0, 4.7),
    (6.0, 5.7),
    (7.0, 6.7),
    (0.0, 0.3),
    (-1.5, -1.2),
    (-2.5, -2.2),
]


def contar_ciclos(dados_df, n1, n2):
    if n1 > 1.0 and n2 >= n1:
        raise ValueError("Para N1 > 1 g, N2 deve ser inferior a N1.")
    if n1 < 1.0 and n2 <= n1:
        raise ValueError("Para N1 < 1 g, N2 deve ser superior a N1.")
    if n1 == 1.0:
        raise ValueError("O algoritmo precisa de N1 diferente de 1 g.")

    em_ciclo = False
    inicio = None
    ciclos = []

    for linha in dados_df.itertuples(index=False):
        t = linha.t
        a_z_g = linha.a_z_g

        if n1 > 1.0:
            inicia = a_z_g > n1
            fecha = a_z_g < n2
        else:
            inicia = a_z_g < n1
            fecha = a_z_g > n2

        if not em_ciclo and inicia:
            em_ciclo = True
            inicio = (t, a_z_g)
            continue

        if em_ciclo and fecha:
            ciclos.append(
                {
                    "N1": n1,
                    "N2": n2,
                    "t_inicio_amostra": inicio[0],
                    "a_z_g_inicio_amostra": inicio[1],
                    "t_fim_amostra": t,
                    "a_z_g_fim_amostra": a_z_g,
                }
            )
            em_ciclo = False
            inicio = None

    return ciclos


df = pd.read_csv(DATA_FILE, sep=";")

colunas_necessarias = {"t", "a_z_g"}
colunas_em_falta = colunas_necessarias - set(df.columns)

if colunas_em_falta:
    raise ValueError(f"Faltam colunas no ficheiro: {sorted(colunas_em_falta)}")

for coluna in colunas_necessarias:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df = df.dropna(subset=colunas_necessarias).sort_values("t").reset_index(drop=True)

todos_os_ciclos = []

for n1, n2 in N_PAIRS:
    ciclos = contar_ciclos(df, n1, n2)
    todos_os_ciclos.extend(ciclos)
    print(f"N1 = {n1:4.1f} g, N2 = {n2:4.1f} g: {len(ciclos)} ciclo(s)")

pd.DataFrame(todos_os_ciclos).to_csv(OUTPUT_FILE, sep=";", index=False)
print(f"\nResultados guardados em: {OUTPUT_FILE.name}")
