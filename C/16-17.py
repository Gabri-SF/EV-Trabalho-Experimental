from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path(__file__).with_name("EV_2026.C24_g_values")
OUTPUT_FILE = Path(__file__).with_name("ciclos_a_z_g")
PLOT_FILE = Path(__file__).with_name("ciclos_a_z_g.png")

N_PAIRS = {
    (2.5, 2.2): "red",
    (4, 3.7): "orange",
    (5.0, 4.7): "blue",
    (6.0, 5.7): "brown",
    (7.0, 6.7): "grey",
    (0.0, 0.3): "purple",
    (-1.5, -1.2): "cyan",
    (-2.5, -2.2): "pink",
}


T_MIN = 0
T_MAX = 4400


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
ciclos_por_par = {}

for n1, n2 in N_PAIRS:
    ciclos = contar_ciclos(df, n1, n2)
    ciclos_por_par[(n1, n2)] = ciclos
    todos_os_ciclos.extend(ciclos)
    print(f"N1 = {n1:4.1f} g, N2 = {n2:4.1f} g: {len(ciclos)} ciclo(s)")

pd.DataFrame(todos_os_ciclos).to_csv(OUTPUT_FILE, sep=";", index=False)
print(f"\nResultados guardados em: {OUTPUT_FILE.name}")

df_plot = df.copy()

if T_MIN is not None:
    df_plot = df_plot[df_plot["t"] >= T_MIN]
if T_MAX is not None:
    df_plot = df_plot[df_plot["t"] <= T_MAX]

if df_plot.empty:
    raise ValueError("O intervalo definido por T_MIN/T_MAX nao contem dados.")

t_min_plot = df_plot["t"].min()
t_max_plot = df_plot["t"].max()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(df_plot["t"], df_plot["a_z_g"], color="g", linewidth=1)
ax.axhline(1.0, color="black", linestyle="--", linewidth=1, label="1 g")

for (n1, n2), ciclos in ciclos_por_par.items():
    cor = N_PAIRS[(n1, n2)]
    ciclos_visiveis = [
        ciclo
        for ciclo in ciclos
        if t_min_plot <= ciclo["t_inicio_amostra"] <= t_max_plot
        and t_min_plot <= ciclo["t_fim_amostra"] <= t_max_plot
    ]

    print(
        f"N1 = {n1:4.1f} g, N2 = {n2:4.1f} g: "
        f"{len(ciclos_visiveis)} ciclo(s)"
    )

    if not ciclos_visiveis:
        continue

    ax.axhline(n1, color=cor, linestyle="--", linewidth=0.8, alpha=0.25)
    ax.axhline(n2, color=cor, linestyle=":", linewidth=0.8, alpha=0.25)

    inicios_t = [ciclo["t_inicio_amostra"] for ciclo in ciclos_visiveis]
    inicios_a_z = [ciclo["a_z_g_inicio_amostra"] for ciclo in ciclos_visiveis]
    fins_t = [ciclo["t_fim_amostra"] for ciclo in ciclos_visiveis]
    fins_a_z = [ciclo["a_z_g_fim_amostra"] for ciclo in ciclos_visiveis]

    ax.scatter(
        inicios_t,
        inicios_a_z,
        color=cor,
        s=18,
        zorder=3,
        label=f"N1={n1:g}, N2={n2:g}",
    )
    ax.scatter(fins_t, fins_a_z, facecolors="white", edgecolors=cor, s=18, zorder=3)

    for ciclo in ciclos_visiveis:
        ax.annotate(
            "",
            xy=(ciclo["t_fim_amostra"], ciclo["a_z_g_fim_amostra"]),
            xytext=(ciclo["t_inicio_amostra"], ciclo["a_z_g_inicio_amostra"]),
            arrowprops={"arrowstyle": "->", "color": cor, "lw": 0.8, "alpha": 0.8},
        )

ax.set_title("Ciclos de aceleração vertical")
ax.set_xlabel("t [s]")
ax.set_ylabel("a_z [g]")
ax.grid(True)
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig(PLOT_FILE, dpi=200)
print(f"Grafico guardado em: {PLOT_FILE.name}")
plt.show()
