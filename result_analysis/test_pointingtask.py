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


def test_pointing(df):
    cond_3D_l = df[df["Condition"] == condition_names[0]].reset_index()
    cond_3D_h = df[df["Condition"] == condition_names[1]].reset_index()
    cond_2D = df[df["Condition"] == condition_names[2]].reset_index()
    conditions = [cond_3D_l, cond_3D_h, cond_2D]

    # Test horizontal offset.

    # # Test for normal distribution.
    # for cond, s in zip(conditions, condition_names):
    #     print("Testing Normal Distribution for condition %s:" % s)
    #     stat, p = stats.normaltest(cond["Horizontal_Offset"], axis=0)
    #     alpha = 1e-3
    #     print("stat: %s,\tp: %s" % (stat, p))
    #     if p < alpha:  # null hypothesis: x comes from a normal distribution
    #         print("The null hypothesis \"Sample comes from normal distribution.\" can be rejected.")
    #     else:
    #         print("The null hypothesis \"Sample comes from normal distribution.\" cannot be rejected.")
    #
    #     plt.figure()
    #     sns.distplot(cond["Horizontal_Offset"])
    #     plt.show()
    # print()
    # # Not clear => Use Friedman's / Wilcoxon's.

    # # ----------
    # # Do the Friedman test and then the Wilcoxon for paired samples.
    # # ----------
    # h_error = pd.concat([cond["Abs_Horizontal_Offset"] for cond in conditions], axis=1)
    # x2, p = stats.friedmanchisquare(h_error.iloc[:, 0],
    #                                 h_error.iloc[:, 1],
    #                                 h_error.iloc[:, 2])
    # print("Friedman statistic: %s,\tp: %s" % (x2, p))
    # alpha = 0.05
    # if p < 0.05:
    #     print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
    #           " can be rejected.")
    # else:
    #     print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
    #           " cannot be rejected.")
    # print()
    # # No significant differences => Don't do Wilcoxon's.
    #
    # for cond in range(len(conditions)):
    #     for cond_other in range(cond + 1, len(conditions)):
    #         W, p = stats.wilcoxon(h_error.iloc[:, cond],
    #                               h_error.iloc[:, cond_other])
    #         z = wilcoxon_to_z(len(h_error.index), W)
    #         print("Wilcoxon statistic:%s -> z:%s,\tp:%s" % (W, z, p))
    # print()
    #
    # for c in conditions:
    #     print("Mean:")
    #     print(c.mean(axis=0))
    #     print("Std:")
    #     print(c.std(axis=0))
    # print()
    #
    # # # Make a Boxplot.
    # # output = df.copy()
    # # output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
    # #                                                "3D_h": cond_labels[1],
    # #                                                "2D": cond_labels[2]})
    # # plt.figure()
    # # ax = sns.boxplot(x="Condition",
    # #                  y="Abs_Horizontal_Offset",
    # #                  palette="muted",
    # #                  color=cond_colors,
    # #                  flierprops={"marker": "x", "markersize": 3},
    # #                  data=output)
    # # ax.set_xlabel("")
    # # ax.set_ylabel("Absolute horiz. Abweichung der Schätzung [$\\degree$]")
    # # plt.show()
    #
    # print("Ausreißer Horizontaler Offset:")
    # outliers = []
    # for cond in conditions:
    #     outliers.extend([y for stat in boxplot_stats(cond["Abs_Horizontal_Offset"]) for y in stat["fliers"]])
    #
    # df_outliers = df.loc[df["Abs_Horizontal_Offset"].isin(outliers)]
    # print(df_outliers[["User ID", "Condition", "Map", "Abs_Horizontal_Offset"]])
    # print()

    # # ----------
    # # Per Map Testing (bc. of outliers).
    # # ----------
    # output = df.copy()
    # output["Map"] = output["Map"].map({"map_%d" % i: "Karte %d" % i for i in range(1, 7)})
    # plt.figure()
    # ax = sns.boxplot(x="Map",
    #                  y="Abs_Horizontal_Offset",
    #                  #hue="Condition",
    #                  palette="muted",
    #                  color=cond_colors,
    #                  flierprops={"marker": "x", "markersize": 3},
    #                  data=output)
    # ax.set_xlabel("")
    # ax.set_ylabel("Absolute horiz. Abweichung der Schätzung [$\\degree$]")
    # plt.show()
    #
    # # Friedman test per map
    # map_dfs = [df[df["Map"] == m].reset_index() for m in maps]
    # h_error_per_map = pd.concat([m["Abs_Horizontal_Offset"] for m in map_dfs], axis=1, ignore_index=True)
    #
    # x2, p = stats.friedmanchisquare(h_error_per_map.iloc[:, 0],
    #                                 h_error_per_map.iloc[:, 1],
    #                                 h_error_per_map.iloc[:, 2],
    #                                 h_error_per_map.iloc[:, 3],
    #                                 h_error_per_map.iloc[:, 4],
    #                                 h_error_per_map.iloc[:, 5])
    # print("Friedman statistic: %s,\tp: %s" % (x2, p))
    # alpha = 0.05
    # if p < 0.05:
    #     print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
    #           " can be rejected.")
    # else:
    #     print("The null hypothesis \"Repeated measurements of the same individuals have the same distribution.\""
    #           " cannot be rejected.")
    # print()
    #
    # # Pairwise Wilcoxon
    # for m in range(len(map_dfs)):
    #     for m_other in range(m + 1, len(map_dfs)):
    #         W, p = stats.wilcoxon(h_error_per_map.iloc[:, m],
    #                               h_error_per_map.iloc[:, m_other])
    #         z = wilcoxon_to_z(len(h_error_per_map.index), W)
    #         print("Pair (%d <--> %d):\tWilcoxon statistic:%s -> z:%s,\tp:%s" % (m + 1, m_other + 1, W, z, p))
    #         alpha = 0.05
    #         if p < 0.05:
    #             print("H_0 can be rejected.")
    # print()
    #
    # for m, s in zip(map_dfs, maps):
    #     print("%s Mean:" % s)
    #     print(m.mean(axis=0))
    #     print("%s STD:" % s)
    #     print(m.std(axis=0))
    #     print()
    # print()

    # ----------------
    # Pointing Times
    # ----------------

    # Make a plot.
    output = df.copy()
    output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
                                                   "3D_h": cond_labels[1],
                                                   "2D": cond_labels[2]})
    plt.figure()
    ax = sns.stripplot(x="Pointing_Time",
                       y="Condition",
                       palette="muted",
                       color=cond_colors,
                       # flierprops={"marker": "x", "markersize": 3},
                       # jitter=False,
                       # linewidth=1,
                       size=3,
                       edgecolor="gray",
                       # alpha=.5,
                       data=output)
    ax.set_xlabel("Benötigte Zeit für Schätzung [s]")
    ax.set_ylabel("")
    ax.set_xlim(left=0, right=25)
    plt.show()
    #
    # print("Ausreißer Pointing Time:")
    # outliers = []
    # for cond in conditions:
    #     outliers.extend([y for stat in boxplot_stats(cond["Pointing_Time"]) for y in stat["fliers"]])
    #
    # df_outliers = df.loc[df["Pointing_Time"].isin(outliers)]
    # print(df_outliers[["User ID", "Condition", "Map", "Horizontal_Offset", "Pointing_Time"]])
    # print()
    #
    # # # Test for normal distribution.
    # # for cond, s in zip(conditions, condition_names):
    # #     print("Testing Normal Distribution for condition %s:" % s)
    # #     stat, p = stats.normaltest(cond["Horizontal_Offset"], axis=0)
    # #     alpha = 1e-3
    # #     print("stat: %s,\tp: %s" % (stat, p))
    # #     if p < alpha:  # null hypothesis: x comes from a normal distribution
    # #         print("The null hypothesis \"Sample comes from normal distribution.\" can be rejected.")
    # #     else:
    # #         print("The null hypothesis \"Sample comes from normal distribution.\" cannot be rejected.")
    # #
    # #     # plt.figure()
    # #     # sns.distplot(cond["Horizontal_Offset"])
    # #     # plt.show()
    # # print()
    #
    # Do the Friedman test and then the Wilcoxon for paired samples.
    pointing_times = pd.concat([cond["Pointing_Time"] for cond in conditions], axis=1)

    x2, p = stats.friedmanchisquare(pointing_times.iloc[:, 0],
                                    pointing_times.iloc[:, 1],
                                    pointing_times.iloc[:, 2])
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
            W, p = stats.kruskal(pointing_times.iloc[:, cond],
                                 pointing_times.iloc[:, cond_other])
            z = wilcoxon_to_z(len(pointing_times.index), W)
            print("Pair (%s <--> %s):\tWilcoxon statistic:%s -> z:%s,\tp:%s" % (condition_names[cond],
                                                                                condition_names[cond_other],
                                                                                W, z, p))
            alpha = 0.05
            if p < 0.05:
                print("H_0 can be rejected.")
    print()

    for cond, s in zip(conditions, condition_names):
        print("%s Mean:" % s)
        print(cond.mean(axis=0))
        print("%s STD:" % s)
        print(cond.std(axis=0))
        print()
    print()
    #
    # #----------
    # # Correlate Time to precision.
    # #----------
    #
    # # fig, axs = plt.subplots(1, 3, sharey=True)
    # # axs = axs.flatten()
    # #
    # # for cond in range(3):
    # #     output = conditions[cond].copy()
    # #     output["Horizontal_Offset"] = output["Horizontal_Offset"].abs()
    # #
    # #     sns.scatterplot(x="Pointing_Time",
    # #                     y="Horizontal_Offset",
    # #                     color=cond_colors[cond],
    # #                     palette="muted",
    # #                     ax=axs[cond],
    # #                     data=output)
    # #
    # #     axs[cond].set_xlim(left=0, right=30)
    # #     axs[cond].set_ylim(bottom=0, top=50)
    # #     axs[cond].set_ylabel("Absolute horiz. Abweichung [$\\degree$]", labelpad=10)
    # #     axs[cond].set_xlabel("")
    # #
    # # axs[1].set_xlabel("Benötigte Zeit für Schätzung [s]")
    # # plt.show()
    #
    # # Check correlations per condition.
    # for cond in range(3):
    #     print("Checking correlation (Pointing Time <-> H.Error) for condition %s:" % condition_names[cond])
    #     print(stats.spearmanr(conditions[cond]["Pointing_Time"], conditions[cond]["Horizontal_Offset"]))
    #
    # #----------
    # # Correlate SBSOD to H.Error.
    # #----------
    #
    # df_sbsod = pd.read_csv("sbsod.csv")
    # df_sbsod = df_sbsod.iloc[:, 1:]
    # df_sbsod = df_sbsod.drop(df_sbsod[df_sbsod["User ID"] == "user_5"].index)
    #
    # # Mean h.error for each user (per cond.).
    # values = []
    # for user in user_ids:
    #     for cond in range(len(conditions)):
    #         error = conditions[cond][conditions[cond]["User ID"] == user]["Horizontal_Offset"].mean()
    #         score = df_sbsod[df_sbsod["User ID"] == user].iat[0, -1]
    #         values.append([user, condition_names[cond], error, score])
    #
    # output = pd.DataFrame(values,
    #                       columns=["User ID", "Condition", "Horizontal_Offset", "SBSOD_Score"])
    # output["Horizontal_Offset"] = output["Horizontal_Offset"].abs()
    #
    # # # Check correlations per condition.
    # # for cond in conditions:
    # #     print("Checking correlation (SBSOD <-> Time) for condition %s:" % cond)
    # #     df_cond = output[output["Condition"] == cond]
    # #     print(stats.spearmanr(df_cond["Mean_Search_Time"], df_cond["SBSOD_Score"]))
    #
    # print(output["Horizontal_Offset"])
    # fig, axs = plt.subplots(1, 3, sharey=True)
    # axs = axs.flatten()
    # for cond in range(3):
    #     temp = output[output["Condition"] == condition_names[cond]]
    #     sns.scatterplot(x="SBSOD_Score",
    #                     y="Horizontal_Offset",
    #                     color=cond_colors[cond],
    #                     palette="muted",
    #                     ax=axs[cond],
    #                     data=temp)
    #
    #     #axs[cond].set_xlim(left=0, right=30)
    #     axs[cond].set_ylim(bottom=0, top=50)
    #     axs[cond].set_ylabel("Absolute horiz. Abweichung [$\\degree$]", labelpad=10)
    #     axs[cond].set_xlabel("")
    #     axs[cond].set_title(cond_labels[cond])
    #
    # axs[1].set_xlabel("SBSOD-Wertung")
    # plt.show()
    #
    # # # Check correlations per condition.
    # # for cond in condition_names:
    # #     print("Checking correlation (SBSOD <-> H.Error) for condition %s:" % cond)
    # #     temp = output[output["Condition"] == cond]
    # #     print(stats.spearmanr(temp["SBSOD_Score"], temp["Horizontal_Offset"]))


