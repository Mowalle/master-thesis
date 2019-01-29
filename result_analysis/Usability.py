#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import pandas as pd
from scipy import stats
import seaborn as sns

import math
import sys

filenames = ["q_3D_l.csv", "q_3D_h.csv", "q_2D.csv"]

data = []
for filename in filenames:
    # Some cleanup
    df = pd.read_csv(str(sys.argv[1]) + filename)
    df = df.drop("Zeitstempel", axis=1)
    df = df.reindex([0, 1, 13] + list(range(2, 11)) + [14, 11, 12])
    df.set_index("User ID", inplace=True)
    df.columns = ["Question_%d" % (i+1) for i in range(0, len(df.columns))]
    df.to_csv("sus_" + filename[:-4] + "_clean.csv")
    data.append(df)

positives = [1, 3, 6, 7]
positives = [i-1 for i in positives]
negatives = [2, 4, 5, 8]
negatives = [i-1 for i in negatives]

scores = pd.DataFrame(index=data[0].index, columns=["Condition_3D_l", "Condition_3D_h", "Condition_2D"])

for i, df in zip(range(0, 3), data):
    df_pos = 5 - df.iloc[:, positives]
    df_neg = df.iloc[:, negatives] - 1
    df_score = df_pos.join(df_neg).sum(axis=1) * (100/32)
    scores[scores.columns[i]].fillna(df_score, inplace=True)

print("Usability scores:")
print(scores)
print(scores.mean())

sns.set(font="Linux Biolinum O")

# First, print 3D vs 2D.
fig = plt.figure()
colors = ["b", "g"]
ax = sns.boxplot(data=pd.concat([scores.iloc[:, 0:2].mean(axis=1), scores.iloc[:, 2]],axis=1),
                 palette=colors)
ax.set_ylabel("Wertung der Nutzbarkeit\n", labelpad=-10)
ax.set_ylim(bottom=30, top=100)
ax.set_xlabel("")
ax.set_xticklabels(["$3D$", "$2D$"])
plt.show()

# Then, show all individual cases.
fig = plt.figure()
ax = sns.boxplot(data=scores)
ax.set_ylabel("Wertung der Nutzbarkeit\n", labelpad=-10)
ax.set_ylim(bottom=30, top=100)
ax.set_xlabel("")
ax.set_xticklabels(["$3D_l$", "$3D_h$", "$2D$"])
plt.show()

for c in scores.columns:
    print(c + " Mean Score:" + str(scores[c].mean()))
    print(c + " Score Std:"  + str(scores[c].std()))
    print()

for i in range(3):
    print(stats.shapiro(scores.iloc[:, i]))

print(stats.ttest_rel(scores.iloc[:, 2], scores.iloc[:, 0]))