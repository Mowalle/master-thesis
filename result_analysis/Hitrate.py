#!/usr/bin/env python3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

import sys

df = pd.read_csv(str(sys.argv[1]))
df = df[["conditionIndex", "taskIndex", "hitRoom"]]

values = []
for condition in df["conditionIndex"].unique():
    for task in df["taskIndex"].unique():
        df_hits = df[(df["conditionIndex"] == condition) & (df["taskIndex"] == task)]
        row = [task, condition, df_hits["hitRoom"].mean()]
        values.append(row)

hitrates = pd.DataFrame(values, columns=["Map", "Condition", "Hitrate"])
hitrates["Hitrate"] *= 100
print(hitrates)

sns.set(style="whitegrid", font="Linux Biolinum")

plt.figure()
ax = sns.boxplot(x="Condition",
                 y="Hitrate",
                 data=hitrates,
                 palette="muted")
ax = sns.swarmplot(x="Condition",
                   y="Hitrate",
                   data=hitrates,
                   color="k")
ax.set_ylim(top=100)
ax.set_ylabel("Trefferquote bei Richtungsschätzung [%]")
ax.set_xlabel("")
ax.set_xticklabels(["$3D_l$", "$3D_h$", "$2D$"])
ax.text(x=2 + 0.05,
        y=hitrates[hitrates["Condition"] == 2].iloc[4]["Hitrate"] + 1,
        s="Karte 5")

plt.figure()
ax = sns.barplot(x="Map",
                 y="Hitrate",
                 data=hitrates,
                 capsize=.1,
                 errwidth=1.5,
                 palette="muted")
ax.set_xticklabels(["Karte %d" % (i + 1) for i in range(6)])
ax.set_ylim(top=100, bottom=40)
ax.set_ylabel("Trefferquote bei Richtungsschätzung [%]")
ax.set_xlabel("")

plt.show()
