#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

num_users = 14
num_conditions = 3
num_tasks = 6

df = pd.read_csv("results.csv")

sns.set()
sns.set_style("whitegrid", rc={"font.family": ["Linux Biolinum", "sans-serif"]})

plt.figure()
ax = sns.boxplot(x="taskIndex", y="megamapTime", hue="conditionIndex", data=df)
plt.title("Benötigte Zeit zum Suchen und Auswählen des Zielraums")
plt.xticks(df["taskIndex"], labels=["Karte %d" % (i+1) for i in range(0, 6)])
plt.xlabel("")
plt.ylabel("Zeit [s]")
plt.ylim(0)
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])
fig = ax.get_figure()
fig.savefig("megamap_time.pdf")

plt.figure()
ax = sns.boxplot(x="taskIndex", y="horizOffsetDeg", hue="conditionIndex", data=df)
plt.title("Horzontale Abweichung beim Richtungsschätzen")
plt.xticks(df["taskIndex"], labels=["Karte %d" % (i+1) for i in range(0, 6)])
plt.xlabel("")
plt.ylabel("Grad [$\degree$]")
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])
fig = ax.get_figure()
fig.savefig("horiz_error.pdf")

plt.figure()
ax = sns.boxplot(x="taskIndex", y="vertOffsetDeg", hue="conditionIndex", data=df)
plt.title("Vertikale Abweichung beim Richtungsschätzen")
plt.xticks(df["taskIndex"], labels=["Karte %d" % (i+1) for i in range(0, 6)])
plt.xlabel("")
plt.ylabel("Grad [$\degree$]")
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])
fig = ax.get_figure()
fig.savefig("vert_error.pdf")



