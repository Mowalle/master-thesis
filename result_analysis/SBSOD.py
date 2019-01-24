#!/usr/bin/env python3

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

import sys

# The recommended scoring procedure for the scale is to first reverse score the positively phrased items. This
# ensures that all items are coded such that a high number indicates more ability and a low number indicates less
# ability. The items that should be reverse scored are items 1, 3, 4, 5, 7, 9, and 14. After reverse scoring,
# then sum the scores for all of the items together, and then divide the total by the number of items (15) to compute
# the overall score for the scale (average score across items). Using this technique, the score will be a number
# between 1 and 5 where the higher the score, the better the perceived sense of direction.
#
# Source: https://labs.psych.ucsb.edu/hegarty/mary/content/santa-barbara-sense-direction-scale

positives = [1, 3, 4, 5, 7, 9, 14]

df = pd.read_csv(str(sys.argv[1]))
df = df.drop(df.columns[0], axis=1)
df = df.drop(df.columns[1:-15], axis=1)

sns.set(style="whitegrid", font="Linux Biolinum")

df_reversed = df.copy()

df_reversed.iloc[:, positives] = 3 - df_reversed.iloc[:, positives] + 3

df["Score"] = df_reversed.mean(axis=1)
df = df.reindex([0, 1, 13] + list(range(2, 11)) + [14, 11, 12])
df.to_csv("sbsod.csv")

ax = sns.barplot(x="Score",
                 y="User ID",
                 data=df)
ax.set_xlim(1, 5)
ax.set_xticks(np.arange(1, 6))
ax.set_xlabel("SBSOD Wertung\n[höher ist besser]")
ax.set_ylabel("Proband")

labels = df["Score"].tolist()
# Put labels beside each bar for easier reading.
for i in range(0, 15):
    ax.text(x=labels[i]+0.05, y=i+0.2, s="%.2f" % labels[i], size=10, fontdict={"weight": "bold"})

ax.get_figure().suptitle("Santa-Barbara Sense-of-Direction (SBSOD) Skala")
ax.get_figure().savefig("sbsod.pdf")

plt.show()
