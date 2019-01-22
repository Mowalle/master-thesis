#!/usr/bin/env python3

import pandas as pd

import sys

num_users = 14
num_conditions = 3
num_tasks = 6

# Means per condition ----

df = pd.read_csv(str(sys.argv[1]), delimiter=",")
df = df[["conditionIndex", "megamapTime", "horizOffsetDeg", "vertOffsetDeg"]]

meansPerCondition = []
for condition in range(0, num_conditions):
    df_cond = df[df["conditionIndex"] == condition]
    means = {
        "conditionIndex": condition,
        "Mean megamapTime": df_cond["megamapTime"].mean(),
        "Mean horizOffsetDeg": df_cond["horizOffsetDeg"].mean(),
        "Mean vertOffsetDeg": df_cond["vertOffsetDeg"].mean()}
    meansPerCondition.append(means)

print("Means per condition:")
for row in meansPerCondition:
    print(row)

# ---------------------------
