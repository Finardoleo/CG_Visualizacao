"""Visualize the relationship between income and life expectancy, 1952–2007.

Data: https://github.com/jennybc/gapminder (CC0), an excerpt from
https://www.gapminder.org/data/.
"""

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "gapminder.tsv"
YEARS = (1952, 2007)
CONTINENT_COLORS = {
    "Africa": "#D55E00",
    "Americas": "#0072B2",
    "Asia": "#009E73",
    "Europe": "#CC79A7",
    "Oceania": "#E69F00",
}


def load_endpoints():
    endpoints = {year: {} for year in YEARS}
    with DATA_FILE.open(encoding="utf-8", newline="") as dataset:
        rows = csv.DictReader(dataset, delimiter="\t")
        for row in rows:
            year = int(row["year"])
            if year in endpoints:
                endpoints[year][row["country"]] = {
                    "continent": row["continent"],
                    "life_expectancy": float(row["lifeExp"]),
                    "gdp_per_capita": float(row["gdpPercap"]),
                }

    countries = endpoints[YEARS[0]].keys() & endpoints[YEARS[1]].keys()
    if not countries:
        raise ValueError(f"No countries have data for both {YEARS[0]} and {YEARS[1]}.")
    return endpoints, sorted(countries)


def create_visualization(output_path):
    endpoints, countries = load_endpoints()
    start, end = (endpoints[year] for year in YEARS)

    fig, ax = plt.subplots(figsize=(11, 7), constrained_layout=True)
    fig.patch.set_facecolor("#FBFCFE")
    ax.set_facecolor("#FBFCFE")

    for country in countries:
        first = start[country]
        last = end[country]
        ax.plot(
            [first["gdp_per_capita"], last["gdp_per_capita"]],
            [first["life_expectancy"], last["life_expectancy"]],
            color=CONTINENT_COLORS[last["continent"]],
            alpha=0.5,
            linewidth=0.8,
            zorder=1,
        )

    ax.scatter(
        [start[country]["gdp_per_capita"] for country in countries],
        [start[country]["life_expectancy"] for country in countries],
        s=22,
        facecolors="#FBFCFE",
        edgecolors=[CONTINENT_COLORS[end[country]["continent"]] for country in countries],
        linewidths=1.1,
        label=str(YEARS[0]),
        zorder=2,
    )

    for continent, color in CONTINENT_COLORS.items():
        subset = [country for country in countries if end[country]["continent"] == continent]
        if not subset:
            continue
        ax.scatter(
            [end[country]["gdp_per_capita"] for country in subset],
            [end[country]["life_expectancy"] for country in subset],
            s=30,
            color=color,
            edgecolors="white",
            linewidths=0.5,
            label=continent,
            zorder=3,
        )

    ax.set_xscale("log")
    ax.set_xlabel(
        "PIB per capita (US$, escala logarítmica)", fontsize=11, labelpad=10
    )
    ax.set_ylabel("Expectativa de vida ao nascer (anos)", fontsize=11, labelpad=10)
    ax.set_title(
        "Análise entre renda e longevidade por país em cada continente (1952-2007)",
        loc="left",
        fontsize=17,
        fontweight="bold",
        pad=14,
    )
    ax.grid(True, which="major", color="#DCE2E8", linewidth=0.8)
    ax.grid(True, which="minor", axis="x", color="#E9EDF1", linewidth=0.5)
    ax.tick_params(colors="#526170")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#AAB4BF")
    ax.spines["bottom"].set_color("#AAB4BF")

    legend_handles = [
        Line2D(
            [],
            [],
            marker="o",
            linestyle="none",
            markerfacecolor="#FBFCFE",
            markeredgecolor="#526170",
            markersize=6,
        ),
    ]
    legend_labels = [f"{YEARS[0]} (círculo vazio)"]
    for continent, color in CONTINENT_COLORS.items():
        legend_handles.append(
            Line2D(
                [],
                [],
                marker="o",
                linestyle="none",
                markerfacecolor=color,
                markeredgecolor="white",
                markersize=6,
            )
        )
        legend_labels.append(continent)

    ax.legend(
        legend_handles,
        legend_labels,
        title=f"{YEARS[0]} (círculo vazio); {YEARS[1]} por continente",
        frameon=False,
        loc="lower right",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    return len(countries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "visualizacao_gapminder.png",
        help="caminho do arquivo de imagem a gerar",
    )
    args = parser.parse_args()
    country_count = create_visualization(args.output)
    print(f"Visualização gerada para {country_count} países: {args.output}")


if __name__ == "__main__":
    main()
