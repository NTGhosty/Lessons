import numpy as np
import pandas as pd

rng = np.random.default_rng(1)

mi1 = pd.MultiIndex.from_product(
    [["A1", "A2"], [2025, 2026]], names=["property", "year"]
)
print(mi1)

mi2 = pd.MultiIndex.from_product(
    [["B1", "B2", "B3"], ["jan", "feb"]], names=["shop", "month"]
)
print(mi2)

data = rng.random((4, 6))

print(data)

df = pd.DataFrame(data, index = mi1, columns = mi2)
# print(df)
#
# # по столбцам
# print(df["B2"])
# print(df["B2", "feb"])
#
# # срезы
# print(df.iloc[1:, 2:5])
#
# print(df.loc[:, "B1"])
#
# print(df.loc[:, ("B1", "jan")])
#
# print(df.loc[:, (["B1", "B2"], "jan")])
#
# ind1 = pd.IndexSlice[:, 2025]
# ind2 = pd.IndexSlice[:, "jan"]
#
# print(df.loc[ind1, ind2])

data = {
    ("A1", 2025): 1,
    ("A1", 2026): 2,
    ("A1", 2027): 3,
    ("A2", 2025): 11,
    ("A2", 2026): 12,
    ("A2", 2027): 13,
    ("A3", 2025): 21,
    ("A3", 2026): 22,
    ("A3", 2027): 23,
}

sr = pd.Series(data)
sr.index.names = ["property", "year"]

print(sr)
# по нескольким индексам
print(sr["A1"])
print(sr["A1", 2027])
print(sr[:, 2027])

print(sr.loc["A2":"A3", 2025:2026])

print(sr[sr > 12])

print(sr.loc[["A1","A3"], 2025:2026])


index = pd.MultiIndex.from_product([["a", "b", "c"], [2, 1]])

data = pd.Series(rng.random(6), index=index)
print(data)

data = data.sort_index()
print(data)

print(data["a":"b"])


data = {
    ("A1", 2025, 1): 1,
    ("A1", 2025, 2): 2,
    ("A1", 2026, 1): 3,
    ("A1", 2026, 2): 4,
    ("A1", 2027, 1): 5,
    ("A1", 2027, 2): 6,
    ("A2", 2025, 1): 11,
    ("A2", 2025, 2): 12,
    ("A2", 2026, 1): 13,
    ("A2", 2026, 2): 14,
    ("A2", 2027, 1): 15,
    ("A2", 2027, 2): 16,
    ("A3", 2025, 1): 21,
    ("A3", 2025, 2): 22,
    ("A3", 2026, 1): 23,
    ("A3", 2026, 2): 24,
    ("A3", 2027, 1): 25,
    ("A3", 2027, 2): 26,
}

sr = pd.Series(data)

print(sr)

print(sr.unstack())
print(sr.unstack(level = 2))
print(sr.unstack(level = 1))
print(sr.unstack(level = 0))

sr.index.names = ["product", "year", "count"]

print(sr)
print(type(sr))

df = sr.reset_index(name = "value")
print(df)
print(type(df))

print(df.set_index("product"))
print(df.set_index(["product", "count"]))

# Свобные таблицы

import seaborn as sns

# titanic = sns.load_dataset('titanic')
#
# print(type(titanic))
#
# print(titanic.head)
#
# print(titanic.groupby("sex")["survived"].mean())
#
# print(titanic.groupby(["sex", "class"])["survived"].mean())

births = pd.read_csv("data/births.csv")

print(births.head())

births["decade"] = 10 * (births["year"] // 10)

print(births.head())

print(births.pivot_table("births", index = "decade", columns = "gender", aggfunc = "sum"))

import matplotlib.pyplot as plt

births_years = births.pivot_table("births", index = "year", columns = "gender", aggfunc = "sum")
# births_years.plot()

plt.hist(births[births["year"] == 1969]["births"], bins = 100)

q = np.percentile(births["births"], [25,50,75])

print(q)

m = q[1]
sig = 0.74 * (q[2] - q[0])

births = births.query("(births > @m - 5*@sig) & (births < @m + 5*@sig)")

# plt.hist(births[births["year"] == 1969]["births"], bins = 100)
#
# plt.show()

print(births.dtypes)

print(births.index)

births.index = pd.to_datetime(births["year"] * 10000 + births["month"] * 100 + births["day"], format = "%Y%m%d")

print(births.index)

births["dayofweek"] = births.index.dayofweek

print(births.head())


births_dow = births.pivot_table("births", index = "dayofweek", columns = "decade", aggfunc = "mean")

print(births_dow)

births_dom = births.pivot_table("births", index = [births.month, births.day])

print(births_dom)

from datetime import datetime

print(births.dtypes)

births_dom.index = [datetime(2012, month, day) for (month, day) in births_dom.index]

print(births_dom.head())

births_dom.plot()
plt.show()