def test_hitrate(df):
    cond_3D_l = df[df["Condition"] == condition_names[0]].reset_index()
    cond_3D_h = df[df["Condition"] == condition_names[1]].reset_index()
    cond_2D = df[df["Condition"] == condition_names[2]].reset_index()
    conditions = [cond_3D_l, cond_3D_h, cond_2D]

    values = []
    for condition, cn in zip(conditions, condition_names):
        for m in maps:
            hits = condition[condition["Map"] == m]["Hit_Room"]
            row = [cn, m, hits.mean(), hits.sum()]
            values.append(row)

    hitrates = pd.DataFrame(values, columns=["Condition", "Map", "Hitrate", "Hitcount"])    # # output = df.copy()
    for cn in condition_names:
        count = hitrates[hitrates["Condition"] == cn]["Hitcount"].sum()
        print("Abs. Hitcount: %d" % count)
        print(hitrates[hitrates["Condition"] == cn].mean())

    ## Make a plot
    # output = hitrates.copy()
    # output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
    #                                                "3D_h": cond_labels[1],
    #                                                "2D": cond_labels[2]})
    # output["Map"] = output["Map"].map({m: k for m,k in zip(maps, ["Karte %d" % (i+1) for i in range(len(maps))])})
    # output = output.rename(columns={"Condition": "Kondition"})
    # print(output)
    # plt.figure()
    # ax = sns.barplot(x="Map", y="Hitcount", hue="Kondition", data=output)
    # ax.set_ylim(bottom=5, top=14)
    # ax.set_xlabel("")
    # ax.set_ylabel("Anzahl Treffer des Zielraums")
    # plt.show()

    values = []
    for condition, cn in zip(conditions, condition_names):
        for u in user_ids:
            hits = condition[condition["User ID"] == u]["Hit_Room"]
            row = [cn, u, hits.mean(), hits.sum()]
            values.append(row)

    hitrates_per_user = pd.DataFrame(values, columns=["Condition", "User ID", "Hitrate", "Hitcount"])

    ## Make a plot
    # output = hitrates_per_user.copy()
    # output["Condition"] = output["Condition"].map({"3D_l": cond_labels[0],
    #                                                "3D_h": cond_labels[1],
    #                                                "2D": cond_labels[2]})
    # output.loc[:, "Hitrate"] *= 100
    # plt.figure()
    # ax = sns.boxplot(x="Condition", y="Hitrate", data=output, palette="muted")
    # sns.swarmplot(x="Condition", y="Hitrate", data=output, palette="muted")
    # ax.set_xlabel("")
    # ax.set_ylabel("Trefferrate pro Proband [%]")
    # plt.show()

    print(stats.friedmanchisquare(
        hitrates_per_user[hitrates_per_user["Condition"] == condition_names[0]]["Hitrate"],
        hitrates_per_user[hitrates_per_user["Condition"] == condition_names[1]]["Hitrate"],
        hitrates_per_user[hitrates_per_user["Condition"] == condition_names[2]]["Hitrate"]))
    print()


def main():
    df = pd.read_csv(str(sys.argv[1]))

    # Cleaning data a bit.
    df = df[["User ID", "conditionIndex", "taskIndex", "horizOffsetDeg", "pointingTime", "hitRoom"]]
    df.columns = ["User ID", "Condition", "Map", "Horizontal_Offset", "Pointing_Time", "Hit_Room"]
    df["User ID"] = ["user_%d" % i for i in df["User ID"]]
    df["Condition"] = df["Condition"].map({0: condition_names[0],
                                           1: condition_names[1],
                                           2: condition_names[2]})
    df["Map"] = ["map_%d" % (i + 1) for i in df["Map"]]

    # We want to work mostly with the absolute error, so that positive and negative angles don't cancel each other out.
    df["Abs_Horizontal_Offset"] = df["Horizontal_Offset"].abs()

    sns.set(font="Linux Biolinum O")
    for user in dropped_users:
        df = df.drop(df[df["User ID"] == user].index)

    test_pointing(df)
    #test_hitrate(df)


if __name__ == "__main__":
    main()
