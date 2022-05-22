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

    df["CompressionMethod"].unique()

    JPEG_means = {}
    JPEG2K_means = {}
    JPEGXR_means = {}
    DL_means = {}

    for k in metrics:
        JPEG_means.update({k: np.mean(df.loc[df["CompressionMethod"] == "JPEG"][k])})
        JPEG2K_means.update(
            {k: np.mean(df.loc[df["CompressionMethod"] == "JPEG2K"][k])}
        )
        JPEGXR_means.update(
            {k: np.mean(df.loc[df["CompressionMethod"] == "JPEGXR"][k])}
        )
        DL_means.update(
            {k: np.mean(df.loc[df["CompressionMethod"] == "b2018-gdn-128-1"][k])}
        )
        fig, ax = plt.subplots()
        ax.set_xticks(
            np.arange(1, 5, 1),
            labels=df["CompressionMethod"].unique(),
        )
        ax.bar(
            np.arange(1, 5, 1),
            [
                DL_means[k],
                JPEGXR_means[k],
                JPEG_means[k],
                JPEG2K_means[k],
            ],
        )
        ax.set_title("Metric: " + str(k))
        # plt.show()
        print(k)
        plt.savefig("./tmp/last_run_metrics_plots/" + k + ".jpg")
