import matplotlib.pyplot as plt
import sys
import csv
import pandas as pd
import benchmark


def get_conf_data(result_list):
    return [float(row["conf"]) for row in result_list]


def generate_graphs(results):
    num_rows = len(results)
    fig, axs = plt.subplots(num_rows, 3)
    plt.subplots_adjust(hspace=0.35)

    graphs = ["hit", "miss", "all"]
    all_data = dict()
    for name in graphs:
        all_data[name] = list()

    colors = ["lightgreen", "red"]
    for i, res in enumerate(results):
        hit_miss = [get_conf_data(data) for data in res.hits_misses()]

        axs[i][0].hist(hit_miss[0], bins=10, color=colors[0], range=(0.9, 1.0))
        axs[i][1].hist(hit_miss[1], bins=20, color=colors[1], range=(0.0, 1.0))
        axs[i][2].hist(hit_miss, bins=10, color=colors, range=(0.8, 1.0), stacked=True)

        axs[i][1].set_title(
            f"Class: {res.name} (acc={round(res.accuracy(), 3)}, pres={round(res.precision(), 3)}, n={res.pop})"
        )

    fig.set_figheight(20)
    fig.set_figwidth(10)
    fig.savefig("output/hist.pdf", bbox_inches="tight")


if __name__ == "__main__":
    """Generates PDF histograms of hit and miss confidences.

    Usage: python3 histogram.py output/benchmark.csv
    """
    results, mat = benchmark.load_data(sys.argv[1])
    generate_graphs(results)
    names = [res.name for res in results if res.name != "All"] + [""]
    df = pd.DataFrame(mat, index=names, columns=names)
    print(df)