#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import pandas as pd
from scipy import stats
import seaborn as sns

import math
import sys

cond_colors = ["b", "y", "g"]
cond_labels = ["$3D_l$", "$3D_h$", "$2D$"]

def mu_wilcoxon(n):
    return (n * (n + 1)) / 4


def std_wilcoxon(n):
    return math.sqrt( (n * (n + 1) * (2 * n + 1)) / 24)


def wilcoxon_to_z(n, W):
    z = (W - mu_wilcoxon(n)) / std_wilcoxon(n)
    print("z:\t" + str(z))
    return z

df = pd.read_csv(str(sys.argv[1]))

# Cleaning data a bit.
df = df[["User ID", "conditionIndex", "taskIndex", "megamapTime", "pointingTime", "horizOffsetDeg"]]
df.columns = ["User ID", "Condition", "Map", "Search_Time", "Pointing_Time", "Horizontal_Offset"]
df["User ID"] = ["user_%d" % i for i in df["User ID"]]
df["Condition"] = df["Condition"].map({0: "3D_l", 1: "3D_h", 2: "2D"})
df["Map"] = ["map_%d" % (i+1) for i in df["Map"]]

sns.set(font="Linux Biolinum")
df = df.drop(df[df["User ID"] == "user_5"].index)
#df = df.drop(df[df["User ID"] == "user_9"].index)

# Test Searching_Time.
outliers = []
for cond in df["Condition"].unique():
    outliers.extend([y for stat in boxplot_stats(df[df["Condition"] == cond]["Search_Time"]) for y in stat['fliers']])

df_outliers = df.loc[df["Search_Time"].isin(outliers)]

print("Ausreisser:")
print(df_outliers[["User ID", "Search_Time"]])
print(df_outliers["User ID"].value_counts())
print()

# Draw distributions of search time.
fig, axs = plt.subplots(1, 3, sharey=True)
axs = axs.flatten()
for i in range(3):
    time_cond = df[df["Condition"] == df["Condition"].unique()[i]]["Search_Time"]
    k2, p = stats.normaltest(time_cond, axis=0)
    alpha = 1e-3
    print("k2:\t" + str(k2) + "\np:\t" + str(p))

    sns.distplot(time_cond, color=cond_colors[i], ax=axs[i])
    axs[i].set_xlabel("")
    axs[i].set_xlim(left=-10, right=75)
    axs[i].set_title(cond_labels[i])
axs[1].set_xlabel("Suchzeit [s]")

plt.show()

# Do the Friedman test and then the Wilcoxon for paired samples.
cond_3D_l = df[df["Condition"] == "3D_l"].reset_index()
cond_3D_h = df[df["Condition"] == "3D_h"].reset_index()
cond_2D = df[df["Condition"] == "2D"].reset_index()
times = pd.concat([cond_3D_l["Search_Time"], cond_3D_h["Search_Time"], cond_2D["Search_Time"]], axis=1)

print(stats.friedmanchisquare(times.iloc[:, 0], times.iloc[:, 1], times.iloc[:, 2]))

W, p = stats.wilcoxon(times.iloc[:, 2], times.iloc[:, 0])
print(str(W) + "\t" + str(p))
wilcoxon_to_z(len(times.index), W)

# diff = pd.concat([cond_3D_h["Search_Time"] - cond_3D_l["Search_Time"],
#                      cond_2D["Search_Time"] - cond_3D_l["Search_Time"],
#                      cond_2D["Search_Time"] - cond_3D_h["Search_Time"]],
#                     axis=1)
# diff.columns = ["3D_h - 3D_l", "2D - 3D_l", "2D - 3D_h"]
#
# plt.figure()
# #sns.boxplot(x="Condition", y="Search_Time", data=df)
# sns.boxplot(x="variable", y="value", data=pd.melt(diff))
# plt.show()


# # Test Pointing_Time.
# outliers = []
# for cond in df["Condition"].unique():
#     outliers.extend([y for stat in boxplot_stats(df[df["Condition"] == cond]["Pointing_Time"]) for y in stat['fliers']])
#
# df_outliers = df.loc[df["Pointing_Time"].isin(outliers)]
#
# print("Ausreisser:")
# print(df_outliers[["User ID", "Pointing_Time"]])
# print(df_outliers["User ID"].value_counts())
#
# plt.figure()
# ax = sns.boxplot(x="Condition", y="Pointing_Time", data=df)
# plt.show()

# # Test Horizontal_Offset.
# outliers = []
# for cond in df["Condition"].unique():
#     outliers.extend([y for stat in boxplot_stats(df[df["Condition"] == cond]["Horizontal_Offset"]) for y in stat['fliers']])
#
# df_outliers = df.loc[df["Horizontal_Offset"].isin(outliers)]
#
# print("Ausreisser:")
# print(df_outliers[["User ID", "Condition", "Horizontal_Offset"]])
# print(df_outliers["User ID"].value_counts())
#
# ax = sns.boxplot(x="Condition", y="Horizontal_Offset", data=df)
#
# for cond, color in zip(df["Condition"].unique(), ["b", "y", "g"]):
#     herr_cond = df[df["Condition"] == cond]["Horizontal_Offset"]
#     k2, p = stats.normaltest(herr_cond, axis=0)
#     alpha = 1e-3
#     print("k2:\t" + str(k2) + "\np:\t" + str(p))
#
#     plt.figure()
#     sns.distplot(herr_cond, color=color)
#     plt.show()
