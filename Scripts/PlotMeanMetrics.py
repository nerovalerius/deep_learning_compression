import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    df = pd.read_csv("./tmp/last_run_metrics.csv", index_col=0)
    df.head()

    if not os.path.exists("./tmp/last_run_metrics_plots"):
        os.makedirs("./tmp/last_run_metrics_plots")

    metrics = json.loads(df.iloc[0]["Metrics"].replace("'", '"'))
    metrics = list(metrics.keys())
    metrics

    compression_methods = df["CompressionMethod"].unique()

    metric_means = {}
    metric_means.update({m: {} for m in metrics})
    for k in metrics:
        for cm in compression_methods:
            metric_means[k].update(
                {cm: np.mean(df.loc[df["CompressionMethod"] == cm][k])}
            )
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        fig.set_figwidth(20)
        ax.set_xticks(
            np.arange(1, 12, 1),
            labels=compression_methods,
        )
        ax.bar(np.arange(1, 12, 1), metric_means[k].values(), 0.35)
        ax.set_title("Metric: " + str(k))
        # plt.show()
        print(k)
        plt.savefig("./tmp/last_run_metrics_plots/" + k + ".jpg")
