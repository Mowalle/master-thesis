#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import pandas as pd
from scipy import stats
import seaborn as sns

import math
import sys

user_ids = ["user_%d" % i for i in range(15)]
dropped_users = ["user_5"]
user_ids = [s for s in user_ids if s not in dropped_users]

maps = ["map_%d" % (i + 1) for i in range(6)]

condition_names = ["3D_l", "3D_h", "2D"]
cond_labels = ["$3D_l$", "$3D_h$", "$2D$"]
cond_colors = ["b", "y", "g"]


def mu_wilcoxon(n):
    return (n * (n + 1)) / 4


def std_wilcoxon(n):
    return math.sqrt((n * (n + 1) * (2 * n + 1)) / 24)


def wilcoxon_to_z(n, W):
    z = (W - mu_wilcoxon(n)) / std_wilcoxon(n)
    print("z:\t" + str(z))
    return z


df = pd.read_csv(str(sys.argv[1]))

# Cleaning data a bit.
df = df[["User ID", "conditionIndex", "taskIndex", "horizOffsetDeg", "pointingTime"]]
df.columns = ["User ID", "Condition", "Map", "Horizontal_Offset", "Pointing_Time"]
df["User ID"] = ["user_%d" % i for i in df["User ID"]]
df["Condition"] = df["Condition"].map({0: condition_names[0],
                                       1: condition_names[1],
                                       2: condition_names[2]})
df["Map"] = ["map_%d" % (i + 1) for i in df["Map"]]

sns.set(font="Linux Biolinum")
for user in dropped_users:
    df = df.drop(df[df["User ID"] == user].index)

cond_3D_l = df[df["Condition"] == condition_names[0]].reset_index()
cond_3D_h = df[df["Condition"] == condition_names[1]].reset_index()
cond_2D = df[df["Condition"] == condition_names[2]].reset_index()
conditions = [cond_3D_l, cond_3D_h, cond_2D]

# Test horizontal offset.

# Test for normal distribution.
for cond, s in zip(conditions, condition_names):
    print("Testing Normal Distribution for condition %s:" % s)
    stat, p = stats.normaltest(cond["Horizontal_Offset"], axis=0)
    alpha = 1e-3
    print("stat: %s,\tp: %s" % (stat, p))
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis \"Sample comes from normal distribution.\" can be rejected.")
    else:
        print("The null hypothesis \"Sample comes from normal distribution.\" cannot be rejected.")

    # plt.figure()
    # sns.distplot(cond["Horizontal_Offset"])
    # plt.show()
print()
# Not clear => Use Friedman's / Wilcoxon's.

# ----------
# Do the Friedman test and then the Wilcoxon for paired samples.
# ----------
h_error = pd.concat([cond["Horizontal_Offset"] for cond in conditions], axis=1)

x2, p = stats.friedmanchisquare(h_error.iloc[:, 0],
                                h_error.iloc[:, 1],
                                h_error.iloc[:, 2])
print("Friedman statistic: %s,\tp: %s" % (x2, p))
alpha = 0.05
if p < 0.05:
    print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
          " can be rejected.")
else:
    print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
          " cannot be rejected.")
print()
# No significant differences => Don't do Wilcoxon's.

for cond in range(len(conditions)):
    for cond_other in range(cond + 1, len(conditions)):
        W, p = stats.wilcoxon(h_error.iloc[:, cond],
                              h_error.iloc[:, cond_other])
        z = wilcoxon_to_z(len(h_error.index), W)
        print("Wilcoxon statistic:%s -> z:%s,\tp:%s" % (W, z, p))
print()

print("Means:")
for c in conditions:
    print(c.mean(axis=0))
print("Stds:")
for c in conditions:
    print(c.std(axis=0))
print()

## Make a Boxplot.
# output = df.copy()
# output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
#                                                "3D_h": cond_labels[1],
#                                                "2D": cond_labels[2]})
# plt.figure()
# ax = sns.boxplot(x="Condition",
#                  y="Horizontal_Offset",
#                  palette="muted",
#                  color=cond_colors,
#                  flierprops={"marker": "x", "markersize": 3},
#                  data=output)
# ax.set_xlabel("")
# ax.set_ylabel("Horizontale Abweichung der Schätzung [$\\degree$]")
# plt.show()

print("Ausreißer Horizontaler Offset:")
outliers = []
for cond in conditions:
    outliers.extend([y for stat in boxplot_stats(cond["Horizontal_Offset"]) for y in stat["fliers"]])

df_outliers = df.loc[df["Horizontal_Offset"].isin(outliers)]
print(df_outliers[["User ID", "Condition", "Map", "Horizontal_Offset", "Pointing_Time"]])
print()

# ----------
# Per Map Testing (bc. of outliers).
# ----------
output = df.copy()
output["Map"] = output["Map"].map({"map_%d" % i: "Karte %d" % i for i in range(1, 7)})
plt.figure()
ax = sns.boxplot(x="Map",
                 y="Horizontal_Offset",
                 #hue="Condition",
                 palette="muted",
                 color=cond_colors,
                 flierprops={"marker": "x", "markersize": 3},
                 data=output)
ax.set_xlabel("")
ax.set_ylabel("Horizontale Abweichung der Schätzung [$\\degree$]")
plt.show()

# Friedman test per map
map_dfs = [df[df["Map"] == m].reset_index() for m in maps]
h_error_per_map = pd.concat([m["Horizontal_Offset"] for m in map_dfs], axis=1, ignore_index=True)

x2, p = stats.friedmanchisquare(h_error_per_map.iloc[:, 0],
                                h_error_per_map.iloc[:, 1],
                                h_error_per_map.iloc[:, 2],
                                h_error_per_map.iloc[:, 3],
                                h_error_per_map.iloc[:, 4],
                                h_error_per_map.iloc[:, 5])
print("Friedman statistic: %s,\tp: %s" % (x2, p))
alpha = 0.05
if p < 0.05:
    print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
          " can be rejected.")
else:
    print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
          " cannot be rejected.")
print()

# Pairwise Wilcoxon
for m in range(len(map_dfs)):
    for m_other in range(m + 1, len(map_dfs)):
        W, p = stats.wilcoxon(h_error_per_map.iloc[:, m],
                              h_error_per_map.iloc[:, m_other])
        z = wilcoxon_to_z(len(h_error_per_map.index), W)
        print("Pair (%d <--> %d):\tWilcoxon statistic:%s -> z:%s,\tp:%s" % (m+1, m_other+1, W, z, p))
        alpha = 0.05
        if p < 0.05:
            print("H_0 can be rejected.")
print()

for m, s in zip(map_dfs, maps):
    print("%s Mean:" % s)
    print(m.mean(axis=0))
    print("%s STD:" % s)
    print(m.std(axis=0))
    print()
print()

print(df[df["Horizontal_Offset"] < 0].count())
