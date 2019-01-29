#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import seaborn as sns

import sys

num_users = 14
num_conditions = 3
num_tasks = 6

df = pd.read_csv(str(sys.argv[1]))

sns.set(style="whitegrid", font="Linux Biolinum")

# Time Boxplot

df_times = df[["taskIndex", "conditionIndex", "megamapTime"]].copy()

fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [6, 1]}, sharey=True)
sns.boxplot(x="taskIndex",
            y="megamapTime",
            hue="conditionIndex",
            palette="muted",
            data=df_times,
            ax=axs[0],
            flierprops={"marker": "x", "markersize": 3})
print(df_times["megamapTime"])
axs[0].set_ylim(bottom=0)
axs[0].set_xticklabels(["Karte %d" % i for i in range(1, 7)])
axs[0].set_xlabel("")
axs[0].set_ylabel("Suchzeit [s]")
handles, _ = axs[0].get_legend_handles_labels()
axs[0].legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])

print(df[["horizOffsetDeg", "vertOffsetDeg"]].corr())
# Somehow gives only 16 outliers, even though 17 are plottet?
# outliers = [y for stat in boxplot_stats(df_times["megamapTime"]) for y in stat["fliers"]]
# print(df[df["megamapTime"].isin(outliers)])

df_times.loc[:, "taskIndex"] = 7
sns.boxplot(x="taskIndex",
            y="megamapTime",
            hue="conditionIndex",
            palette="muted",
            data=df_times,
            ax=axs[1],
            flierprops={"marker": "x", "markersize": 3})
axs[1].legend_.remove()
axs[1].set_xticklabels(["Gesamt"])
axs[1].set_xlabel("")
axs[1].set_ylabel("")

plt.show()

# Horiz. Error Boxplot

df_h_error = df[["taskIndex", "conditionIndex", "horizOffsetDeg"]].copy()

fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [6, 1]}, sharey=True)
sns.boxplot(x="taskIndex",
            y="horizOffsetDeg",
            hue="conditionIndex",
            palette="muted",
            data=df_h_error,
            ax=axs[0],
            flierprops={"marker": "x", "markersize": 3})
axs[0].set_xticklabels(["Karte %d" % i for i in range(1, 7)])
axs[0].set_xlabel("")
axs[0].set_ylabel("Horizontale Abweichung [$\\degree$]")
handles, _ = axs[0].get_legend_handles_labels()
axs[0].legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])

h_ylims = axs[0].get_ylim()

df_h_error.loc[:, "taskIndex"] = 7
sns.boxplot(x="taskIndex",
            y="horizOffsetDeg",
            hue="conditionIndex",
            palette="muted",
            data=df_h_error,
            ax=axs[1],
            flierprops={"marker": "x", "markersize": 3})
axs[1].legend_.remove()
axs[1].set_xticklabels(["Gesamt"])
axs[1].set_xlabel("")
axs[1].set_ylabel("")

plt.show()

# Vert. Error Boxplot

df_v_error = df[["taskIndex", "conditionIndex", "vertOffsetDeg"]].copy()

fig, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios': [6, 1]}, sharey=True)
sns.boxplot(x="taskIndex",
            y="vertOffsetDeg",
            hue="conditionIndex",
            palette="muted",
            data=df_v_error,
            ax=axs[0],
            flierprops={"marker": "x", "markersize": 3})
axs[0].set_xticklabels(["Karte %d" % i for i in range(1, 7)])
axs[0].set_xlabel("")
axs[0].set_ylabel("Vertikale Abweichung [$\\degree$]")
handles, _ = axs[0].get_legend_handles_labels()
axs[0].legend(handles, ["$3D_l$", "$3D_h$", "$2D$"])
axs[0].set_ylim(h_ylims)

df_v_error.loc[:, "taskIndex"] = 7
sns.boxplot(x="taskIndex",
            y="vertOffsetDeg",
            hue="conditionIndex",
            palette="muted",
            data=df_v_error,
            ax=axs[1],
            flierprops={"marker": "x", "markersize": 3})
axs[1].legend_.remove()
axs[1].set_xticklabels(["Gesamt"])
axs[1].set_xlabel("")
axs[1].set_ylabel("")

plt.show()