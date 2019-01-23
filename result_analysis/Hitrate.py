#!/usr/bin/env python3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

import sys

df = pd.read_csv(str(sys.argv[1]))

sns.set(style="whitegrid", font="Linux Biolinum")

fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [6, 1]}, sharey=True)
plt.subplots_adjust(wspace=0.02)

values = []
for condition in df["conditionIndex"].unique():
    for task in df["taskIndex"].unique():
        df_hits = df[(df["conditionIndex"] == condition) & (df["taskIndex"] == task)]
        row = [condition, task, df_hits["hitRoom"].mean()]
        values.append(row)

df_hitrates = pd.DataFrame(values, columns=["conditionIndex", "taskIndex", "hitrate"])
print(df_hitrates)
sns.barplot(x="taskIndex",
            y="hitrate",
            hue="conditionIndex",
            data=df_hitrates,
            ax=axs[0])
axs[0].set_xticklabels(["Karte %d" % i for i in range(1, 7)])
axs[0].set_xlabel("")
axs[0].set_ylim(0, 1)
axs[0].set_yticklabels(np.arange(0, 101, step=20))
axs[0].set_ylabel("Trefferquote [%]")
handles, _ = axs[0].get_legend_handles_labels()
axs[0].legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])


values = []
for condition in df["conditionIndex"].unique():
    df_hits = df[df["conditionIndex"] == condition]
    row = ["dummy", condition, df_hits["hitRoom"].mean()]
    values.append(row)

df_hitrates = pd.DataFrame(values, columns=["Gesamt", "conditionIndex", "hitrate"])
print(df_hitrates)
sns.barplot(x="Gesamt",
            y="hitrate",
            hue="conditionIndex",
            data=df_hitrates,
            ax=axs[1])
axs[1].legend_.remove()
axs[1].set_xticklabels(["Gesamt"])
axs[1].set_xlabel("")
axs[1].set_ylabel("")

fig.suptitle("Zielraum-Trefferquote beim Richtungsschätzen")
fig.savefig("hitrates.pdf")
plt.show()
