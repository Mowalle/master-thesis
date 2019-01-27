#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import seaborn as sns

import sys

df = pd.read_csv(str(sys.argv[1]))
df = df[["conditionIndex", "taskIndex", "User ID", "pointingTime"]]

sns.set(style="whitegrid", font="Linux Biolinum")
ax = sns.boxplot(x="conditionIndex",
                 y="pointingTime",
                 palette="muted",
                 flierprops={"marker": "x", "markersize": 3},
                 data=df)
ax.set_xlabel("")
ax.set_xticklabels(["$3D_l$", "$3D_h$", "$2D$"])
ax.set_ylabel("Schätzungszeit [s]")
ax.set_ylim(bottom=0)

outliers = []
for cond in range(3):
    outliers.extend([y for stat in boxplot_stats(df[df["conditionIndex"] == cond]["pointingTime"]) for y in stat['fliers']])

df_outliers = df.loc[df["pointingTime"].isin(outliers)]
df_outliers = df_outliers[["User ID", "conditionIndex", "taskIndex", "pointingTime"]]
df_outliers.columns = ["User ID", "Condition", "Map", "Pointing_Time"]
df_outliers.loc[:, "User ID"] = ["user_%d" % id for id in df_outliers["User ID"]]
df_outliers["Map"] = df_outliers["Map"].map({i: "map_%d" % (i+1) for i in range(6)})
df_outliers["Condition"] = df_outliers["Condition"].map({0: "3D_l", 1: "3D_h", 2: "2D"})

print("Ausreisser:")
print(df_outliers)
plt.show()

# fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
# plt.subplots_adjust(left=0.16, top=0.88)
# colors = ["b", "y", "g"] * 2
# conditions = ["$3D_l$", "$3D_h$", "$2D$"]
#
# values = [df["conditionIndex"].tolist(),
#           df["horizOffsetDeg"].abs().tolist(),
#           df["vertOffsetDeg"].abs().tolist()]
# #print(values)
# df_errors = pd.concat([df["conditionIndex"], df["pointingTime"], df["horizOffsetDeg"].abs(), df["vertOffsetDeg"].abs()], axis=1)
# df_errors.rename(columns={"horizOffsetDeg": "abs_horizOffset",
#                           "vertOffsetDeg": "abs_vertOffset"},
#                  inplace=True)
# print(df_errors)
#
# for condition in range(0, 6):
#     current_ax = axs.flatten()[condition]
#     column = "abs_horizOffset" if condition < 3 else "abs_vertOffset"
#     sns.scatterplot(x="pointingTime",
#                     y=column,
#                     color=colors[condition],
#                     alpha=0.8,
#                     data=df_errors[df_errors["conditionIndex"] == (condition % 3)],
#                     ax=current_ax,
#                     #edgecolor="face",
#                     s=35)
#     current_ax.set_xlim(left=0, right=30)
#     current_ax.set_ylim(bottom=0, top=50)
#     current_ax.set_xlabel("")
#     current_ax.set_title(conditions[condition % 3])
#
# axs.flatten()[0].set_ylabel("Horizontal")
# axs.flatten()[3].set_ylabel("Vertikal")
# axs.flatten()[4].set_xlabel("Zeit [s]")
#
# fig.text(0.04, 0.5, 'Absolute Abweichung [$\degree$]', va='center', rotation='vertical')
# fig.suptitle("Abweichung über Schätzzeit")
# #fig.tight_layout()
# fig.savefig("pointing_times.pdf")
#
#
# plt.show()
