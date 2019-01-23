#!/usr/bin/env python3

import pandas as pd

import sys

num_users = 14
num_conditions = 3
num_tasks = 6

# Means per condition ----

df = pd.read_csv(str(sys.argv[1]), delimiter=",")
df = df[["conditionIndex", "megamapTime", "horizOffsetDeg", "vertOffsetDeg", "hitRoom"]]

# output = pd.DataFrame(index="])
values = []
for condition in range(0, num_conditions):
    df_cond = df[df["conditionIndex"] == condition]
    column = [df_cond["megamapTime"].mean(), df_cond["megamapTime"].std(),
              df_cond["horizOffsetDeg"].mean(), df_cond["horizOffsetDeg"].std(),
              df_cond["vertOffsetDeg"].mean(), df_cond["vertOffsetDeg"].std(),
              df_cond["hitRoom"].mean() * 100]
    values.append(column)

output = pd.DataFrame(values, index=["3D_l", "3D_h", "2D"], columns=["Megamap Time",
                                                                           "std Time",
                                                                           "H-Error",
                                                                           "std H-Error",
                                                                           "V-Error",
                                                                           "std V-Error",
                                                                           "Hitrate"]).transpose().round(2)
print(output)
# ---------------------------
