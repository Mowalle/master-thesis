#!/usr/bin/env python3

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import sys

df = pd.read_csv(str(sys.argv[1]))

sns.set(style="darkgrid", font="Linux Biolinum")

fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)
plt.subplots_adjust(left=0.16, top=0.88)

colors = ["b", "y", "g"] * 2
conditions = ["$3D_l$", "$3D_h$", "$2D$"]

values = [df["conditionIndex"].tolist(),
          df["horizOffsetDeg"].abs().tolist(),
          df["vertOffsetDeg"].abs().tolist()]
#print(values)
df_errors = pd.concat([df["conditionIndex"], df["pointingTime"], df["horizOffsetDeg"].abs(), df["vertOffsetDeg"].abs()], axis=1)
df_errors.rename(columns={"horizOffsetDeg": "abs_horizOffset",
                          "vertOffsetDeg": "abs_vertOffset"},
                 inplace=True)
print(df_errors)

for condition in range(0, 6):
    current_ax = axs.flatten()[condition]
    column = "abs_horizOffset" if condition < 3 else "abs_vertOffset"
    sns.scatterplot(x="pointingTime",
                    y=column,
                    color=colors[condition],
                    alpha=0.8,
                    data=df_errors[df_errors["conditionIndex"] == (condition % 3)],
                    ax=current_ax,
                    #edgecolor="face",
                    s=35)
    current_ax.set_xlim(left=0, right=30)
    current_ax.set_ylim(bottom=0, top=50)
    current_ax.set_xlabel("")
    current_ax.set_title(conditions[condition % 3])

axs.flatten()[0].set_ylabel("Horizontal")
axs.flatten()[3].set_ylabel("Vertikal")
axs.flatten()[4].set_xlabel("Zeit [s]")

fig.text(0.04, 0.5, 'Absolute Abweichung [$\degree$]', va='center', rotation='vertical')
fig.suptitle("Abweichung über Schätzzeit")
#fig.tight_layout()
fig.savefig("pointing_times.pdf")


plt.show()
