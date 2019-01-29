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

conditions = ["3D_l", "3D_h", "2D"]
maps = ["map_%d" % (i + 1) for i in range(6)]

cond_colors = ["b", "y", "g"]
cond_labels = ["$3D_l$", "$3D_h$", "$2D$"]


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
df = df[["User ID", "conditionIndex", "taskIndex", "megamapTime", "numErrors"]]
df.columns = ["User ID", "Condition", "Map", "Search_Time", "Wrong_Selections"]
df["User ID"] = ["user_%d" % i for i in df["User ID"]]
df["Condition"] = df["Condition"].map({0: "3D_l", 1: "3D_h", 2: "2D"})
df["Map"] = ["map_%d" % (i + 1) for i in df["Map"]]

sns.set(font="Linux Biolinum O")
df = df.drop(df[df["User ID"] == "user_5"].index)
# df = df.drop(df[df["User ID"] == "user_9"].index)

cond_3D_l = df[df["Condition"] == "3D_l"].reset_index()
cond_3D_h = df[df["Condition"] == "3D_h"].reset_index()
cond_2D = df[df["Condition"] == "2D"].reset_index()
condition_dict = {conditions[0]: cond_3D_l, conditions[1]: cond_3D_h, conditions[2]: cond_2D}

# Test Searching_Time.

# # For table.
# means_per_cond = [cond_3D_l["Search_Time"].mean(),
#                   cond_3D_h["Search_Time"].mean(),
#                   cond_2D["Search_Time"].mean()]
# std_per_cond = [cond_3D_l["Search_Time"].std(),
#                 cond_3D_h["Search_Time"].std(),
#                 cond_2D["Search_Time"].std()]
# df_times_overview = pd.DataFrame([means_per_cond, std_per_cond])

outliers = []
for cond in condition_dict.keys():
    outliers.extend([y for stat in boxplot_stats(condition_dict[cond]["Search_Time"]) for y in stat['fliers']])

df_outliers = df.loc[df["Search_Time"].isin(outliers)]
print("Ausreisser:")
print(df_outliers[["User ID", "Search_Time"]])
print(df_outliers["User ID"].value_counts())
print()

# output = df.copy()
# output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
#                                                "3D_h": cond_labels[1],
#                                                "2D": cond_labels[2]})
# plt.figure()
# ax = sns.boxplot(x="Condition",
#             y="Search_Time",
#             palette="muted",
#             color=cond_colors,
#             flierprops={"marker": "x", "markersize": 3},
#             data=output)
# ax.set_ylabel("Benötigte Zeit für Suche nach Zielraum [s]")
# ax.set_xlabel("")
# plt.show()

# # Draw distributions of search time.
# # fig, axs = plt.subplots(1, 3, sharey=True)
# # axs = axs.flatten()
# for i in range(3):
#     time_cond = df[df["Condition"] == df["Condition"].unique()[i]]["Search_Time"]
#     k2, p = stats.normaltest(time_cond, axis=0)
#     alpha = 1e-3
#     print("k2:\t" + str(k2) + "\np:\t" + str(p))
#     print(stats.skew(time_cond, axis=0))
#
# #     sns.distplot(time_cond, color=cond_colors[i], ax=axs[i])
# #     axs[i].set_xlabel("")
# #     axs[i].set_xlim(left=-10, right=75)
# #     axs[i].set_title(cond_labels[i])
# # axs[1].set_xlabel("Suchzeit [s]")
# # plt.show()

#----------
# Do the Friedman test and then the Wilcoxon for paired samples.
#----------

times = pd.concat([cond_3D_l["Search_Time"], cond_3D_h["Search_Time"], cond_2D["Search_Time"]], axis=1)

print(stats.friedmanchisquare(times.iloc[:, 0], times.iloc[:, 1], times.iloc[:, 2]))

W, p = stats.wilcoxon(times.iloc[:, 1], times.iloc[:, 0])
print(str(W) + "\t" + str(p))
wilcoxon_to_z(len(times.index), W)

#----------
# Correlate SBSOD to times.
#----------

df_sbsod = pd.read_csv("sbsod.csv")
df_sbsod = df_sbsod.iloc[:, 1:]
df_sbsod = df_sbsod.drop(df_sbsod[df_sbsod["User ID"] == "user_5"].index)

# Mean search times for each user (per cond.).
values = []
for user in user_ids:
    for cond in conditions:
        time = df[(df["User ID"] == user) & (df["Condition"] == cond)]["Search_Time"].mean()
        score = df_sbsod[df_sbsod["User ID"] == user].iat[0, -1]
        values.append([user, cond, time, score])

output = pd.DataFrame(values,
                      columns=["User ID", "Condition", "Mean_Search_Time", "SBSOD_Score"])

# Check correlations per condition.
for cond in conditions:
    print("Checking correlation (SBSOD <-> Time) for condition %s:" % cond)
    df_cond = output[output["Condition"] == cond]
    print(stats.spearmanr(df_cond["Mean_Search_Time"], df_cond["SBSOD_Score"]))

#----------
# Find the one error when selecting rooms.
#----------
wrong_selections = df[df["Wrong_Selections"] != 0]
print(wrong_selections)

# plt.figure()
# output_renamed = output.rename(columns={"Condition": "Kondition"})
# output_renamed["Kondition"] = output_renamed["Kondition"].map({"3D_l": cond_labels[0],
#                                                                "3D_h": cond_labels[1],
#                                                                "2D": cond_labels[2]})
# ax = sns.scatterplot(x="SBSOD_Score",
#                      y="Mean_Search_Time",
#                      hue="Kondition",
#                      data=output_renamed,
#                      palette="muted")
# ax.set_ylabel("$\\mu$ Suchzeit [s] pro Kondition")
# ax.set_xlabel("SBSOD Wertung")
# plt.show()

#
# for user in cond_3D_l["User ID"].unique():
#     user_times.append(times.iloc[cond_3D_l[cond_3D_l["User ID"] == user].index].mean(axis=1).mean())
#
# output = pd.DataFrame({"User_Mean_Time": user_times, "SBSOD_Score": df_sbsod["Score"].tolist()})
# plt.figure()
# sns.scatterplot(x="User_Mean_Time", y="SBSOD_Score", data=output)
# plt.show()
#
# print(stats.spearmanr(user_times, df_sbsod["Score"].tolist()))

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
